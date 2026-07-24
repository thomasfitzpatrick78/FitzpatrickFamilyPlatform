package core

import (
	"bytes"
	"context"
	"encoding/json"
	"strings"
	"sync"
	"testing"
	"time"

	"fitzpatrickfamilyplatform/engineering/privileged_proxy/protocol"
	"fitzpatrickfamilyplatform/engineering/privileged_proxy/upstream"
)

func TestTransportFreePipelineSupportsFiveApprovedOperations(t *testing.T) {
	operations := []protocol.Operation{
		protocol.ResolveTargetIdentity,
		protocol.ObserveLifecycle,
		protocol.ObserveHealth,
		protocol.ObserveRestartInformation,
		protocol.ObserveStatisticsOnce,
	}
	for index, operation := range operations {
		t.Run(string(operation), func(t *testing.T) {
			harness := newHarness(t)
			configureAttempt(t, &harness.request, harness.privateKey, operation, index)
			data, err := harness.service.Handle(context.Background(), harness.peer, encodeRequest(t, harness.request))
			if err != nil {
				t.Fatal(err)
			}
			response := decodeResponse(t, data)
			if response.Decision != "allowed" || response.ReasonCode != protocol.ReasonRequestCompleted ||
				response.Result == nil {
				t.Fatalf("unexpected response: %+v", response)
			}
			if harness.observer.InvocationCount(operation) != 1 {
				t.Fatalf("typed observer invocation count = %d", harness.observer.InvocationCount(operation))
			}
			if !bytes.Equal(data, mustCanonicalResponse(t, response)) {
				t.Fatal("response is not byte-stable canonical JSON")
			}
		})
	}
}

func TestPreUpstreamDenialsNeverInvokeSyntheticObserver(t *testing.T) {
	alternate := testDigest("alternate")
	tests := []struct {
		name   string
		reason protocol.ReasonCode
		resign bool
		mutate func(*harness)
	}{
		{"wrong-peer", protocol.ReasonIdentityMismatch, false, func(h *harness) { h.peer.UID++ }},
		{"unsupported-protocol", protocol.ReasonProtocolUnsupported, false, func(h *harness) { h.request.ProtocolVersion = "2.0" }},
		{"wrong-identity", protocol.ReasonIdentityMismatch, true, func(h *harness) { h.request.Authorization.AdapterIdentity = "wrong-adapter" }},
		{"invalid-signature", protocol.ReasonSignatureInvalid, false, func(h *harness) { h.request.Authorization.Signature = strings.Repeat("A", 86) }},
		{"unknown-key", protocol.ReasonUnknownKey, true, func(h *harness) { h.request.Authorization.KeyID = "unknown-key" }},
		{"expired", protocol.ReasonAuthorizationExpired, true, func(h *harness) { h.clock.value = h.clock.value.Add(10 * time.Minute) }},
		{"future", protocol.ReasonAuthorizationFuture, true, func(h *harness) {
			h.request.Authorization.ValidFrom = h.clock.value.Add(2 * time.Minute).Format(time.RFC3339Nano)
		}},
		{"lifetime", protocol.ReasonAuthorizationLifetime, true, func(h *harness) {
			h.request.Authorization.ValidUntil = h.clock.value.Add(16 * time.Minute).Format(time.RFC3339Nano)
		}},
		{"approval-missing", protocol.ReasonAuthorizationInvalid, true, func(h *harness) { h.request.Authorization.ApprovalReference = "" }},
		{"nonce-invalid", protocol.ReasonAuthorizationInvalid, true, func(h *harness) { h.request.Authorization.Nonce = "short" }},
		{"wrong-subject", protocol.ReasonTargetMismatch, false, func(h *harness) { h.request.Target.SubjectID = "different-subject" }},
		{"subject-case-change", protocol.ReasonTargetMismatch, false, func(h *harness) { h.request.Target.SubjectID = "Subject-test" }},
		{"subject-prefix", protocol.ReasonTargetMismatch, false, func(h *harness) { h.request.Target.SubjectID = "prefix-subject-test" }},
		{"subject-suffix", protocol.ReasonTargetMismatch, false, func(h *harness) { h.request.Target.SubjectID = "subject-test-suffix" }},
		{"subject-encoding", protocol.ReasonTargetInvalid, false, func(h *harness) { h.request.Target.SubjectID = "%73ubject-test" }},
		{"subject-whitespace", protocol.ReasonTargetInvalid, false, func(h *harness) { h.request.Target.SubjectID = " subject-test" }},
		{"selector-substitution", protocol.ReasonTargetMismatch, false, func(h *harness) { h.request.Target.ComposeService = "different-service" }},
		{"wildcard", protocol.ReasonWildcardDenied, false, func(h *harness) { h.request.Target.SubjectID = "*" }},
		{"unsupported-operation", protocol.ReasonOperationDenied, true, func(h *harness) {
			h.request.Operation = "UnknownOperation"
			h.request.Authorization.AllowedOperations = []protocol.Operation{"UnknownOperation"}
		}},
		{"reserved-operation", protocol.ReasonOperationDenied, true, func(h *harness) {
			h.request.Operation = protocol.CheckProviderCompatibility
			h.request.Authorization.AllowedOperations = []protocol.Operation{protocol.CheckProviderCompatibility}
		}},
		{"signal-scope", protocol.ReasonSignalDenied, true, func(h *harness) {
			h.request.RequestedSignals = []string{"container.healthcheck.state"}
			h.request.Authorization.AllowedSignals = []string{"container.healthcheck.state"}
		}},
		{"missing-digest", protocol.ReasonAuthorizationInvalid, true, func(h *harness) {
			h.request.ConfigurationDigest = ""
			h.request.Authorization.ConfigurationDigest = ""
		}},
		{"policy-digest", protocol.ReasonPolicyDigestMismatch, true, func(h *harness) {
			h.request.PolicyDigest = alternate
			h.request.Authorization.PolicyDigest = alternate
		}},
		{"configuration-digest", protocol.ReasonConfigurationDigestMismatch, true, func(h *harness) {
			h.request.ConfigurationDigest = alternate
			h.request.Authorization.ConfigurationDigest = alternate
		}},
		{"deployment-digest", protocol.ReasonDeploymentDigestMismatch, true, func(h *harness) {
			h.request.DeploymentBundleDigest = alternate
			h.request.Authorization.DeploymentBundleDigest = alternate
		}},
		{"adapter-digest", protocol.ReasonAdapterDigestMismatch, true, func(h *harness) {
			h.request.AdapterArtifactDigest = alternate
			h.request.Authorization.AdapterArtifactDigest = alternate
		}},
		{"implementation-digest", protocol.ReasonProxyDigestMismatch, true, func(h *harness) {
			h.request.ProxyImplementationDigest = alternate
			h.request.Authorization.ProxyImplementationDigest = alternate
		}},
		{"registry-digest", protocol.ReasonRegistryDigestMismatch, true, func(h *harness) {
			h.request.Target.RegistryRecordDigest = alternate
			h.request.Authorization.RegistryRecordDigest = alternate
		}},
		{"trust-anchor", protocol.ReasonTrustAnchorMismatch, true, func(h *harness) {
			h.request.Authorization.TrustAnchorDigest = alternate
		}},
		{"trust-binding", protocol.ReasonTrustBindingDigestMismatch, true, func(h *harness) {
			h.request.TrustBindingDigest = alternate
			h.request.Authorization.TrustBindingDigest = alternate
		}},
	}
	for _, test := range tests {
		t.Run(test.name, func(t *testing.T) {
			harness := newHarness(t)
			test.mutate(harness)
			if test.resign {
				signRequest(t, &harness.request, harness.privateKey)
			}
			data, err := harness.service.Handle(context.Background(), harness.peer, encodeRequest(t, harness.request))
			if err != nil {
				t.Fatal(err)
			}
			response := decodeResponse(t, data)
			if response.ReasonCode != test.reason {
				t.Fatalf("got %s, want %s", response.ReasonCode, test.reason)
			}
			if totalInvocations(harness.observer) != 0 {
				t.Fatal("synthetic observer invoked before denial")
			}
		})
	}
}

func TestMalformedUnknownDuplicateAndOversizedRequestsFailBeforeUpstream(t *testing.T) {
	harness := newHarness(t)
	canonical := encodeRequest(t, harness.request)
	var object map[string]any
	if err := json.Unmarshal(canonical, &object); err != nil {
		t.Fatal(err)
	}
	object["unknown"] = "denied"
	unknown, _ := json.Marshal(object)
	duplicate := append([]byte(`{"adapter_artifact_digest":"`+harness.bindings.AdapterArtifactDigest+`",`), canonical[1:]...)
	cases := [][]byte{
		[]byte(`{"malformed":`),
		unknown,
		duplicate,
		bytes.Repeat([]byte{'x'}, protocol.MaximumRequestBytes+1),
	}
	for _, data := range cases {
		if _, err := harness.service.Handle(context.Background(), harness.peer, data); err == nil {
			t.Fatal("malformed request unexpectedly returned no error")
		}
	}
	if totalInvocations(harness.observer) != 0 {
		t.Fatal("synthetic observer invoked for malformed input")
	}
}

func TestReplayConsumesNonceBeforeLaterAttemptBoundary(t *testing.T) {
	harness := newHarness(t)
	cancelled, cancel := context.WithCancel(context.Background())
	cancel()
	data, err := harness.service.Handle(cancelled, harness.peer, encodeRequest(t, harness.request))
	if err != nil {
		t.Fatal(err)
	}
	if response := decodeResponse(t, data); response.ReasonCode != protocol.ReasonRequestTimedOut {
		t.Fatalf("got %s", response.ReasonCode)
	}
	data, err = harness.service.Handle(context.Background(), harness.peer, encodeRequest(t, harness.request))
	if err != nil {
		t.Fatal(err)
	}
	if response := decodeResponse(t, data); response.ReasonCode != protocol.ReasonAuthorizationReplayed {
		t.Fatalf("got %s", response.ReasonCode)
	}
	if totalInvocations(harness.observer) != 0 {
		t.Fatal("observer invoked despite cancellation and replay")
	}
}

func TestConcurrentReplayAllowsAtMostOneUpstreamInvocation(t *testing.T) {
	harness := newHarness(t)
	requestBytes := encodeRequest(t, harness.request)
	var wait sync.WaitGroup
	for range 16 {
		wait.Add(1)
		go func() {
			defer wait.Done()
			_, _ = harness.service.Handle(context.Background(), harness.peer, requestBytes)
		}()
	}
	wait.Wait()
	if count := totalInvocations(harness.observer); count != 1 {
		t.Fatalf("observer invocation count = %d, want 1", count)
	}
}

func TestProjectionRejectsLeakageRecordAndResponseSize(t *testing.T) {
	tests := []struct {
		name        string
		reason      protocol.ReasonCode
		observation func(time.Time) upstream.Observation
	}{
		{"unexpected-field", protocol.ReasonResponseFieldRejected, func(now time.Time) upstream.Observation {
			value := syntheticResults(now).Lifecycle
			value.UnexpectedFields = []string{"environment"}
			return value
		}},
		{"record-limit", protocol.ReasonRecordLimitExceeded, func(now time.Time) upstream.Observation {
			value := syntheticResults(now).Lifecycle
			value.RecordCount = 2
			return value
		}},
		{"oversized", protocol.ReasonResponseOversized, func(now time.Time) upstream.Observation {
			value := syntheticResults(now).Lifecycle
			value.PayloadSizeBytes = protocol.MaximumResponseBytes + 1
			return value
		}},
		{"target-substitution", protocol.ReasonTargetMismatch, func(now time.Time) upstream.Observation {
			value := syntheticResults(now).Lifecycle
			value.TargetSubject = "other-subject"
			return value
		}},
		{"unsafe-value", protocol.ReasonResponseMalformed, func(now time.Time) upstream.Observation {
			value := syntheticResults(now).Lifecycle
			value.Lifecycle.State = "running\nsecret"
			return value
		}},
	}
	for _, test := range tests {
		t.Run(test.name, func(t *testing.T) {
			harness := newHarness(t)
			harness.observer.SetObservation(protocol.ObserveLifecycle, test.observation(harness.clock.value))
			data, err := harness.service.Handle(context.Background(), harness.peer, encodeRequest(t, harness.request))
			if err != nil {
				t.Fatal(err)
			}
			response := decodeResponse(t, data)
			if response.ReasonCode != test.reason {
				t.Fatalf("got %s, want %s", response.ReasonCode, test.reason)
			}
		})
	}
}

func TestSyntheticUpstreamFailureAndTimeoutAreBounded(t *testing.T) {
	for _, reason := range []protocol.ReasonCode{protocol.ReasonProviderUnavailable, protocol.ReasonUpstreamTimedOut} {
		harness := newHarness(t)
		harness.observer.SetFailure(protocol.ObserveLifecycle, protocol.Fail(reason, "raw provider detail must not pass"))
		data, err := harness.service.Handle(context.Background(), harness.peer, encodeRequest(t, harness.request))
		if err != nil {
			t.Fatal(err)
		}
		response := decodeResponse(t, data)
		if response.ReasonCode != reason || strings.Contains(response.SafeMessage, "raw provider") {
			t.Fatalf("unsafe response: %+v", response)
		}
	}
}

func TestLogicalDeadlineExpiresAfterOneShotConsumptionAndBeforeUpstream(t *testing.T) {
	harness := newHarness(t)
	harness.clock.value = harness.clock.value.Add(5 * time.Second)
	data, err := harness.service.Handle(context.Background(), harness.peer, encodeRequest(t, harness.request))
	if err != nil {
		t.Fatal(err)
	}
	if response := decodeResponse(t, data); response.ReasonCode != protocol.ReasonRequestTimedOut {
		t.Fatalf("got %s", response.ReasonCode)
	}
	if totalInvocations(harness.observer) != 0 {
		t.Fatal("observer invoked after logical request deadline")
	}
	data, err = harness.service.Handle(context.Background(), harness.peer, encodeRequest(t, harness.request))
	if err != nil {
		t.Fatal(err)
	}
	if response := decodeResponse(t, data); response.ReasonCode != protocol.ReasonAuthorizationReplayed {
		t.Fatalf("expected consumed authorization, got %s", response.ReasonCode)
	}
}

func TestFinalAuditFailureReturnsFailureAndDisablesAfterUpstream(t *testing.T) {
	harness := newHarness(t)
	harness.audit.FailAfter(8)
	data, err := harness.service.Handle(context.Background(), harness.peer, encodeRequest(t, harness.request))
	if err == nil {
		t.Fatal("final audit failure unexpectedly returned nil error")
	}
	if response := decodeResponse(t, data); response.ReasonCode != protocol.ReasonAuditUnavailable {
		t.Fatalf("got %s", response.ReasonCode)
	}
	if totalInvocations(harness.observer) != 1 {
		t.Fatal("expected exactly one upstream invocation before final audit failure")
	}
	if _, err := harness.service.Handle(context.Background(), harness.peer, encodeRequest(t, harness.request)); err == nil {
		t.Fatal("core did not remain disabled")
	}
}

type failingReplayJournal struct{}

func (failingReplayJournal) CheckAndConsume(string, string, time.Time, time.Time) *protocol.Failure {
	return protocol.Fail(protocol.ReasonReplayStateCorrupt, "synthetic corrupt replay state")
}

func TestReplayJournalFailureDeniesBeforeUpstream(t *testing.T) {
	harness := newHarness(t)
	harness.config.Replay = failingReplayJournal{}
	service, failure := New(harness.config)
	if failure != nil {
		t.Fatal(failure)
	}
	data, err := service.Handle(context.Background(), harness.peer, encodeRequest(t, harness.request))
	if err != nil {
		t.Fatal(err)
	}
	if response := decodeResponse(t, data); response.ReasonCode != protocol.ReasonReplayStateCorrupt {
		t.Fatalf("got %s", response.ReasonCode)
	}
	if totalInvocations(harness.observer) != 0 {
		t.Fatal("observer invoked with corrupt replay state")
	}
}

func TestAuditFailureDisablesCoreBeforeUpstream(t *testing.T) {
	harness := newHarness(t)
	harness.audit.FailNext()
	data, err := harness.service.Handle(context.Background(), harness.peer, encodeRequest(t, harness.request))
	if err == nil {
		t.Fatal("audit failure unexpectedly returned nil error")
	}
	if response := decodeResponse(t, data); response.ReasonCode != protocol.ReasonAuditUnavailable {
		t.Fatalf("got %s", response.ReasonCode)
	}
	if totalInvocations(harness.observer) != 0 {
		t.Fatal("observer invoked after audit failure")
	}
	if _, err := harness.service.Handle(context.Background(), harness.peer, encodeRequest(t, harness.request)); err == nil {
		t.Fatal("disabled core accepted another request")
	}
}

func TestAuditEventsExcludeSignatureAndRawRequest(t *testing.T) {
	harness := newHarness(t)
	if _, err := harness.service.Handle(context.Background(), harness.peer, encodeRequest(t, harness.request)); err != nil {
		t.Fatal(err)
	}
	events, err := json.Marshal(harness.audit.Events())
	if err != nil {
		t.Fatal(err)
	}
	for _, prohibited := range []string{
		harness.request.Authorization.Signature,
		"TEST ONLY",
		"private",
		"environment",
	} {
		if bytes.Contains(events, []byte(prohibited)) {
			t.Fatalf("audit leaked prohibited value %q", prohibited)
		}
	}
}

func TestRateDenialOccursAfterOneShotConsumptionAndBeforeThirdInvocation(t *testing.T) {
	harness := newHarness(t)
	for attempt := 0; attempt < 3; attempt++ {
		configureAttempt(t, &harness.request, harness.privateKey, protocol.ObserveLifecycle, attempt)
		data, err := harness.service.Handle(context.Background(), harness.peer, encodeRequest(t, harness.request))
		if err != nil {
			t.Fatal(err)
		}
		response := decodeResponse(t, data)
		if attempt < 2 && response.ReasonCode != protocol.ReasonRequestCompleted {
			t.Fatalf("attempt %d got %s", attempt, response.ReasonCode)
		}
		if attempt == 2 && response.ReasonCode != protocol.ReasonRateLimited {
			t.Fatalf("attempt %d got %s", attempt, response.ReasonCode)
		}
	}
	if count := harness.observer.InvocationCount(protocol.ObserveLifecycle); count != 2 {
		t.Fatalf("observer invoked %d times", count)
	}
}

func mustCanonicalResponse(t *testing.T, response protocol.ResponseEnvelope) []byte {
	t.Helper()
	data, failure := protocol.EncodeCanonical(response, protocol.MaximumResponseBytes)
	if failure != nil {
		t.Fatal(failure)
	}
	return data
}

func FuzzCoreRequestBoundary(f *testing.F) {
	f.Add([]byte(`{}`))
	f.Add([]byte(`{"protocol_version":"1.0"}`))
	f.Fuzz(func(t *testing.T, data []byte) {
		harness := newHarness(t)
		_, _ = harness.service.Handle(context.Background(), harness.peer, data)
	})
}
