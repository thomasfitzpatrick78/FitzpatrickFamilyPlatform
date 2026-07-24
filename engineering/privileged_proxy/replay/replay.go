package replay

import (
	"bytes"
	"encoding/json"
	"errors"
	"io"
	"os"
	"path/filepath"
	"slices"
	"sync"
	"time"

	"fitzpatrickfamilyplatform/engineering/privileged_proxy/protocol"
)

const (
	fileVersion         = "repository-test-replay-v1"
	maximumJournalBytes = 1_048_576
	DefaultRetention    = 24 * time.Hour
	DefaultMaximumAge   = 90 * 24 * time.Hour
)

type Journal interface {
	CheckAndConsume(authorizationReference, nonce string, expiresAt, now time.Time) *protocol.Failure
}

type entry struct {
	AuthorizationReference string `json:"authorization_reference"`
	ExpiresAt              string `json:"expires_at"`
	Nonce                  string `json:"nonce"`
}

type MemoryJournal struct {
	capacity  int
	entries   []entry
	mutex     sync.Mutex
	retention time.Duration
}

func NewMemoryJournal(capacity int, retention time.Duration) (*MemoryJournal, *protocol.Failure) {
	if capacity <= 0 || capacity > 100_000 || retention < 0 {
		return nil, protocol.Fail(protocol.ReasonReplayStateUnavailable, "Replay journal configuration is invalid.")
	}
	return &MemoryJournal{capacity: capacity, retention: retention}, nil
}

func (journal *MemoryJournal) CheckAndConsume(
	authorizationReference, nonce string,
	expiresAt, now time.Time,
) *protocol.Failure {
	journal.mutex.Lock()
	defer journal.mutex.Unlock()
	journal.entries = retain(journal.entries, now, journal.retention)
	if failure := check(journal.entries, authorizationReference, nonce); failure != nil {
		return failure
	}
	if len(journal.entries) >= journal.capacity {
		return protocol.Fail(protocol.ReasonReplayStateUnavailable, "Replay journal capacity is exhausted.")
	}
	journal.entries = append(journal.entries, newEntry(authorizationReference, nonce, expiresAt))
	sortEntries(journal.entries)
	return nil
}

// FileJournal is an ordinary-file, repository-test implementation. Its
// atomicity is in-process plus same-directory durable replacement; it is not an
// approved production persistence mechanism.
type FileJournal struct {
	capacity   int
	maximumAge time.Duration
	mutex      sync.Mutex
	path       string
	retention  time.Duration
}

type FileOptions struct {
	Capacity   int
	MaximumAge time.Duration
	Retention  time.Duration
}

func NewTestFileJournal(root, name string, options FileOptions, now time.Time) (*FileJournal, *protocol.Failure) {
	if !filepath.IsAbs(root) || filepath.Base(name) != name || name == "." || name == "" ||
		options.Capacity <= 0 || options.MaximumAge <= 0 || options.Retention < 0 {
		return nil, protocol.Fail(protocol.ReasonReplayStateUnavailable, "Replay test-journal path or limits are invalid.")
	}
	info, err := os.Lstat(root)
	if err != nil || !info.IsDir() || info.Mode()&os.ModeSymlink != 0 {
		return nil, protocol.Fail(protocol.ReasonReplayStateUnavailable, "Replay test-journal root is unavailable.")
	}
	journal := &FileJournal{
		capacity:   options.Capacity,
		maximumAge: options.MaximumAge,
		path:       filepath.Join(root, name),
		retention:  options.Retention,
	}
	if _, err := os.Lstat(journal.path); err == nil {
		if _, failure := journal.load(now); failure != nil {
			return nil, failure
		}
		return journal, nil
	} else if !errors.Is(err, os.ErrNotExist) {
		return nil, protocol.Fail(protocol.ReasonReplayStateUnavailable, "Replay test journal cannot be inspected.")
	}
	initial := fileState{Entries: []entry{}, UpdatedAt: now.UTC().Format(time.RFC3339Nano), Version: fileVersion}
	if failure := journal.write(initial); failure != nil {
		return nil, failure
	}
	return journal, nil
}

func (journal *FileJournal) CheckAndConsume(
	authorizationReference, nonce string,
	expiresAt, now time.Time,
) *protocol.Failure {
	journal.mutex.Lock()
	defer journal.mutex.Unlock()
	state, failure := journal.load(now)
	if failure != nil {
		return failure
	}
	state.Entries = retain(state.Entries, now, journal.retention)
	if failure := check(state.Entries, authorizationReference, nonce); failure != nil {
		return failure
	}
	if len(state.Entries) >= journal.capacity {
		return protocol.Fail(protocol.ReasonReplayStateUnavailable, "Replay journal capacity is exhausted.")
	}
	state.Entries = append(state.Entries, newEntry(authorizationReference, nonce, expiresAt))
	sortEntries(state.Entries)
	state.UpdatedAt = now.UTC().Format(time.RFC3339Nano)
	return journal.write(state)
}

func (journal *FileJournal) load(now time.Time) (fileState, *protocol.Failure) {
	var zero fileState
	if _, err := os.Lstat(journal.path + ".pending"); err == nil {
		return zero, protocol.Fail(protocol.ReasonReplayStateCorrupt, "Partial replay-journal replacement exists.")
	} else if !errors.Is(err, os.ErrNotExist) {
		return zero, protocol.Fail(protocol.ReasonReplayStateUnavailable, "Replay journal replacement state is unavailable.")
	}
	info, err := os.Lstat(journal.path)
	if err != nil || !info.Mode().IsRegular() || info.Mode()&os.ModeSymlink != 0 || info.Size() > maximumJournalBytes {
		return zero, protocol.Fail(protocol.ReasonReplayStateUnavailable, "Replay journal is unavailable or unsafe.")
	}
	data, err := os.ReadFile(journal.path)
	if err != nil {
		return zero, protocol.Fail(protocol.ReasonReplayStateUnavailable, "Replay journal cannot be read.")
	}
	if failure := protocol.ValidateCanonicalJSON(data, maximumJournalBytes); failure != nil {
		return zero, protocol.Fail(protocol.ReasonReplayStateCorrupt, "Replay journal is not canonical.")
	}
	decoder := json.NewDecoder(bytes.NewReader(data))
	decoder.DisallowUnknownFields()
	var state fileState
	if err := decoder.Decode(&state); err != nil || requireEOF(decoder) != nil || state.Version != fileVersion {
		return zero, protocol.Fail(protocol.ReasonReplayStateCorrupt, "Replay journal structure is corrupt.")
	}
	content := stateContent{Entries: state.Entries, UpdatedAt: state.UpdatedAt, Version: state.Version}
	canonical, failure := protocol.EncodeCanonical(content, maximumJournalBytes)
	if failure != nil || !protocol.ConstantDigestEqual(protocol.SHA256Digest(canonical), state.Checksum) {
		return zero, protocol.Fail(protocol.ReasonReplayStateCorrupt, "Replay journal checksum is invalid.")
	}
	updatedAt, parseErr := time.Parse(time.RFC3339Nano, state.UpdatedAt)
	if parseErr != nil || now.Before(updatedAt) || now.Sub(updatedAt) > journal.maximumAge {
		return zero, protocol.Fail(protocol.ReasonReplayStateCorrupt, "Replay journal is stale or time-ambiguous.")
	}
	if len(state.Entries) > journal.capacity || !slices.IsSortedFunc(state.Entries, compareEntries) {
		return zero, protocol.Fail(protocol.ReasonReplayStateCorrupt, "Replay journal entries are invalid.")
	}
	seenNonces := make(map[string]struct{}, len(state.Entries))
	for index, current := range state.Entries {
		if current.AuthorizationReference == "" || current.Nonce == "" {
			return zero, protocol.Fail(protocol.ReasonReplayStateCorrupt, "Replay journal entry is incomplete.")
		}
		if index > 0 && current.AuthorizationReference == state.Entries[index-1].AuthorizationReference {
			return zero, protocol.Fail(protocol.ReasonReplayStateCorrupt, "Replay journal entry is duplicated.")
		}
		if _, duplicate := seenNonces[current.Nonce]; duplicate {
			return zero, protocol.Fail(protocol.ReasonReplayStateCorrupt, "Replay journal nonce is duplicated.")
		}
		seenNonces[current.Nonce] = struct{}{}
		if _, err := time.Parse(time.RFC3339Nano, current.ExpiresAt); err != nil {
			return zero, protocol.Fail(protocol.ReasonReplayStateCorrupt, "Replay journal expiration is invalid.")
		}
	}
	return state, nil
}

func (journal *FileJournal) write(state fileState) *protocol.Failure {
	content := stateContent{Entries: state.Entries, UpdatedAt: state.UpdatedAt, Version: state.Version}
	contentBytes, failure := protocol.EncodeCanonical(content, maximumJournalBytes)
	if failure != nil {
		return protocol.Fail(protocol.ReasonReplayStateUnavailable, "Replay journal content exceeds its bound.")
	}
	state.Checksum = protocol.SHA256Digest(contentBytes)
	data, failure := protocol.EncodeCanonical(state, maximumJournalBytes)
	if failure != nil {
		return protocol.Fail(protocol.ReasonReplayStateUnavailable, "Replay journal exceeds its bound.")
	}
	pending := journal.path + ".pending"
	file, err := os.OpenFile(pending, os.O_CREATE|os.O_EXCL|os.O_WRONLY, 0o600)
	if err != nil {
		return protocol.Fail(protocol.ReasonReplayStateUnavailable, "Replay journal replacement cannot be created.")
	}
	removePending := true
	defer func() {
		if removePending {
			_ = os.Remove(pending)
		}
	}()
	_, writeErr := file.Write(data)
	syncErr := file.Sync()
	closeErr := file.Close()
	if writeErr != nil || syncErr != nil || closeErr != nil {
		return protocol.Fail(protocol.ReasonReplayStateUnavailable, "Replay journal replacement was not durably written.")
	}
	if err = os.Rename(pending, journal.path); err != nil {
		return protocol.Fail(protocol.ReasonReplayStateUnavailable, "Replay journal replacement failed.")
	}
	removePending = false
	directory, err := os.Open(filepath.Dir(journal.path))
	if err != nil {
		return protocol.Fail(protocol.ReasonReplayStateUnavailable, "Replay journal directory cannot be verified.")
	}
	directorySyncErr := directory.Sync()
	directoryCloseErr := directory.Close()
	if directorySyncErr != nil || directoryCloseErr != nil {
		return protocol.Fail(protocol.ReasonReplayStateUnavailable, "Replay journal directory was not durably synchronized.")
	}
	return nil
}

type fileState struct {
	Checksum  string  `json:"checksum"`
	Entries   []entry `json:"entries"`
	UpdatedAt string  `json:"updated_at"`
	Version   string  `json:"version"`
}

type stateContent struct {
	Entries   []entry `json:"entries"`
	UpdatedAt string  `json:"updated_at"`
	Version   string  `json:"version"`
}

func newEntry(reference, nonce string, expiresAt time.Time) entry {
	return entry{
		AuthorizationReference: reference,
		ExpiresAt:              expiresAt.UTC().Format(time.RFC3339Nano),
		Nonce:                  nonce,
	}
}

func check(entries []entry, reference, nonce string) *protocol.Failure {
	if reference == "" || nonce == "" {
		return protocol.Fail(protocol.ReasonAuthorizationInvalid, "Replay binding is incomplete.")
	}
	seenNonces := make(map[string]struct{}, len(entries))
	for _, current := range entries {
		if current.Nonce == nonce || current.AuthorizationReference == reference {
			return protocol.Fail(protocol.ReasonAuthorizationReplayed, protocol.SafeMessage(protocol.ReasonAuthorizationReplayed))
		}
		if _, duplicate := seenNonces[current.Nonce]; duplicate {
			return protocol.Fail(protocol.ReasonReplayStateCorrupt, "Replay journal nonce is duplicated.")
		}
		seenNonces[current.Nonce] = struct{}{}
	}
	return nil
}

func retain(entries []entry, now time.Time, retention time.Duration) []entry {
	result := entries[:0]
	for _, current := range entries {
		expiresAt, err := time.Parse(time.RFC3339Nano, current.ExpiresAt)
		if err == nil && now.Before(expiresAt.Add(retention)) {
			result = append(result, current)
		}
	}
	return result
}

func sortEntries(entries []entry) {
	slices.SortFunc(entries, compareEntries)
}

func compareEntries(left, right entry) int {
	if left.AuthorizationReference < right.AuthorizationReference {
		return -1
	}
	if left.AuthorizationReference > right.AuthorizationReference {
		return 1
	}
	if left.Nonce < right.Nonce {
		return -1
	}
	if left.Nonce > right.Nonce {
		return 1
	}
	return 0
}

func requireEOF(decoder *json.Decoder) error {
	var extra any
	err := decoder.Decode(&extra)
	if errors.Is(err, io.EOF) {
		return nil
	}
	if err == nil {
		return errors.New("trailing value")
	}
	return err
}
