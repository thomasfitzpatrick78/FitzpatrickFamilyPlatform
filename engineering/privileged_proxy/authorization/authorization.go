package authorization

import (
	"crypto/ed25519"
	"encoding/base64"
	"regexp"
	"slices"
	"time"

	"fitzpatrickfamilyplatform/engineering/privileged_proxy/protocol"
)

const (
	Algorithm        = "Ed25519"
	MaximumLifetime  = 15 * time.Minute
	MaximumClockSkew = 30 * time.Second
)

var (
	noncePattern     = regexp.MustCompile(`^[0-9a-f]{64}$`)
	referencePattern = regexp.MustCompile(`^[A-Za-z0-9][A-Za-z0-9._:/-]{0,127}$`)
)

type TrustKey struct {
	ID             string
	PublicKey      ed25519.PublicKey
	Revoked        bool
	SignerIdentity string
}

type TrustKeySet struct {
	keys map[string]TrustKey
}

func NewTrustKeySet(keys []TrustKey) (TrustKeySet, *protocol.Failure) {
	result := TrustKeySet{keys: make(map[string]TrustKey, len(keys))}
	if len(keys) == 0 || len(keys) > 16 {
		return TrustKeySet{}, protocol.Fail(protocol.ReasonUnknownKey, "Trust-key set is empty or oversized.")
	}
	for _, key := range keys {
		if !referencePattern.MatchString(key.ID) || !referencePattern.MatchString(key.SignerIdentity) ||
			len(key.PublicKey) != ed25519.PublicKeySize {
			return TrustKeySet{}, protocol.Fail(protocol.ReasonUnknownKey, "Trust key metadata is invalid.")
		}
		if _, exists := result.keys[key.ID]; exists {
			return TrustKeySet{}, protocol.Fail(protocol.ReasonUnknownKey, "Trust key identifier is duplicated.")
		}
		key.PublicKey = slices.Clone(key.PublicKey)
		result.keys[key.ID] = key
	}
	return result, nil
}

type ExpectedBindings struct {
	AdapterArtifactDigest     string
	AdapterIdentity           string
	ConfigurationDigest       string
	DeploymentBundleDigest    string
	PolicyDigest              string
	ProxyImplementationDigest string
	RegistryRecordDigest      string
	TrustAnchorDigest         string
	TrustBindingDigest        string
}

type PeerExpectation struct {
	GID             uint32
	ServiceIdentity string
	UID             uint32
}

func ValidatePeer(peer protocol.PeerContext, expected PeerExpectation) *protocol.Failure {
	if peer.VerificationState != "verified" || peer.IdentitySource == "" {
		return protocol.Fail(protocol.ReasonIdentityMissing, protocol.SafeMessage(protocol.ReasonIdentityMissing))
	}
	if peer.UID != expected.UID || peer.GID != expected.GID || peer.PID <= 0 ||
		peer.ServiceIdentity != expected.ServiceIdentity {
		return protocol.Fail(protocol.ReasonIdentityMismatch, protocol.SafeMessage(protocol.ReasonIdentityMismatch))
	}
	return nil
}

// Verify validates the detached Ed25519 authorization and every request binding.
// Peer validation is deliberately separate: peer context is necessary but never
// complete request authorization.
func Verify(
	request protocol.RequestEnvelope,
	keys TrustKeySet,
	expected ExpectedBindings,
	now time.Time,
) *protocol.Failure {
	auth := request.Authorization
	if auth.AuthorizationVersion == "" || auth.Signature == "" {
		return protocol.Fail(protocol.ReasonAuthorizationMissing, protocol.SafeMessage(protocol.ReasonAuthorizationMissing))
	}
	if auth.AuthorizationVersion != protocol.AuthorizationVersion || auth.Algorithm != Algorithm ||
		!referencePattern.MatchString(auth.AuthorizationReference) ||
		!referencePattern.MatchString(auth.ApprovalReference) ||
		!referencePattern.MatchString(auth.AdapterIdentity) ||
		!referencePattern.MatchString(auth.KeyID) ||
		!referencePattern.MatchString(auth.SignerIdentity) ||
		auth.MaxAttempts != 1 ||
		!noncePattern.MatchString(auth.Nonce) {
		return protocol.Fail(protocol.ReasonAuthorizationInvalid, protocol.SafeMessage(protocol.ReasonAuthorizationInvalid))
	}
	if failure := validateScope(request); failure != nil {
		return failure
	}
	if failure := validateTargetBindings(request); failure != nil {
		return failure
	}
	if failure := validateDigestBindings(request, expected); failure != nil {
		return failure
	}
	validFrom, failure := protocol.ParseUTC(auth.ValidFrom)
	if failure != nil {
		return protocol.Fail(protocol.ReasonAuthorizationInvalid, "Authorization validity window is invalid.")
	}
	validUntil, failure := protocol.ParseUTC(auth.ValidUntil)
	if failure != nil || !validUntil.After(validFrom) || validUntil.Sub(validFrom) > MaximumLifetime {
		return protocol.Fail(protocol.ReasonAuthorizationLifetime, "Authorization lifetime exceeds the governed maximum.")
	}
	requestedAt, _ := protocol.ParseUTC(request.RequestedAt)
	if requestedAt.Before(validFrom.Add(-MaximumClockSkew)) || now.Before(validFrom.Add(-MaximumClockSkew)) {
		return protocol.Fail(protocol.ReasonAuthorizationFuture, protocol.SafeMessage(protocol.ReasonAuthorizationFuture))
	}
	if requestedAt.After(validUntil) || now.After(validUntil.Add(MaximumClockSkew)) {
		return protocol.Fail(protocol.ReasonAuthorizationExpired, protocol.SafeMessage(protocol.ReasonAuthorizationExpired))
	}
	key, exists := keys.keys[auth.KeyID]
	if !exists || key.Revoked {
		return protocol.Fail(protocol.ReasonUnknownKey, protocol.SafeMessage(protocol.ReasonUnknownKey))
	}
	if key.SignerIdentity != auth.SignerIdentity {
		return protocol.Fail(protocol.ReasonIdentityMismatch, protocol.SafeMessage(protocol.ReasonIdentityMismatch))
	}
	if !protocol.ConstantDigestEqual(protocol.SHA256Digest(key.PublicKey), auth.TrustAnchorDigest) {
		return protocol.Fail(protocol.ReasonTrustAnchorMismatch, protocol.SafeMessage(protocol.ReasonTrustAnchorMismatch))
	}
	digest, digestFailure := AuthorizationDigest(auth)
	if digestFailure != nil || !protocol.ConstantDigestEqual(digest, auth.AuthorizationDigest) {
		return protocol.Fail(protocol.ReasonAuthorizationInvalid, protocol.SafeMessage(protocol.ReasonAuthorizationInvalid))
	}
	signature, decodeErr := base64.RawURLEncoding.DecodeString(auth.Signature)
	if decodeErr != nil || len(signature) != ed25519.SignatureSize {
		return protocol.Fail(protocol.ReasonSignatureInvalid, protocol.SafeMessage(protocol.ReasonSignatureInvalid))
	}
	signingBytes, signingFailure := SigningBytes(auth)
	if signingFailure != nil || !ed25519.Verify(key.PublicKey, signingBytes, signature) {
		return protocol.Fail(protocol.ReasonSignatureInvalid, protocol.SafeMessage(protocol.ReasonSignatureInvalid))
	}
	return nil
}

func AuthorizationDigest(auth protocol.AuthorizationEnvelope) (string, *protocol.Failure) {
	content := digestContent{
		AdapterArtifactDigest:     auth.AdapterArtifactDigest,
		AdapterIdentity:           auth.AdapterIdentity,
		Algorithm:                 auth.Algorithm,
		AllowedOperations:         auth.AllowedOperations,
		AllowedSignals:            auth.AllowedSignals,
		ApprovalReference:         auth.ApprovalReference,
		AuthorizationReference:    auth.AuthorizationReference,
		AuthorizationVersion:      auth.AuthorizationVersion,
		ComposeProject:            auth.ComposeProject,
		ComposeService:            auth.ComposeService,
		ConfigurationDigest:       auth.ConfigurationDigest,
		CorrelationID:             auth.CorrelationID,
		DeploymentBundleDigest:    auth.DeploymentBundleDigest,
		GovernedRuntimeName:       auth.GovernedRuntimeName,
		HostReference:             auth.HostReference,
		KeyID:                     auth.KeyID,
		MaxAttempts:               auth.MaxAttempts,
		Nonce:                     auth.Nonce,
		PolicyDigest:              auth.PolicyDigest,
		ProxyImplementationDigest: auth.ProxyImplementationDigest,
		RegistryRecordDigest:      auth.RegistryRecordDigest,
		SelectorKind:              auth.SelectorKind,
		SignerIdentity:            auth.SignerIdentity,
		SubjectID:                 auth.SubjectID,
		TrustAnchorDigest:         auth.TrustAnchorDigest,
		TrustBindingDigest:        auth.TrustBindingDigest,
		ValidFrom:                 auth.ValidFrom,
		ValidUntil:                auth.ValidUntil,
	}
	data, failure := protocol.EncodeCanonical(content, protocol.MaximumRequestBytes)
	if failure != nil {
		return "", failure
	}
	return protocol.SHA256Digest(data), nil
}

func SigningBytes(auth protocol.AuthorizationEnvelope) ([]byte, *protocol.Failure) {
	content := signingContent{
		AdapterArtifactDigest:     auth.AdapterArtifactDigest,
		AdapterIdentity:           auth.AdapterIdentity,
		Algorithm:                 auth.Algorithm,
		AllowedOperations:         auth.AllowedOperations,
		AllowedSignals:            auth.AllowedSignals,
		ApprovalReference:         auth.ApprovalReference,
		AuthorizationDigest:       auth.AuthorizationDigest,
		AuthorizationReference:    auth.AuthorizationReference,
		AuthorizationVersion:      auth.AuthorizationVersion,
		ComposeProject:            auth.ComposeProject,
		ComposeService:            auth.ComposeService,
		ConfigurationDigest:       auth.ConfigurationDigest,
		CorrelationID:             auth.CorrelationID,
		DeploymentBundleDigest:    auth.DeploymentBundleDigest,
		GovernedRuntimeName:       auth.GovernedRuntimeName,
		HostReference:             auth.HostReference,
		KeyID:                     auth.KeyID,
		MaxAttempts:               auth.MaxAttempts,
		Nonce:                     auth.Nonce,
		PolicyDigest:              auth.PolicyDigest,
		ProxyImplementationDigest: auth.ProxyImplementationDigest,
		RegistryRecordDigest:      auth.RegistryRecordDigest,
		SelectorKind:              auth.SelectorKind,
		SignerIdentity:            auth.SignerIdentity,
		SubjectID:                 auth.SubjectID,
		TrustAnchorDigest:         auth.TrustAnchorDigest,
		TrustBindingDigest:        auth.TrustBindingDigest,
		ValidFrom:                 auth.ValidFrom,
		ValidUntil:                auth.ValidUntil,
	}
	return protocol.EncodeCanonical(content, protocol.MaximumRequestBytes)
}

func validateScope(request protocol.RequestEnvelope) *protocol.Failure {
	auth := request.Authorization
	if len(auth.AllowedOperations) == 0 || len(auth.AllowedOperations) > 8 ||
		!slices.IsSorted(auth.AllowedOperations) || hasDuplicateOperations(auth.AllowedOperations) ||
		!slices.Contains(auth.AllowedOperations, request.Operation) {
		return protocol.Fail(protocol.ReasonOperationDenied, protocol.SafeMessage(protocol.ReasonOperationDenied))
	}
	if len(auth.AllowedSignals) == 0 || len(auth.AllowedSignals) > 16 ||
		!slices.IsSorted(auth.AllowedSignals) || hasDuplicateStrings(auth.AllowedSignals) {
		return protocol.Fail(protocol.ReasonSignalDenied, protocol.SafeMessage(protocol.ReasonSignalDenied))
	}
	for _, signal := range request.RequestedSignals {
		if !slices.Contains(auth.AllowedSignals, signal) {
			return protocol.Fail(protocol.ReasonSignalDenied, protocol.SafeMessage(protocol.ReasonSignalDenied))
		}
	}
	if auth.CorrelationID != request.CorrelationID {
		return protocol.Fail(protocol.ReasonAuthorizationInvalid, protocol.SafeMessage(protocol.ReasonAuthorizationInvalid))
	}
	return nil
}

func validateTargetBindings(request protocol.RequestEnvelope) *protocol.Failure {
	auth := request.Authorization
	target := request.Target
	if auth.SubjectID != target.SubjectID || auth.HostReference != target.HostReference ||
		!protocol.ConstantDigestEqual(auth.RegistryRecordDigest, target.RegistryRecordDigest) ||
		auth.SelectorKind != target.SelectorKind ||
		auth.ComposeProject != target.ComposeProject ||
		auth.ComposeService != target.ComposeService ||
		auth.GovernedRuntimeName != target.GovernedRuntimeName {
		return protocol.Fail(protocol.ReasonTargetMismatch, protocol.SafeMessage(protocol.ReasonTargetMismatch))
	}
	return nil
}

func validateDigestBindings(request protocol.RequestEnvelope, expected ExpectedBindings) *protocol.Failure {
	checks := []struct {
		actual   string
		envelope string
		expected string
		reason   protocol.ReasonCode
	}{
		{request.Authorization.PolicyDigest, request.PolicyDigest, expected.PolicyDigest, protocol.ReasonPolicyDigestMismatch},
		{request.Authorization.ConfigurationDigest, request.ConfigurationDigest, expected.ConfigurationDigest, protocol.ReasonConfigurationDigestMismatch},
		{request.Authorization.DeploymentBundleDigest, request.DeploymentBundleDigest, expected.DeploymentBundleDigest, protocol.ReasonDeploymentDigestMismatch},
		{request.Authorization.AdapterArtifactDigest, request.AdapterArtifactDigest, expected.AdapterArtifactDigest, protocol.ReasonAdapterDigestMismatch},
		{request.Authorization.ProxyImplementationDigest, request.ProxyImplementationDigest, expected.ProxyImplementationDigest, protocol.ReasonProxyDigestMismatch},
		{request.Authorization.TrustBindingDigest, request.TrustBindingDigest, expected.TrustBindingDigest, protocol.ReasonTrustBindingDigestMismatch},
	}
	for _, check := range checks {
		if !protocol.ConstantDigestEqual(check.actual, check.envelope) ||
			!protocol.ConstantDigestEqual(check.actual, check.expected) {
			return protocol.Fail(check.reason, protocol.SafeMessage(check.reason))
		}
	}
	if request.Authorization.AdapterIdentity != expected.AdapterIdentity {
		return protocol.Fail(protocol.ReasonIdentityMismatch, protocol.SafeMessage(protocol.ReasonIdentityMismatch))
	}
	if !protocol.ConstantDigestEqual(request.Authorization.RegistryRecordDigest, request.Target.RegistryRecordDigest) {
		return protocol.Fail(protocol.ReasonRegistryDigestMismatch, protocol.SafeMessage(protocol.ReasonRegistryDigestMismatch))
	}
	if !protocol.ConstantDigestEqual(request.Authorization.RegistryRecordDigest, expected.RegistryRecordDigest) {
		return protocol.Fail(protocol.ReasonRegistryDigestMismatch, protocol.SafeMessage(protocol.ReasonRegistryDigestMismatch))
	}
	if !protocol.ConstantDigestEqual(request.Authorization.TrustAnchorDigest, expected.TrustAnchorDigest) {
		return protocol.Fail(protocol.ReasonTrustAnchorMismatch, protocol.SafeMessage(protocol.ReasonTrustAnchorMismatch))
	}
	return nil
}

func hasDuplicateOperations(values []protocol.Operation) bool {
	for index := 1; index < len(values); index++ {
		if values[index] == values[index-1] {
			return true
		}
	}
	return false
}

func hasDuplicateStrings(values []string) bool {
	for index := 1; index < len(values); index++ {
		if values[index] == values[index-1] {
			return true
		}
	}
	return false
}

type digestContent struct {
	AdapterArtifactDigest     string               `json:"adapter_artifact_digest"`
	AdapterIdentity           string               `json:"adapter_identity"`
	Algorithm                 string               `json:"algorithm"`
	AllowedOperations         []protocol.Operation `json:"allowed_operations"`
	AllowedSignals            []string             `json:"allowed_signals"`
	ApprovalReference         string               `json:"approval_reference"`
	AuthorizationReference    string               `json:"authorization_reference"`
	AuthorizationVersion      string               `json:"authorization_version"`
	ComposeProject            string               `json:"compose_project"`
	ComposeService            string               `json:"compose_service"`
	ConfigurationDigest       string               `json:"configuration_digest"`
	CorrelationID             string               `json:"correlation_id"`
	DeploymentBundleDigest    string               `json:"deployment_bundle_digest"`
	GovernedRuntimeName       string               `json:"governed_runtime_name"`
	HostReference             string               `json:"host_reference"`
	KeyID                     string               `json:"key_id"`
	MaxAttempts               int                  `json:"max_attempts"`
	Nonce                     string               `json:"nonce"`
	PolicyDigest              string               `json:"policy_digest"`
	ProxyImplementationDigest string               `json:"proxy_implementation_digest"`
	RegistryRecordDigest      string               `json:"registry_record_digest"`
	SelectorKind              string               `json:"selector_kind"`
	SignerIdentity            string               `json:"signer_identity"`
	SubjectID                 string               `json:"subject_id"`
	TrustAnchorDigest         string               `json:"trust_anchor_digest"`
	TrustBindingDigest        string               `json:"trust_binding_digest"`
	ValidFrom                 string               `json:"valid_from"`
	ValidUntil                string               `json:"valid_until"`
}

type signingContent struct {
	AdapterArtifactDigest     string               `json:"adapter_artifact_digest"`
	AdapterIdentity           string               `json:"adapter_identity"`
	Algorithm                 string               `json:"algorithm"`
	AllowedOperations         []protocol.Operation `json:"allowed_operations"`
	AllowedSignals            []string             `json:"allowed_signals"`
	ApprovalReference         string               `json:"approval_reference"`
	AuthorizationDigest       string               `json:"authorization_digest"`
	AuthorizationReference    string               `json:"authorization_reference"`
	AuthorizationVersion      string               `json:"authorization_version"`
	ComposeProject            string               `json:"compose_project"`
	ComposeService            string               `json:"compose_service"`
	ConfigurationDigest       string               `json:"configuration_digest"`
	CorrelationID             string               `json:"correlation_id"`
	DeploymentBundleDigest    string               `json:"deployment_bundle_digest"`
	GovernedRuntimeName       string               `json:"governed_runtime_name"`
	HostReference             string               `json:"host_reference"`
	KeyID                     string               `json:"key_id"`
	MaxAttempts               int                  `json:"max_attempts"`
	Nonce                     string               `json:"nonce"`
	PolicyDigest              string               `json:"policy_digest"`
	ProxyImplementationDigest string               `json:"proxy_implementation_digest"`
	RegistryRecordDigest      string               `json:"registry_record_digest"`
	SelectorKind              string               `json:"selector_kind"`
	SignerIdentity            string               `json:"signer_identity"`
	SubjectID                 string               `json:"subject_id"`
	TrustAnchorDigest         string               `json:"trust_anchor_digest"`
	TrustBindingDigest        string               `json:"trust_binding_digest"`
	ValidFrom                 string               `json:"valid_from"`
	ValidUntil                string               `json:"valid_until"`
}
