package replay

import (
	"os"
	"path/filepath"
	"sync"
	"testing"
	"time"

	"fitzpatrickfamilyplatform/engineering/privileged_proxy/protocol"
)

func TestMemoryJournalOneShotConcurrentAndCapacity(t *testing.T) {
	journal, failure := NewMemoryJournal(2, DefaultRetention)
	if failure != nil {
		t.Fatal(failure)
	}
	now := time.Date(2026, 7, 23, 12, 0, 0, 0, time.UTC)
	var successes int
	var mutex sync.Mutex
	var wait sync.WaitGroup
	for range 16 {
		wait.Add(1)
		go func() {
			defer wait.Done()
			if failure := journal.CheckAndConsume("AUTH-1", "NONCE-1", now.Add(time.Minute), now); failure == nil {
				mutex.Lock()
				successes++
				mutex.Unlock()
			}
		}()
	}
	wait.Wait()
	if successes != 1 {
		t.Fatalf("concurrent replay successes = %d, want 1", successes)
	}
	if failure := journal.CheckAndConsume("AUTH-2", "NONCE-2", now.Add(time.Minute), now); failure != nil {
		t.Fatal(failure)
	}
	if failure := journal.CheckAndConsume("AUTH-3", "NONCE-3", now.Add(time.Minute), now); failure == nil ||
		failure.Reason != protocol.ReasonReplayStateUnavailable {
		t.Fatalf("expected capacity failure, got %v", failure)
	}
}

func TestMemoryJournalRejectsReferenceAndNonceReuseIndependently(t *testing.T) {
	journal, failure := NewMemoryJournal(8, DefaultRetention)
	if failure != nil {
		t.Fatal(failure)
	}
	now := time.Date(2026, 7, 23, 12, 0, 0, 0, time.UTC)
	if failure := journal.CheckAndConsume("AUTH-1", "NONCE-1", now.Add(time.Minute), now); failure != nil {
		t.Fatal(failure)
	}
	for _, candidate := range []struct {
		name      string
		reference string
		nonce     string
	}{
		{name: "same reference different nonce", reference: "AUTH-1", nonce: "NONCE-2"},
		{name: "different reference same nonce", reference: "AUTH-2", nonce: "NONCE-1"},
	} {
		t.Run(candidate.name, func(t *testing.T) {
			if failure := journal.CheckAndConsume(
				candidate.reference, candidate.nonce, now.Add(time.Minute), now,
			); failure == nil || failure.Reason != protocol.ReasonAuthorizationReplayed {
				t.Fatalf("expected replay denial, got %v", failure)
			}
		})
	}
}

func TestFileJournalPersistsReplayAndRejectsCorruption(t *testing.T) {
	root := t.TempDir()
	now := time.Date(2026, 7, 23, 12, 0, 0, 0, time.UTC)
	options := FileOptions{Capacity: 8, MaximumAge: DefaultMaximumAge, Retention: DefaultRetention}
	journal, failure := NewTestFileJournal(root, "replay.json", options, now)
	if failure != nil {
		t.Fatal(failure)
	}
	if failure := journal.CheckAndConsume("AUTH-1", "NONCE-1", now.Add(time.Minute), now); failure != nil {
		t.Fatal(failure)
	}
	reopened, failure := NewTestFileJournal(root, "replay.json", options, now)
	if failure != nil {
		t.Fatal(failure)
	}
	if failure := reopened.CheckAndConsume("AUTH-1", "NONCE-1", now.Add(time.Minute), now); failure == nil ||
		failure.Reason != protocol.ReasonAuthorizationReplayed {
		t.Fatalf("expected persisted replay denial, got %v", failure)
	}
	if err := os.WriteFile(filepath.Join(root, "replay.json"), []byte(`{"corrupt":true}`), 0o600); err != nil {
		t.Fatal(err)
	}
	if _, failure := NewTestFileJournal(root, "replay.json", options, now); failure == nil ||
		failure.Reason != protocol.ReasonReplayStateCorrupt {
		t.Fatalf("expected corrupt-state denial, got %v", failure)
	}
}

func TestFileJournalPartialAndStaleStateFailClosed(t *testing.T) {
	root := t.TempDir()
	now := time.Date(2026, 7, 23, 12, 0, 0, 0, time.UTC)
	options := FileOptions{Capacity: 8, MaximumAge: time.Hour, Retention: DefaultRetention}
	journal, failure := NewTestFileJournal(root, "replay.json", options, now)
	if failure != nil {
		t.Fatal(failure)
	}
	if err := os.WriteFile(filepath.Join(root, "replay.json.pending"), []byte("partial"), 0o600); err != nil {
		t.Fatal(err)
	}
	if failure := journal.CheckAndConsume("AUTH-1", "NONCE-1", now.Add(time.Minute), now); failure == nil ||
		failure.Reason != protocol.ReasonReplayStateCorrupt {
		t.Fatalf("expected partial-write denial, got %v", failure)
	}
	if err := os.Remove(filepath.Join(root, "replay.json.pending")); err != nil {
		t.Fatal(err)
	}
	if failure := journal.CheckAndConsume("AUTH-1", "NONCE-1", now.Add(time.Minute), now.Add(2*time.Hour)); failure == nil ||
		failure.Reason != protocol.ReasonReplayStateCorrupt {
		t.Fatalf("expected stale-state denial, got %v", failure)
	}
}

func TestFileJournalUnreadableAndUnwritableStateFailsClosed(t *testing.T) {
	t.Run("unreadable state type", func(t *testing.T) {
		root := t.TempDir()
		now := time.Date(2026, 7, 23, 12, 0, 0, 0, time.UTC)
		options := FileOptions{Capacity: 8, MaximumAge: DefaultMaximumAge, Retention: DefaultRetention}
		journal, failure := NewTestFileJournal(root, "replay.json", options, now)
		if failure != nil {
			t.Fatal(failure)
		}
		path := filepath.Join(root, "replay.json")
		if err := os.Remove(path); err != nil {
			t.Fatal(err)
		}
		if err := os.Mkdir(path, 0o700); err != nil {
			t.Fatal(err)
		}
		if failure := journal.CheckAndConsume(
			"AUTH-1", "NONCE-1", now.Add(time.Minute), now,
		); failure == nil || failure.Reason != protocol.ReasonReplayStateUnavailable {
			t.Fatalf("expected unreadable-state denial, got %v", failure)
		}
	})

	t.Run("unwritable journal root", func(t *testing.T) {
		root := t.TempDir()
		now := time.Date(2026, 7, 23, 12, 0, 0, 0, time.UTC)
		options := FileOptions{Capacity: 8, MaximumAge: DefaultMaximumAge, Retention: DefaultRetention}
		journal, failure := NewTestFileJournal(root, "replay.json", options, now)
		if failure != nil {
			t.Fatal(failure)
		}
		if err := os.Chmod(root, 0o500); err != nil {
			t.Fatal(err)
		}
		t.Cleanup(func() {
			if err := os.Chmod(root, 0o700); err != nil {
				t.Errorf("restore journal-root permissions: %v", err)
			}
		})
		if failure := journal.CheckAndConsume(
			"AUTH-1", "NONCE-1", now.Add(time.Minute), now,
		); failure == nil || failure.Reason != protocol.ReasonReplayStateUnavailable {
			t.Fatalf("expected unwritable-state denial, got %v", failure)
		}
	})
}

func FuzzFileJournalStateDecoding(f *testing.F) {
	f.Add([]byte(`{"checksum":"sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","entries":[],"updated_at":"2026-07-23T12:00:00Z","version":"repository-test-replay-v1"}`))
	f.Add([]byte(`{"entries":[]}`))
	f.Fuzz(func(t *testing.T, data []byte) {
		if len(data) > maximumJournalBytes {
			return
		}
		root := t.TempDir()
		path := filepath.Join(root, "replay.json")
		if err := os.WriteFile(path, data, 0o600); err != nil {
			t.Fatal(err)
		}
		_, _ = NewTestFileJournal(root, "replay.json", FileOptions{
			Capacity: 8, MaximumAge: DefaultMaximumAge, Retention: DefaultRetention,
		}, time.Date(2026, 7, 23, 12, 0, 0, 0, time.UTC))
	})
}
