package core

import (
	"bytes"
	"crypto/ed25519"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"os"
	"strings"
	"testing"
	"time"

	"fitzpatrickfamilyplatform/engineering/privileged_proxy/audit"
	"fitzpatrickfamilyplatform/engineering/privileged_proxy/authorization"
	"fitzpatrickfamilyplatform/engineering/privileged_proxy/policy"
	"fitzpatrickfamilyplatform/engineering/privileged_proxy/protocol"
	"fitzpatrickfamilyplatform/engineering/privileged_proxy/replay"
	"fitzpatrickfamilyplatform/engineering/privileged_proxy/resource"
	"fitzpatrickfamilyplatform/engineering/privileged_proxy/upstream"
)

const testKeyWarning = "TEST ONLY — NOT A CREDENTIAL"

type testClock struct {
	value time.Time
}

func (clock *testClock) now() time.Time {
	return clock.value
}

type harness struct {
	audit      *audit.MemorySink
	bindings   authorization.ExpectedBindings
	clock      *testClock
	config     Configuration
	observer   *upstream.SyntheticObserver
	peer       protocol.PeerContext
	privateKey ed25519.PrivateKey
	request    protocol.RequestEnvelope
	service    *Service
}

func newHarness(t *testing.T) *harness {
	t.Helper()
	if testKeyWarning == "" {
		t.Fatal("test-key warning missing")
	}
	seed := bytes.Repeat([]byte{0x42}, ed25519.SeedSize)
	privateKey := ed25519.NewKeyFromSeed(seed)
	publicKey := privateKey.Public().(ed25519.PublicKey)
	trustAnchorDigest := protocol.SHA256Digest(publicKey)
	bindings := authorization.ExpectedBindings{
		AdapterArtifactDigest:     testDigest("adapter"),
		AdapterIdentity:           "adapter-service-test",
		ConfigurationDigest:       testDigest("configuration"),
		DeploymentBundleDigest:    testDigest("deployment"),
		PolicyDigest:              publishedPolicy(t).PolicyDigest,
		ProxyImplementationDigest: testDigest("implementation"),
		RegistryRecordDigest:      testDigest("registry"),
		TrustAnchorDigest:         trustAnchorDigest,
		TrustBindingDigest:        testDigest("trust-binding"),
	}
	compiledPolicy, failure := policy.Compile(publishedPolicy(t))
	if failure != nil {
		t.Fatal(failure)
	}
	keys, failure := authorization.NewTrustKeySet([]authorization.TrustKey{{
		ID:             "test-key-1",
		PublicKey:      publicKey,
		SignerIdentity: "test-signer",
	}})
	if failure != nil {
		t.Fatal(failure)
	}
	journal, failure := replay.NewMemoryJournal(128, replay.DefaultRetention)
	if failure != nil {
		t.Fatal(failure)
	}
	admission, failure := resource.NewAdmission(resource.GovernedLimits())
	if failure != nil {
		t.Fatal(failure)
	}
	fixed := time.Date(2026, 7, 23, 12, 0, 0, 0, time.UTC)
	clock := &testClock{value: fixed}
	auditSink := audit.NewMemorySink()
	observer := upstream.NewSyntheticObserver(syntheticResults(fixed))
	configuration := Configuration{
		Admission: admission,
		Audit:     auditSink,
		Bindings:  bindings,
		Keys:      keys,
		Now:       clock.now,
		Observer:  observer,
		Peer: authorization.PeerExpectation{
			GID:             1002,
			ServiceIdentity: bindings.AdapterIdentity,
			UID:             1001,
		},
		Policy:       compiledPolicy,
		ProxyID:      "repository-privileged-proxy-source",
		ProxyVersion: "repository-source-v1.0",
		Replay:       journal,
	}
	service, failure := New(configuration)
	if failure != nil {
		t.Fatal(failure)
	}
	request := baseRequest(bindings, fixed)
	signRequest(t, &request, privateKey)
	return &harness{
		audit:    auditSink,
		bindings: bindings,
		clock:    clock,
		config:   configuration,
		observer: observer,
		peer: protocol.PeerContext{
			GID:               1002,
			IdentitySource:    "synthetic_test",
			PID:               4242,
			ServiceIdentity:   bindings.AdapterIdentity,
			UID:               1001,
			VerificationState: "verified",
		},
		privateKey: privateKey,
		request:    request,
		service:    service,
	}
}

func publishedPolicy(t *testing.T) policy.Source {
	t.Helper()
	data, err := os.ReadFile("../../tests/fixtures/proxy_foundation/proxy-policy.json")
	if err != nil {
		t.Fatal(err)
	}
	var source policy.Source
	if err := json.Unmarshal(data, &source); err != nil {
		t.Fatal(err)
	}
	return source
}

func baseRequest(bindings authorization.ExpectedBindings, now time.Time) protocol.RequestEnvelope {
	request := protocol.RequestEnvelope{
		AdapterArtifactDigest: bindings.AdapterArtifactDigest,
		Authorization: protocol.AuthorizationEnvelope{
			AdapterArtifactDigest:     bindings.AdapterArtifactDigest,
			AdapterIdentity:           bindings.AdapterIdentity,
			Algorithm:                 authorization.Algorithm,
			AllowedOperations:         []protocol.Operation{protocol.ObserveLifecycle},
			AllowedSignals:            []string{"container.lifecycle.observed_state"},
			ApprovalReference:         "TEST-APPROVAL-1",
			AuthorizationReference:    "TEST-AUTH-1",
			AuthorizationVersion:      protocol.AuthorizationVersion,
			ComposeProject:            "project-test",
			ComposeService:            "service-test",
			ConfigurationDigest:       bindings.ConfigurationDigest,
			CorrelationID:             strings.Repeat("2", 16),
			DeploymentBundleDigest:    bindings.DeploymentBundleDigest,
			HostReference:             "host-test",
			KeyID:                     "test-key-1",
			MaxAttempts:               1,
			Nonce:                     strings.Repeat("1", 64),
			PolicyDigest:              bindings.PolicyDigest,
			ProxyImplementationDigest: bindings.ProxyImplementationDigest,
			RegistryRecordDigest:      bindings.RegistryRecordDigest,
			SelectorKind:              "compose_identity",
			SignerIdentity:            "test-signer",
			SubjectID:                 "subject-test",
			TrustAnchorDigest:         bindings.TrustAnchorDigest,
			TrustBindingDigest:        bindings.TrustBindingDigest,
			ValidFrom:                 now.Add(-time.Minute).Format(time.RFC3339Nano),
			ValidUntil:                now.Add(5 * time.Minute).Format(time.RFC3339Nano),
		},
		ConfigurationDigest:       bindings.ConfigurationDigest,
		CorrelationID:             strings.Repeat("2", 16),
		Deadline:                  now.Add(5 * time.Second).Format(time.RFC3339Nano),
		DeploymentBundleDigest:    bindings.DeploymentBundleDigest,
		Operation:                 protocol.ObserveLifecycle,
		PolicyDigest:              bindings.PolicyDigest,
		ProtocolVersion:           protocol.ProtocolVersion,
		ProxyImplementationDigest: bindings.ProxyImplementationDigest,
		RequestedAt:               now.Format(time.RFC3339Nano),
		RequestedSignals:          []string{"container.lifecycle.observed_state"},
		RequestID:                 strings.Repeat("1", 16),
		Target: protocol.TargetReference{
			ComposeProject:       "project-test",
			ComposeService:       "service-test",
			HostReference:        "host-test",
			RegistryRecordDigest: bindings.RegistryRecordDigest,
			RegistryReference:    "registry/subject-test",
			SelectorKind:         "compose_identity",
			SubjectID:            "subject-test",
		},
		TrustBindingDigest: bindings.TrustBindingDigest,
	}
	return request
}

func configureAttempt(t *testing.T, request *protocol.RequestEnvelope, privateKey ed25519.PrivateKey, operation protocol.Operation, attempt int) {
	t.Helper()
	signals := protocol.AllowedSignals(operation)
	request.Operation = operation
	request.RequestedSignals = signals
	request.Authorization.AllowedOperations = []protocol.Operation{operation}
	request.Authorization.AllowedSignals = signals
	request.RequestID = fmt.Sprintf("%016x", attempt+100)
	request.Authorization.AuthorizationReference = fmt.Sprintf("TEST-AUTH-%d", attempt+100)
	request.Authorization.Nonce = fmt.Sprintf("%064x", attempt+100)
	signRequest(t, request, privateKey)
}

func signRequest(t *testing.T, request *protocol.RequestEnvelope, privateKey ed25519.PrivateKey) {
	t.Helper()
	request.Authorization.AuthorizationDigest = ""
	request.Authorization.Signature = ""
	digest, failure := authorization.AuthorizationDigest(request.Authorization)
	if failure != nil {
		t.Fatal(failure)
	}
	request.Authorization.AuthorizationDigest = digest
	signingBytes, failure := authorization.SigningBytes(request.Authorization)
	if failure != nil {
		t.Fatal(failure)
	}
	request.Authorization.Signature = base64.RawURLEncoding.EncodeToString(ed25519.Sign(privateKey, signingBytes))
}

func encodeRequest(t *testing.T, request protocol.RequestEnvelope) []byte {
	t.Helper()
	data, failure := protocol.EncodeCanonical(request, protocol.MaximumRequestBytes)
	if failure != nil {
		t.Fatal(failure)
	}
	return data
}

func decodeResponse(t *testing.T, data []byte) protocol.ResponseEnvelope {
	t.Helper()
	var response protocol.ResponseEnvelope
	if err := json.Unmarshal(data, &response); err != nil {
		t.Fatalf("response is not JSON: %v; %q", err, data)
	}
	return response
}

func testDigest(label string) string {
	return protocol.SHA256Digest([]byte(label))
}

func syntheticResults(now time.Time) upstream.SyntheticResults {
	common := func() upstream.Observation {
		return upstream.Observation{
			Limitations:        []protocol.Limitation{protocol.LimitationFixtureOnly},
			PayloadSizeBytes:   1024,
			ProviderAPIVersion: "synthetic-v1",
			RecordCount:        1,
			TargetHost:         "host-test",
			TargetSubject:      "subject-test",
		}
	}
	identity := common()
	identity.Identity = &protocol.IdentityResult{
		ComposeContainerNumber: "1",
		ComposeProject:         "project-test",
		ComposeService:         "service-test",
		ImageDigest:            testDigest("image"),
		ImageReference:         "example/image:fixture",
		ProviderContext:        "synthetic",
		Resolution:             "exact",
		RuntimeIDReference:     testDigest("runtime"),
		RuntimeName:            "project-test-service-test-1",
	}
	lifecycle := common()
	lifecycle.Lifecycle = &protocol.LifecycleResult{
		ExitCode:   0,
		ObservedAt: now.Format(time.RFC3339Nano),
		Running:    true,
		StartedAt:  now.Add(-time.Hour).Format(time.RFC3339Nano),
		State:      "running",
	}
	health := common()
	health.Health = &protocol.HealthResult{
		Configured: true,
		ObservedAt: now.Format(time.RFC3339Nano),
		State:      "healthy",
	}
	restart := common()
	restart.Restart = &protocol.RestartResult{
		Count:      1,
		Occurred:   true,
		ObservedAt: now.Format(time.RFC3339Nano),
		State:      "running",
	}
	statistics := common()
	statistics.Statistics = &protocol.StatisticsResult{
		CPUOnlineCount:           4,
		CPUSystemUsage:           200,
		CPUTotalUsage:            100,
		CalculationInputComplete: true,
		CgroupMode:               "synthetic",
		MemoryCacheBasis:         10,
		MemoryLimit:              1024,
		MemoryUsage:              512,
		PIDsCurrent:              3,
		ReadAt:                   now.Format(time.RFC3339Nano),
	}
	return upstream.SyntheticResults{
		Health:     health,
		Identity:   identity,
		Lifecycle:  lifecycle,
		Restart:    restart,
		Statistics: statistics,
	}
}

func totalInvocations(observer *upstream.SyntheticObserver) int {
	total := 0
	for _, operation := range []protocol.Operation{
		protocol.ResolveTargetIdentity,
		protocol.ObserveLifecycle,
		protocol.ObserveHealth,
		protocol.ObserveRestartInformation,
		protocol.ObserveStatisticsOnce,
	} {
		total += observer.InvocationCount(operation)
	}
	return total
}
