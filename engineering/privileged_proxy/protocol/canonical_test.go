package protocol

import (
	"bytes"
	"encoding/json"
	"strings"
	"testing"
)

func testRequest() RequestEnvelope {
	digest := "sha256:" + strings.Repeat("a", 64)
	return RequestEnvelope{
		AdapterArtifactDigest: digest,
		Authorization: AuthorizationEnvelope{
			AdapterArtifactDigest:     digest,
			AdapterIdentity:           "adapter-test",
			Algorithm:                 "Ed25519",
			AllowedOperations:         []Operation{ObserveLifecycle},
			AllowedSignals:            []string{"container.lifecycle.observed_state"},
			ApprovalReference:         "TEST-APPROVAL-1",
			AuthorizationDigest:       digest,
			AuthorizationReference:    "TEST-AUTH-1",
			AuthorizationVersion:      AuthorizationVersion,
			ComposeProject:            "project-test",
			ComposeService:            "service-test",
			ConfigurationDigest:       digest,
			CorrelationID:             "2222222222222222",
			DeploymentBundleDigest:    digest,
			HostReference:             "host-test",
			KeyID:                     "test-key",
			MaxAttempts:               1,
			Nonce:                     strings.Repeat("1", 64),
			PolicyDigest:              digest,
			ProxyImplementationDigest: digest,
			RegistryRecordDigest:      digest,
			SelectorKind:              "compose_identity",
			Signature:                 "TEST-ONLY-NOT-A-CREDENTIAL",
			SignerIdentity:            "test-signer",
			SubjectID:                 "subject-test",
			TrustAnchorDigest:         digest,
			TrustBindingDigest:        digest,
			ValidFrom:                 "2026-07-23T11:59:00Z",
			ValidUntil:                "2026-07-23T12:05:00Z",
		},
		ConfigurationDigest:       digest,
		CorrelationID:             "2222222222222222",
		Deadline:                  "2026-07-23T12:00:05Z",
		DeploymentBundleDigest:    digest,
		Operation:                 ObserveLifecycle,
		PolicyDigest:              digest,
		ProtocolVersion:           ProtocolVersion,
		ProxyImplementationDigest: digest,
		RequestedAt:               "2026-07-23T12:00:00Z",
		RequestedSignals:          []string{"container.lifecycle.observed_state"},
		RequestID:                 "1111111111111111",
		Target: TargetReference{
			ComposeProject:       "project-test",
			ComposeService:       "service-test",
			HostReference:        "host-test",
			RegistryRecordDigest: digest,
			RegistryReference:    "registry/subject-test",
			SelectorKind:         "compose_identity",
			SubjectID:            "subject-test",
		},
		TrustBindingDigest: digest,
	}
}

func TestCanonicalRequestRoundTrip(t *testing.T) {
	request := testRequest()
	data, failure := EncodeCanonical(request, MaximumRequestBytes)
	if failure != nil {
		t.Fatal(failure)
	}
	decoded, failure := DecodeRequest(data)
	if failure != nil {
		t.Fatal(failure)
	}
	roundTrip, failure := EncodeCanonical(decoded, MaximumRequestBytes)
	if failure != nil || !bytes.Equal(data, roundTrip) {
		t.Fatalf("canonical round trip differs: %v", failure)
	}
}

func TestStrictRequestRejections(t *testing.T) {
	canonical, failure := EncodeCanonical(testRequest(), MaximumRequestBytes)
	if failure != nil {
		t.Fatal(failure)
	}
	var object map[string]any
	if err := json.Unmarshal(canonical, &object); err != nil {
		t.Fatal(err)
	}
	object["unknown"] = "denied"
	unknown, _ := json.Marshal(object)
	duplicate := append([]byte(`{"adapter_artifact_digest":"sha256:`+strings.Repeat("a", 64)+`",`), canonical[1:]...)
	cases := []struct {
		name   string
		data   []byte
		reason ReasonCode
	}{
		{"unknown", unknown, ReasonUnknownField},
		{"duplicate", duplicate, ReasonDuplicateField},
		{"whitespace", append([]byte(" "), canonical...), ReasonRequestMalformed},
		{"trailing", append(canonical, []byte(`{}`)...), ReasonRequestMalformed},
		{"float", bytes.Replace(canonical, []byte(`"max_attempts":1`), []byte(`"max_attempts":1.0`), 1), ReasonRequestMalformed},
		{"negative-zero", bytes.Replace(canonical, []byte(`"max_attempts":1`), []byte(`"max_attempts":-0`), 1), ReasonRequestMalformed},
		{"bom", append([]byte{0xef, 0xbb, 0xbf}, canonical...), ReasonRequestMalformed},
	}
	for _, test := range cases {
		t.Run(test.name, func(t *testing.T) {
			_, actual := DecodeRequest(test.data)
			if actual == nil || actual.Reason != test.reason {
				t.Fatalf("got %v, want %s", actual, test.reason)
			}
		})
	}
}

func TestUnicodeConfusableTargetIsRejected(t *testing.T) {
	request := testRequest()
	request.Target.SubjectID = "subject-t\u0435st"
	data, failure := EncodeCanonical(request, MaximumRequestBytes)
	if failure != nil {
		t.Fatal(failure)
	}
	if _, failure = DecodeRequest(data); failure == nil || failure.Reason != ReasonRequestMalformed {
		t.Fatalf("expected canonical ASCII rejection, got %v", failure)
	}
}

func TestRequestSizeLimit(t *testing.T) {
	data := bytes.Repeat([]byte{'x'}, MaximumRequestBytes+1)
	if _, failure := DecodeRequest(data); failure == nil || failure.Reason != ReasonRequestOversized {
		t.Fatalf("expected request_oversized, got %v", failure)
	}
}

func FuzzDecodeRequest(f *testing.F) {
	canonical, _ := EncodeCanonical(testRequest(), MaximumRequestBytes)
	f.Add(canonical)
	f.Add([]byte(`{"protocol_version":"1.0"}`))
	f.Add([]byte(`{"x":1,"x":2}`))
	f.Fuzz(func(t *testing.T, data []byte) {
		_, _ = DecodeRequest(data)
	})
}

func FuzzDigestAndReasonSerialization(f *testing.F) {
	f.Add("request_completed")
	f.Add("authorization_replayed")
	f.Add(strings.Repeat("a", 600))
	f.Fuzz(func(t *testing.T, value string) {
		_, _ = EncodeCanonical(struct {
			Reason string `json:"reason"`
		}{Reason: value}, MaximumResponseBytes)
		_ = SHA256Digest([]byte(value))
	})
}
