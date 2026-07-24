package target

import "fitzpatrickfamilyplatform/engineering/privileged_proxy/protocol"

// Derived is the exact, already-authorized selector passed to typed synthetic
// observation methods. It contains no provider path, method, query, or body.
type Derived struct {
	ComposeProject      string
	ComposeService      string
	GovernedRuntimeName string
	HostReference       string
	RegistryDigest      string
	RegistryReference   string
	SelectorKind        string
	SubjectID           string
}

func Derive(request protocol.RequestEnvelope) (Derived, *protocol.Failure) {
	if failure := protocol.ValidateTarget(request.Target); failure != nil {
		return Derived{}, failure
	}
	auth := request.Authorization
	target := request.Target
	if target.SubjectID != auth.SubjectID || target.HostReference != auth.HostReference ||
		!protocol.ConstantDigestEqual(target.RegistryRecordDigest, auth.RegistryRecordDigest) ||
		target.SelectorKind != auth.SelectorKind ||
		target.ComposeProject != auth.ComposeProject ||
		target.ComposeService != auth.ComposeService ||
		target.GovernedRuntimeName != auth.GovernedRuntimeName {
		return Derived{}, protocol.Fail(protocol.ReasonTargetMismatch, protocol.SafeMessage(protocol.ReasonTargetMismatch))
	}
	return Derived{
		ComposeProject:      target.ComposeProject,
		ComposeService:      target.ComposeService,
		GovernedRuntimeName: target.GovernedRuntimeName,
		HostReference:       target.HostReference,
		RegistryDigest:      target.RegistryRecordDigest,
		RegistryReference:   target.RegistryReference,
		SelectorKind:        target.SelectorKind,
		SubjectID:           target.SubjectID,
	}, nil
}
