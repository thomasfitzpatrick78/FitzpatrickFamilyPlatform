package policy

import (
	"encoding/json"
	"os"
	"testing"

	"fitzpatrickfamilyplatform/engineering/privileged_proxy/protocol"
)

func loadPublished(t *testing.T) Source {
	t.Helper()
	data, err := os.ReadFile("../../tests/fixtures/proxy_foundation/proxy-policy.json")
	if err != nil {
		t.Fatal(err)
	}
	var source Source
	if err := json.Unmarshal(data, &source); err != nil {
		t.Fatal(err)
	}
	return source
}

func TestPublishedPolicyCompilesAndClosesDispatch(t *testing.T) {
	compiled, failure := Compile(loadPublished(t))
	if failure != nil {
		t.Fatal(failure)
	}
	for _, operation := range []protocol.Operation{
		protocol.ResolveTargetIdentity,
		protocol.ObserveLifecycle,
		protocol.ObserveHealth,
		protocol.ObserveRestartInformation,
		protocol.ObserveStatisticsOnce,
	} {
		if failure := compiled.Evaluate(operation); failure != nil {
			t.Fatalf("%s: %v", operation, failure)
		}
	}
	for _, operation := range []protocol.Operation{protocol.CheckProviderCompatibility, "UnknownOperation"} {
		if failure := compiled.Evaluate(operation); failure == nil {
			t.Fatalf("%s unexpectedly allowed", operation)
		}
	}
}

func TestPolicyDigestAndDefaultDenyFailClosed(t *testing.T) {
	source := loadPublished(t)
	source.PolicyDigest = "sha256:" + string(make([]byte, 64))
	if _, failure := Compile(source); failure == nil || failure.Reason != protocol.ReasonPolicyDigestMismatch {
		t.Fatalf("expected digest mismatch, got %v", failure)
	}
	source = loadPublished(t)
	source.DefaultState = Allowed
	if _, failure := Compile(source); failure == nil {
		t.Fatal("non-deny default unexpectedly compiled")
	}
}
