package protocol

// ReasonCode is a stable, non-secret outcome identifier from protocol v1.
type ReasonCode string

const (
	ReasonAdapterDigestMismatch       ReasonCode = "adapter_digest_mismatch"
	ReasonAuditUnavailable            ReasonCode = "audit_unavailable"
	ReasonAuthorizationExpired        ReasonCode = "authorization_expired"
	ReasonAuthorizationFuture         ReasonCode = "authorization_future"
	ReasonAuthorizationInvalid        ReasonCode = "authorization_invalid"
	ReasonAuthorizationLifetime       ReasonCode = "authorization_lifetime_exceeded"
	ReasonAuthorizationMissing        ReasonCode = "authorization_missing"
	ReasonAuthorizationReplayed       ReasonCode = "authorization_replayed"
	ReasonCategoryDenied              ReasonCode = "category_denied"
	ReasonConcurrencyExhausted        ReasonCode = "concurrency_exhausted"
	ReasonConfigurationDigestMismatch ReasonCode = "configuration_digest_mismatch"
	ReasonDeadlineInvalid             ReasonCode = "deadline_invalid"
	ReasonDeploymentDigestMismatch    ReasonCode = "deployment_digest_mismatch"
	ReasonDuplicateField              ReasonCode = "duplicate_field"
	ReasonIdentityMismatch            ReasonCode = "identity_mismatch"
	ReasonIdentityMissing             ReasonCode = "identity_missing"
	ReasonInternalFailClosed          ReasonCode = "internal_fail_closed"
	ReasonOperationDenied             ReasonCode = "operation_denied"
	ReasonPolicyDigestMismatch        ReasonCode = "policy_digest_mismatch"
	ReasonProtocolUnsupported         ReasonCode = "protocol_unsupported"
	ReasonProviderUnavailable         ReasonCode = "provider_unavailable"
	ReasonProxyDigestMismatch         ReasonCode = "proxy_digest_mismatch"
	ReasonRateLimited                 ReasonCode = "rate_limited"
	ReasonRecordLimitExceeded         ReasonCode = "record_limit_exceeded"
	ReasonRegistryDigestMismatch      ReasonCode = "registry_digest_mismatch"
	ReasonReplayStateCorrupt          ReasonCode = "replay_state_corrupt"
	ReasonReplayStateUnavailable      ReasonCode = "replay_state_unavailable"
	ReasonRequestCompleted            ReasonCode = "request_completed"
	ReasonRequestMalformed            ReasonCode = "request_malformed"
	ReasonRequestOversized            ReasonCode = "request_oversized"
	ReasonRequestTimedOut             ReasonCode = "request_timed_out"
	ReasonResponseFieldRejected       ReasonCode = "response_field_rejected"
	ReasonResponseMalformed           ReasonCode = "response_malformed"
	ReasonResponseOversized           ReasonCode = "response_oversized"
	ReasonSignalDenied                ReasonCode = "signal_denied"
	ReasonSignatureInvalid            ReasonCode = "signature_invalid"
	ReasonTargetAbsent                ReasonCode = "target_absent"
	ReasonTargetAmbiguous             ReasonCode = "target_ambiguous"
	ReasonTargetConflicting           ReasonCode = "target_conflicting"
	ReasonTargetDuplicate             ReasonCode = "target_duplicate"
	ReasonTargetInvalid               ReasonCode = "target_invalid"
	ReasonTargetMismatch              ReasonCode = "target_mismatch"
	ReasonTrustAnchorMismatch         ReasonCode = "trust_anchor_mismatch"
	ReasonTrustBindingDigestMismatch  ReasonCode = "trust_binding_digest_mismatch"
	ReasonUnknownField                ReasonCode = "unknown_field"
	ReasonUnknownKey                  ReasonCode = "unknown_key"
	ReasonUpstreamTimedOut            ReasonCode = "upstream_timed_out"
	ReasonWildcardDenied              ReasonCode = "wildcard_denied"
)

// Failure is the internal typed failure used throughout the transport-free core.
type Failure struct {
	Reason  ReasonCode
	Message string
}

func (f *Failure) Error() string {
	return string(f.Reason) + ": " + f.Message
}

func Fail(reason ReasonCode, message string) *Failure {
	return &Failure{Reason: reason, Message: message}
}

func SafeMessage(reason ReasonCode) string {
	switch reason {
	case ReasonRequestCompleted:
		return "Request completed."
	case ReasonRequestMalformed, ReasonDuplicateField, ReasonUnknownField:
		return "Request encoding is invalid."
	case ReasonRequestOversized:
		return "Request exceeds the governed size limit."
	case ReasonProtocolUnsupported:
		return "Protocol version is unsupported."
	case ReasonIdentityMissing, ReasonIdentityMismatch:
		return "Peer identity is not authorized."
	case ReasonSignatureInvalid, ReasonUnknownKey, ReasonAuthorizationInvalid, ReasonAuthorizationMissing:
		return "Authorization is invalid."
	case ReasonAuthorizationExpired:
		return "Authorization has expired."
	case ReasonAuthorizationFuture:
		return "Authorization is not yet valid."
	case ReasonAuthorizationReplayed:
		return "Authorization has already been consumed."
	case ReasonOperationDenied, ReasonCategoryDenied:
		return "Operation is denied."
	case ReasonSignalDenied:
		return "Requested signal is denied."
	case ReasonTargetInvalid, ReasonTargetMismatch, ReasonWildcardDenied:
		return "Target is invalid."
	case ReasonTargetAbsent, ReasonTargetDuplicate, ReasonTargetAmbiguous, ReasonTargetConflicting:
		return "Exact target resolution failed."
	case ReasonRateLimited, ReasonConcurrencyExhausted:
		return "Request capacity is unavailable."
	case ReasonProviderUnavailable, ReasonUpstreamTimedOut:
		return "Provider observation is unavailable."
	case ReasonResponseMalformed, ReasonResponseOversized, ReasonResponseFieldRejected, ReasonRecordLimitExceeded:
		return "Provider response was rejected."
	case ReasonAuditUnavailable, ReasonReplayStateCorrupt, ReasonReplayStateUnavailable:
		return "Required security state is unavailable."
	default:
		return "Request failed closed."
	}
}
