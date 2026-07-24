package audit

import (
	"os"
	"path/filepath"
	"slices"
	"sync"

	"fitzpatrickfamilyplatform/engineering/privileged_proxy/protocol"
)

const EventVersion = "1.0"

type Event struct {
	AuthorizationReference string                `json:"authorization_reference"`
	Category               protocol.Category     `json:"category"`
	ConfigurationDigest    string                `json:"configuration_digest"`
	CorrelationID          string                `json:"correlation_id"`
	Decision               string                `json:"decision"`
	DeploymentDigest       string                `json:"deployment_digest"`
	EventType              string                `json:"event_type"`
	EventVersion           string                `json:"event_version"`
	ImplementationDigest   string                `json:"implementation_digest"`
	LatencyMilliseconds    int64                 `json:"latency_milliseconds"`
	Limitations            []protocol.Limitation `json:"limitations"`
	Operation              protocol.Operation    `json:"operation"`
	PolicyDigest           string                `json:"policy_digest"`
	ReasonCode             protocol.ReasonCode   `json:"reason_code"`
	RequestID              string                `json:"request_id"`
	Sequence               uint64                `json:"sequence"`
	ServiceIdentity        string                `json:"service_identity"`
	SubjectReference       string                `json:"subject_reference"`
	TargetReference        string                `json:"target_reference"`
	Timestamp              string                `json:"timestamp"`
}

type Sink interface {
	Append(Event) *protocol.Failure
}

type MemorySink struct {
	events    []Event
	failAfter int
	mutex     sync.Mutex
	sequence  uint64
}

func NewMemorySink() *MemorySink {
	return &MemorySink{failAfter: -1}
}

func (sink *MemorySink) Append(event Event) *protocol.Failure {
	sink.mutex.Lock()
	defer sink.mutex.Unlock()
	if sink.failAfter > 0 {
		sink.failAfter--
		if sink.failAfter == 0 {
			sink.failAfter = -1
			return protocol.Fail(protocol.ReasonAuditUnavailable, protocol.SafeMessage(protocol.ReasonAuditUnavailable))
		}
	}
	sink.sequence++
	event.Sequence = sink.sequence
	event.Limitations = slices.Clone(event.Limitations)
	sink.events = append(sink.events, event)
	return nil
}

func (sink *MemorySink) FailNext() {
	sink.mutex.Lock()
	defer sink.mutex.Unlock()
	sink.failAfter = 1
}

func (sink *MemorySink) FailAfter(appends int) {
	sink.mutex.Lock()
	defer sink.mutex.Unlock()
	if appends <= 0 {
		appends = 1
	}
	sink.failAfter = appends
}

func (sink *MemorySink) Events() []Event {
	sink.mutex.Lock()
	defer sink.mutex.Unlock()
	return slices.Clone(sink.events)
}

// TestFileSink is an ordinary-file sink for temporary repository tests only.
type TestFileSink struct {
	file     *os.File
	mutex    sync.Mutex
	sequence uint64
}

func NewTestFileSink(root, name string) (*TestFileSink, *protocol.Failure) {
	if !filepath.IsAbs(root) || filepath.Base(name) != name || name == "" || name == "." {
		return nil, protocol.Fail(protocol.ReasonAuditUnavailable, "Audit test-sink path is invalid.")
	}
	info, err := os.Lstat(root)
	if err != nil || !info.IsDir() || info.Mode()&os.ModeSymlink != 0 {
		return nil, protocol.Fail(protocol.ReasonAuditUnavailable, "Audit test-sink root is unavailable.")
	}
	path := filepath.Join(root, name)
	if existing, err := os.Lstat(path); err == nil && (!existing.Mode().IsRegular() || existing.Mode()&os.ModeSymlink != 0) {
		return nil, protocol.Fail(protocol.ReasonAuditUnavailable, "Audit test-sink path is unsafe.")
	}
	file, err := os.OpenFile(path, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0o600)
	if err != nil {
		return nil, protocol.Fail(protocol.ReasonAuditUnavailable, "Audit test sink cannot be opened.")
	}
	return &TestFileSink{file: file}, nil
}

func (sink *TestFileSink) Append(event Event) *protocol.Failure {
	sink.mutex.Lock()
	defer sink.mutex.Unlock()
	sink.sequence++
	event.Sequence = sink.sequence
	data, failure := protocol.EncodeCanonical(event, protocol.MaximumResponseBytes)
	if failure != nil {
		return protocol.Fail(protocol.ReasonAuditUnavailable, "Audit event is not serializable.")
	}
	data = append(data, '\n')
	if _, err := sink.file.Write(data); err != nil || sink.file.Sync() != nil {
		return protocol.Fail(protocol.ReasonAuditUnavailable, protocol.SafeMessage(protocol.ReasonAuditUnavailable))
	}
	return nil
}

func (sink *TestFileSink) Close() *protocol.Failure {
	sink.mutex.Lock()
	defer sink.mutex.Unlock()
	if err := sink.file.Close(); err != nil {
		return protocol.Fail(protocol.ReasonAuditUnavailable, "Audit test sink could not close.")
	}
	return nil
}
