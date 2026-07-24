package protocol

import (
	"crypto/sha256"
	"encoding/hex"
	"regexp"
	"slices"
	"strings"
	"time"
)

var (
	hexID        = regexp.MustCompile(`^[0-9a-f]{16,64}$`)
	lowerHex64   = regexp.MustCompile(`^[0-9a-f]{64}$`)
	safeExact    = regexp.MustCompile(`^[A-Za-z0-9][A-Za-z0-9._:/-]{0,127}$`)
	safeSelector = regexp.MustCompile(`^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$`)
)

func CategoryFor(operation Operation) (Category, bool) {
	switch operation {
	case ResolveTargetIdentity:
		return IdentityDiscovery, true
	case ObserveLifecycle:
		return LifecycleObservation, true
	case ObserveHealth:
		return HealthObservation, true
	case ObserveRestartInformation:
		return RestartInformation, true
	case ObserveStatisticsOnce:
		return Statistics, true
	case CheckProviderCompatibility:
		return System, true
	default:
		return "", false
	}
}

func AllowedSignals(operation Operation) []string {
	switch operation {
	case ResolveTargetIdentity:
		return []string{"container.identity"}
	case ObserveLifecycle:
		return []string{"container.lifecycle.observed_state"}
	case ObserveHealth:
		return []string{"container.healthcheck.state"}
	case ObserveRestartInformation:
		return []string{"container.restart.count", "container.restart.occurred"}
	case ObserveStatisticsOnce:
		return []string{
			"container.cpu.online_count",
			"container.cpu.system_usage",
			"container.cpu.total_usage",
			"container.memory.cache_basis",
			"container.memory.limit",
			"container.memory.usage",
			"container.pids.current",
		}
	default:
		return nil
	}
}

func ValidateRequestShape(request RequestEnvelope) *Failure {
	if request.ProtocolVersion != ProtocolVersion {
		return Fail(ReasonProtocolUnsupported, SafeMessage(ReasonProtocolUnsupported))
	}
	if !hexID.MatchString(request.RequestID) || !hexID.MatchString(request.CorrelationID) {
		return Fail(ReasonRequestMalformed, "Request and correlation identifiers are invalid.")
	}
	category, known := CategoryFor(request.Operation)
	if !known || category == System {
		return Fail(ReasonOperationDenied, SafeMessage(ReasonOperationDenied))
	}
	requestedAt, failure := parseUTC(request.RequestedAt, ReasonDeadlineInvalid)
	if failure != nil {
		return failure
	}
	deadline, failure := parseUTC(request.Deadline, ReasonDeadlineInvalid)
	if failure != nil || deadline.Before(requestedAt) || deadline.Sub(requestedAt) > 10*time.Second {
		return Fail(ReasonDeadlineInvalid, "Request deadline is outside the governed budget.")
	}
	if failure := ValidateTarget(request.Target); failure != nil {
		return failure
	}
	if len(request.RequestedSignals) == 0 || len(request.RequestedSignals) > 16 ||
		!slices.IsSorted(request.RequestedSignals) || hasDuplicates(request.RequestedSignals) {
		return Fail(ReasonSignalDenied, SafeMessage(ReasonSignalDenied))
	}
	allowed := AllowedSignals(request.Operation)
	for _, signal := range request.RequestedSignals {
		if !slices.Contains(allowed, signal) {
			return Fail(ReasonSignalDenied, SafeMessage(ReasonSignalDenied))
		}
	}
	for _, digest := range []string{
		request.AdapterArtifactDigest,
		request.ConfigurationDigest,
		request.DeploymentBundleDigest,
		request.PolicyDigest,
		request.ProxyImplementationDigest,
		request.Target.RegistryRecordDigest,
		request.TrustBindingDigest,
	} {
		if !ValidDigest(digest) {
			return Fail(ReasonAuthorizationInvalid, "A required digest is malformed.")
		}
	}
	return nil
}

func ValidateTarget(target TargetReference) *Failure {
	for _, value := range []string{target.SubjectID, target.RegistryReference, target.HostReference} {
		if !safeExact.MatchString(value) {
			if strings.ContainsAny(value, "*?[]") {
				return Fail(ReasonWildcardDenied, SafeMessage(ReasonWildcardDenied))
			}
			return Fail(ReasonTargetInvalid, SafeMessage(ReasonTargetInvalid))
		}
	}
	if !ValidDigest(target.RegistryRecordDigest) {
		return Fail(ReasonTargetInvalid, SafeMessage(ReasonTargetInvalid))
	}
	switch target.SelectorKind {
	case "compose_identity":
		if !safeSelector.MatchString(target.ComposeProject) || !safeSelector.MatchString(target.ComposeService) ||
			target.GovernedRuntimeName != "" {
			return Fail(ReasonTargetInvalid, SafeMessage(ReasonTargetInvalid))
		}
	case "governed_runtime_name":
		if !safeSelector.MatchString(target.GovernedRuntimeName) || target.ComposeProject != "" || target.ComposeService != "" {
			return Fail(ReasonTargetInvalid, SafeMessage(ReasonTargetInvalid))
		}
	default:
		return Fail(ReasonTargetInvalid, SafeMessage(ReasonTargetInvalid))
	}
	if target.ExpectedImageDigest != "" && !ValidDigest(target.ExpectedImageDigest) {
		return Fail(ReasonTargetInvalid, SafeMessage(ReasonTargetInvalid))
	}
	if target.ExpectedImageReference != "" && !safeExact.MatchString(target.ExpectedImageReference) {
		return Fail(ReasonTargetInvalid, SafeMessage(ReasonTargetInvalid))
	}
	return nil
}

func ValidDigest(value string) bool {
	return len(value) == 71 && strings.HasPrefix(value, "sha256:") && lowerHex64.MatchString(value[7:])
}

func SHA256Digest(data []byte) string {
	sum := sha256.Sum256(data)
	return "sha256:" + hex.EncodeToString(sum[:])
}

func ConstantDigestEqual(left, right string) bool {
	if !ValidDigest(left) || !ValidDigest(right) {
		return false
	}
	leftBytes, _ := hex.DecodeString(left[7:])
	rightBytes, _ := hex.DecodeString(right[7:])
	return stringHashEqual(leftBytes, rightBytes)
}

func stringHashEqual(left, right []byte) bool {
	if len(left) != len(right) {
		return false
	}
	var difference byte
	for index := range left {
		difference |= left[index] ^ right[index]
	}
	return difference == 0
}

func hasDuplicates(values []string) bool {
	for index := 1; index < len(values); index++ {
		if values[index] == values[index-1] {
			return true
		}
	}
	return false
}

func ParseUTC(value string) (time.Time, *Failure) {
	return parseUTC(value, ReasonAuthorizationInvalid)
}

func parseUTC(value string, reason ReasonCode) (time.Time, *Failure) {
	parsed, err := time.Parse(time.RFC3339Nano, value)
	if err != nil || parsed.Location() != time.UTC || !strings.HasSuffix(value, "Z") {
		return time.Time{}, Fail(reason, "Timestamp must be canonical UTC.")
	}
	return parsed, nil
}
