package audit

import (
	"os"
	"path/filepath"
	"testing"

	"fitzpatrickfamilyplatform/engineering/privileged_proxy/protocol"
)

func TestMemoryAndOrdinaryFileTestSinks(t *testing.T) {
	event := Event{
		Decision:     "accepted",
		EventType:    "core_initialization",
		EventVersion: EventVersion,
		Limitations:  []protocol.Limitation{},
		ReasonCode:   protocol.ReasonRequestCompleted,
		Timestamp:    "2026-07-23T12:00:00Z",
	}
	memory := NewMemorySink()
	if failure := memory.Append(event); failure != nil {
		t.Fatal(failure)
	}
	if events := memory.Events(); len(events) != 1 || events[0].Sequence != 1 {
		t.Fatalf("unexpected events: %+v", events)
	}
	memory.FailNext()
	if failure := memory.Append(event); failure == nil || failure.Reason != protocol.ReasonAuditUnavailable {
		t.Fatalf("expected audit failure, got %v", failure)
	}
	root := t.TempDir()
	file, failure := NewTestFileSink(root, "audit.jsonl")
	if failure != nil {
		t.Fatal(failure)
	}
	if failure := file.Append(event); failure != nil {
		t.Fatal(failure)
	}
	if failure := file.Close(); failure != nil {
		t.Fatal(failure)
	}
	data, err := os.ReadFile(filepath.Join(root, "audit.jsonl"))
	if err != nil || len(data) == 0 {
		t.Fatalf("audit file missing: %v", err)
	}
}
