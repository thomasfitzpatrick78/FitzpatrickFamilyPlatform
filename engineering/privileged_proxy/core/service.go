package core

import (
	"context"
	"slices"
	"sync"
	"time"

	"fitzpatrickfamilyplatform/engineering/privileged_proxy/audit"
	"fitzpatrickfamilyplatform/engineering/privileged_proxy/authorization"
	"fitzpatrickfamilyplatform/engineering/privileged_proxy/policy"
	"fitzpatrickfamilyplatform/engineering/privileged_proxy/projection"
	"fitzpatrickfamilyplatform/engineering/privileged_proxy/protocol"
	"fitzpatrickfamilyplatform/engineering/privileged_proxy/replay"
	"fitzpatrickfamilyplatform/engineering/privileged_proxy/resource"
	"fitzpatrickfamilyplatform/engineering/privileged_proxy/target"
	"fitzpatrickfamilyplatform/engineering/privileged_proxy/upstream"
)

type Configuration struct {
	Admission    *resource.Admission
	Audit        audit.Sink
	Bindings     authorization.ExpectedBindings
	Keys         authorization.TrustKeySet
	Now          func() time.Time
	Observer     upstream.Observer
	Peer         authorization.PeerExpectation
	Policy       policy.Policy
	ProxyID      string
	ProxyVersion string
	Replay       replay.Journal
}

// Service is a transport-free policy core. It cannot listen, connect, discover
// peers, read environment configuration, or obtain provider authority.
type Service struct {
	config   Configuration
	disabled bool
	mutex    sync.Mutex
}

func New(configuration Configuration) (*Service, *protocol.Failure) {
	if configuration.Admission == nil || configuration.Audit == nil || configuration.Now == nil ||
		configuration.Observer == nil || configuration.Replay == nil ||
		configuration.ProxyID == "" || configuration.ProxyVersion == "" ||
		configuration.Policy.Digest() == "" {
		return nil, protocol.Fail(protocol.ReasonInternalFailClosed, "Core configuration is incomplete.")
	}
	for _, digest := range []string{
		configuration.Bindings.AdapterArtifactDigest,
		configuration.Bindings.ConfigurationDigest,
		configuration.Bindings.DeploymentBundleDigest,
		configuration.Bindings.PolicyDigest,
		configuration.Bindings.ProxyImplementationDigest,
		configuration.Bindings.RegistryRecordDigest,
		configuration.Bindings.TrustAnchorDigest,
		configuration.Bindings.TrustBindingDigest,
	} {
		if !protocol.ValidDigest(digest) {
			_ = configuration.Audit.Append(audit.Event{
				ConfigurationDigest:  configuration.Bindings.ConfigurationDigest,
				Decision:             "rejected",
				DeploymentDigest:     configuration.Bindings.DeploymentBundleDigest,
				EventType:            "configuration_rejected",
				EventVersion:         audit.EventVersion,
				ImplementationDigest: configuration.Bindings.ProxyImplementationDigest,
				Limitations:          []protocol.Limitation{},
				PolicyDigest:         configuration.Bindings.PolicyDigest,
				ReasonCode:           protocol.ReasonConfigurationDigestMismatch,
				Timestamp:            configuration.Now().UTC().Format(time.RFC3339Nano),
			})
			return nil, protocol.Fail(protocol.ReasonConfigurationDigestMismatch, protocol.SafeMessage(protocol.ReasonConfigurationDigestMismatch))
		}
	}
	if !protocol.ConstantDigestEqual(configuration.Policy.Digest(), configuration.Bindings.PolicyDigest) {
		if configuration.Audit != nil && configuration.Now != nil {
			_ = configuration.Audit.Append(audit.Event{
				ConfigurationDigest:  configuration.Bindings.ConfigurationDigest,
				Decision:             "rejected",
				DeploymentDigest:     configuration.Bindings.DeploymentBundleDigest,
				EventType:            "policy_rejected",
				EventVersion:         audit.EventVersion,
				ImplementationDigest: configuration.Bindings.ProxyImplementationDigest,
				Limitations:          []protocol.Limitation{},
				PolicyDigest:         configuration.Bindings.PolicyDigest,
				ReasonCode:           protocol.ReasonPolicyDigestMismatch,
				Timestamp:            configuration.Now().UTC().Format(time.RFC3339Nano),
			})
		}
		return nil, protocol.Fail(protocol.ReasonPolicyDigestMismatch, protocol.SafeMessage(protocol.ReasonPolicyDigestMismatch))
	}
	service := &Service{config: configuration}
	now := configuration.Now().UTC()
	for _, eventType := range []string{"core_initialization", "configuration_accepted", "policy_accepted"} {
		event := service.baseEvent(protocol.RequestEnvelope{}, now, eventType, "accepted", protocol.ReasonRequestCompleted)
		if failure := configuration.Audit.Append(event); failure != nil {
			return nil, failure
		}
	}
	return service, nil
}

// Handle applies the complete repository-only pipeline. The nonce is consumed
// after the security audit precondition succeeds and before admission or the
// typed synthetic upstream is invoked. It remains consumed on later failure.
func (service *Service) Handle(
	ctx context.Context,
	peer protocol.PeerContext,
	requestBytes []byte,
) ([]byte, error) {
	started := service.config.Now().UTC()
	if service.isDisabled() {
		return nil, protocol.Fail(protocol.ReasonInternalFailClosed, "Core is disabled.")
	}
	request, failure := protocol.DecodeRequest(requestBytes)
	if failure != nil {
		event := service.baseEvent(protocol.RequestEnvelope{}, started, "payload_rejected", "denied", failure.Reason)
		if auditFailure := service.config.Audit.Append(event); auditFailure != nil {
			service.disableWithoutAudit()
			return nil, auditFailure
		}
		return nil, failure
	}
	if failure = protocol.ValidateRequestShape(request); failure != nil {
		return service.fail(request, started, eventTypeFor(failure), failure, false)
	}
	if failure = authorization.ValidatePeer(peer, service.config.Peer); failure != nil {
		return service.fail(request, started, "peer_context_rejected", failure, false)
	}
	if failure = service.append(request, started, "peer_context_accepted", "accepted", protocol.ReasonRequestCompleted, nil); failure != nil {
		return service.auditFailureResponse(request, started, failure)
	}
	if failure = authorization.Verify(request, service.config.Keys, service.config.Bindings, started); failure != nil {
		return service.fail(request, started, "authorization_rejected", failure, false)
	}
	for _, eventType := range []string{"service_identity_accepted", "authorization_accepted", "digest_verification"} {
		if failure = service.append(request, started, eventType, "accepted", protocol.ReasonRequestCompleted, nil); failure != nil {
			return service.auditFailureResponse(request, started, failure)
		}
	}
	if failure = service.config.Policy.Evaluate(request.Operation); failure != nil {
		return service.fail(request, started, eventTypeFor(failure), failure, false)
	}
	derived, failure := target.Derive(request)
	if failure != nil {
		return service.fail(request, started, "target_mismatch", failure, false)
	}
	if failure = service.append(request, started, "request_accepted", "accepted", protocol.ReasonRequestCompleted, nil); failure != nil {
		return service.auditFailureResponse(request, started, failure)
	}
	expiresAt, _ := protocol.ParseUTC(request.Authorization.ValidUntil)
	if failure = service.config.Replay.CheckAndConsume(
		request.Authorization.AuthorizationReference,
		request.Authorization.Nonce,
		expiresAt,
		started,
	); failure != nil {
		eventType := "replay_rejected"
		if failure.Reason == protocol.ReasonReplayStateCorrupt || failure.Reason == protocol.ReasonReplayStateUnavailable {
			eventType = "replay_journal_failure"
		}
		return service.fail(request, started, eventType, failure, false)
	}
	if failure = service.append(request, started, "replay_accepted", "accepted", protocol.ReasonRequestCompleted, nil); failure != nil {
		return service.auditFailureResponse(request, started, failure)
	}
	release, failure := service.config.Admission.Acquire(peer.ServiceIdentity, derived.SubjectID, started)
	if failure != nil {
		return service.fail(request, started, eventTypeFor(failure), failure, false)
	}
	defer release()
	requestedAt, _ := protocol.ParseUTC(request.RequestedAt)
	deadline, _ := protocol.ParseUTC(request.Deadline)
	if _, failure = service.config.Admission.EvaluateTimeoutBudget(requestedAt, deadline, started); failure != nil {
		return service.fail(request, started, eventTypeFor(failure), failure, false)
	}
	select {
	case <-ctx.Done():
		return service.fail(
			request,
			started,
			"request_denied",
			protocol.Fail(protocol.ReasonRequestTimedOut, protocol.SafeMessage(protocol.ReasonRequestTimedOut)),
			false,
		)
	default:
	}
	if failure = service.append(request, started, "synthetic_upstream_invocation", "accepted", protocol.ReasonRequestCompleted, nil); failure != nil {
		return service.auditFailureResponse(request, started, failure)
	}
	observation, failure := upstream.Dispatch(ctx, service.config.Observer, request.Operation, derived)
	if failure != nil {
		return service.fail(request, started, "synthetic_upstream_failure", failure, true)
	}
	result, limitations, providerVersion, failure := projection.Project(request.Operation, derived, observation)
	if failure != nil {
		return service.fail(request, started, "response_rejected", failure, true)
	}
	limitations = addRequiredLimitations(limitations)
	completed := service.config.Now().UTC()
	response := service.response(request, started, completed, "allowed", protocol.ReasonRequestCompleted, &result, limitations, providerVersion)
	data, failure := protocol.EncodeCanonical(response, protocol.MaximumResponseBytes)
	if failure != nil {
		return service.fail(request, started, "response_rejected", failure, true)
	}
	if failure = service.append(request, started, "success", "allowed", protocol.ReasonRequestCompleted, limitations); failure != nil {
		return service.auditFailureResponse(request, started, failure)
	}
	return data, nil
}

func (service *Service) Disable(reason protocol.ReasonCode) *protocol.Failure {
	service.mutex.Lock()
	service.disabled = true
	service.mutex.Unlock()
	now := service.config.Now().UTC()
	event := service.baseEvent(protocol.RequestEnvelope{}, now, "disablement_state", "disabled", reason)
	return service.config.Audit.Append(event)
}

func (service *Service) EvaluateShutdown() *protocol.Failure {
	now := service.config.Now().UTC()
	event := service.baseEvent(protocol.RequestEnvelope{}, now, "shutdown_state_evaluation", "evaluated", protocol.ReasonRequestCompleted)
	return service.config.Audit.Append(event)
}

func (service *Service) fail(
	request protocol.RequestEnvelope,
	started time.Time,
	eventType string,
	failure *protocol.Failure,
	afterUpstream bool,
) ([]byte, error) {
	if auditFailure := service.append(request, started, eventType, decisionFor(failure.Reason), failure.Reason, nil); auditFailure != nil {
		return service.auditFailureResponse(request, started, auditFailure)
	}
	completed := service.config.Now().UTC()
	response := service.response(
		request,
		started,
		completed,
		decisionFor(failure.Reason),
		failure.Reason,
		nil,
		addRequiredLimitations(nil),
		"",
	)
	data, encodeFailure := protocol.EncodeCanonical(response, protocol.MaximumResponseBytes)
	if encodeFailure != nil {
		return nil, encodeFailure
	}
	if afterUpstream && failure.Reason == protocol.ReasonAuditUnavailable {
		service.disableWithoutAudit()
	}
	return data, nil
}

func (service *Service) auditFailureResponse(
	request protocol.RequestEnvelope,
	started time.Time,
	failure *protocol.Failure,
) ([]byte, error) {
	service.disableWithoutAudit()
	event := service.baseEvent(request, service.config.Now().UTC(), "audit_sink_failure", "failed", protocol.ReasonAuditUnavailable)
	_ = service.config.Audit.Append(event)
	response := service.response(
		request,
		started,
		service.config.Now().UTC(),
		"failed",
		protocol.ReasonAuditUnavailable,
		nil,
		addRequiredLimitations(nil),
		"",
	)
	data, _ := protocol.EncodeCanonical(response, protocol.MaximumResponseBytes)
	return data, failure
}

func (service *Service) response(
	request protocol.RequestEnvelope,
	started, completed time.Time,
	decision string,
	reason protocol.ReasonCode,
	result *protocol.ResultEnvelope,
	limitations []protocol.Limitation,
	providerVersion string,
) protocol.ResponseEnvelope {
	return protocol.ResponseEnvelope{
		AuditCorrelationID: auditCorrelationID(request),
		CompletedAt:        completed.Format(time.RFC3339Nano),
		CorrelationID:      request.CorrelationID,
		Decision:           decision,
		Limitations:        limitations,
		Operation:          request.Operation,
		ProtocolVersion:    protocol.ProtocolVersion,
		ProviderAPIVersion: providerVersion,
		ProxyIdentity: protocol.ProxyIdentity{
			ArtifactDigest:      service.config.Bindings.ProxyImplementationDigest,
			ConfigurationDigest: service.config.Bindings.ConfigurationDigest,
			ProxyID:             service.config.ProxyID,
			Version:             service.config.ProxyVersion,
		},
		ReasonCode:  reason,
		RequestID:   request.RequestID,
		Result:      result,
		SafeMessage: protocol.SafeMessage(reason),
		StartedAt:   started.Format(time.RFC3339Nano),
		TargetReference: protocol.ResponseTarget{
			HostReference: request.Target.HostReference,
			SubjectID:     request.Target.SubjectID,
		},
	}
}

func (service *Service) append(
	request protocol.RequestEnvelope,
	started time.Time,
	eventType, decision string,
	reason protocol.ReasonCode,
	limitations []protocol.Limitation,
) *protocol.Failure {
	event := service.baseEvent(request, service.config.Now().UTC(), eventType, decision, reason)
	event.LatencyMilliseconds = service.config.Now().UTC().Sub(started).Milliseconds()
	event.Limitations = slices.Clone(limitations)
	return service.config.Audit.Append(event)
}

func (service *Service) baseEvent(
	request protocol.RequestEnvelope,
	at time.Time,
	eventType, decision string,
	reason protocol.ReasonCode,
) audit.Event {
	category, _ := protocol.CategoryFor(request.Operation)
	return audit.Event{
		AuthorizationReference: request.Authorization.AuthorizationReference,
		Category:               category,
		ConfigurationDigest:    service.config.Bindings.ConfigurationDigest,
		CorrelationID:          request.CorrelationID,
		Decision:               decision,
		DeploymentDigest:       service.config.Bindings.DeploymentBundleDigest,
		EventType:              eventType,
		EventVersion:           audit.EventVersion,
		ImplementationDigest:   service.config.Bindings.ProxyImplementationDigest,
		Limitations:            []protocol.Limitation{},
		Operation:              request.Operation,
		PolicyDigest:           service.config.Bindings.PolicyDigest,
		ReasonCode:             reason,
		RequestID:              request.RequestID,
		ServiceIdentity:        request.Authorization.AdapterIdentity,
		SubjectReference:       request.Target.RegistryReference,
		TargetReference:        request.Target.SubjectID,
		Timestamp:              at.Format(time.RFC3339Nano),
	}
}

func (service *Service) isDisabled() bool {
	service.mutex.Lock()
	defer service.mutex.Unlock()
	return service.disabled
}

func (service *Service) disableWithoutAudit() {
	service.mutex.Lock()
	defer service.mutex.Unlock()
	service.disabled = true
}

func auditCorrelationID(request protocol.RequestEnvelope) string {
	digest := protocol.SHA256Digest([]byte(request.CorrelationID + "|" + request.RequestID))
	return digest[7:39]
}

func addRequiredLimitations(limitations []protocol.Limitation) []protocol.Limitation {
	result := append(slices.Clone(limitations),
		protocol.LimitationFixtureOnly,
		protocol.LimitationNoTransport,
		protocol.LimitationOneShot,
		protocol.LimitationSynthetic,
	)
	slices.Sort(result)
	return slices.Compact(result)
}

func decisionFor(reason protocol.ReasonCode) string {
	switch reason {
	case protocol.ReasonProviderUnavailable,
		protocol.ReasonUpstreamTimedOut,
		protocol.ReasonResponseMalformed,
		protocol.ReasonResponseOversized,
		protocol.ReasonResponseFieldRejected,
		protocol.ReasonRecordLimitExceeded,
		protocol.ReasonAuditUnavailable,
		protocol.ReasonInternalFailClosed:
		return "failed"
	default:
		return "denied"
	}
}

func eventTypeFor(failure *protocol.Failure) string {
	switch failure.Reason {
	case protocol.ReasonCategoryDenied:
		return "category_denial"
	case protocol.ReasonOperationDenied:
		return "operation_denial"
	case protocol.ReasonTargetMismatch, protocol.ReasonTargetInvalid, protocol.ReasonWildcardDenied:
		return "target_mismatch"
	case protocol.ReasonProtocolUnsupported:
		return "version_mismatch"
	case protocol.ReasonRequestOversized:
		return "payload_rejection"
	default:
		return "request_denied"
	}
}
