package authorization

import (
	"bytes"
	"crypto/ed25519"
	"testing"

	"fitzpatrickfamilyplatform/engineering/privileged_proxy/protocol"
)

func TestPeerContextNeverCompletesAuthorization(t *testing.T) {
	expected := PeerExpectation{GID: 2, ServiceIdentity: "adapter-test", UID: 1}
	peer := protocol.PeerContext{
		GID:               2,
		IdentitySource:    "synthetic_test",
		PID:               3,
		ServiceIdentity:   "adapter-test",
		UID:               1,
		VerificationState: "verified",
	}
	if failure := ValidatePeer(peer, expected); failure != nil {
		t.Fatal(failure)
	}
	peer.VerificationState = "unverified"
	if failure := ValidatePeer(peer, expected); failure == nil || failure.Reason != protocol.ReasonIdentityMissing {
		t.Fatalf("expected identity_missing, got %v", failure)
	}
}

func TestTrustKeySetRejectsDuplicateAndRevokedKey(t *testing.T) {
	seed := bytes.Repeat([]byte{0x21}, ed25519.SeedSize)
	public := ed25519.NewKeyFromSeed(seed).Public().(ed25519.PublicKey)
	key := TrustKey{ID: "test-key", PublicKey: public, SignerIdentity: "test-signer"}
	if _, failure := NewTrustKeySet([]TrustKey{key, key}); failure == nil {
		t.Fatal("duplicate key unexpectedly accepted")
	}
	key.Revoked = true
	set, failure := NewTrustKeySet([]TrustKey{key})
	if failure != nil {
		t.Fatal(failure)
	}
	if !set.keys["test-key"].Revoked {
		t.Fatal("revocation state was not retained")
	}
}

func FuzzAuthorizationCanonicalContent(f *testing.F) {
	f.Add("TEST-AUTH-1", "adapter-test", "test-signer")
	f.Add("", "*", "\u0430dapter")
	f.Fuzz(func(t *testing.T, reference, identity, signer string) {
		auth := protocol.AuthorizationEnvelope{
			AdapterIdentity:        identity,
			AuthorizationReference: reference,
			SignerIdentity:         signer,
		}
		_, _ = AuthorizationDigest(auth)
		_, _ = SigningBytes(auth)
	})
}
