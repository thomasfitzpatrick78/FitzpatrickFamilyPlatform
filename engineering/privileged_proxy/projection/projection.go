package projection

import (
	"slices"
	"strings"
	"time"

	"fitzpatrickfamilyplatform/engineering/privileged_proxy/protocol"
	"fitzpatrickfamilyplatform/engineering/privileged_proxy/target"
	"fitzpatrickfamilyplatform/engineering/privileged_proxy/upstream"
)

func Project(
	operation protocol.Operation,
	derived target.Derived,
	observation upstream.Observation,
) (protocol.ResultEnvelope, []protocol.Limitation, string, *protocol.Failure) {
	if observation.TargetSubject != derived.SubjectID || observation.TargetHost != derived.HostReference {
		return protocol.ResultEnvelope{}, nil, "", protocol.Fail(
			protocol.ReasonTargetMismatch,
			protocol.SafeMessage(protocol.ReasonTargetMismatch),
		)
	}
	if observation.RecordCount < 0 || observation.RecordCount > protocol.MaximumResultRecords {
		return protocol.ResultEnvelope{}, nil, "", protocol.Fail(
			protocol.ReasonRecordLimitExceeded,
			protocol.SafeMessage(protocol.ReasonRecordLimitExceeded),
		)
	}
	if observation.PayloadSizeBytes < 0 || observation.PayloadSizeBytes > protocol.MaximumResponseBytes {
		return protocol.ResultEnvelope{}, nil, "", protocol.Fail(
			protocol.ReasonResponseOversized,
			protocol.SafeMessage(protocol.ReasonResponseOversized),
		)
	}
	if len(observation.UnexpectedFields) != 0 {
		return protocol.ResultEnvelope{}, nil, "", protocol.Fail(
			protocol.ReasonResponseFieldRejected,
			protocol.SafeMessage(protocol.ReasonResponseFieldRejected),
		)
	}
	if !boundedASCII(observation.ProviderAPIVersion, 32, false) {
		return protocol.ResultEnvelope{}, nil, "", protocol.Fail(
			protocol.ReasonResponseMalformed,
			protocol.SafeMessage(protocol.ReasonResponseMalformed),
		)
	}
	result := protocol.ResultEnvelope{}
	switch operation {
	case protocol.ResolveTargetIdentity:
		if observation.Identity == nil || anyOtherResult(observation, operation) {
			return result, nil, "", malformed()
		}
		switch observation.Identity.Resolution {
		case "exact":
		case "absent":
			return result, nil, "", protocol.Fail(protocol.ReasonTargetAbsent, protocol.SafeMessage(protocol.ReasonTargetAbsent))
		case "duplicate":
			return result, nil, "", protocol.Fail(protocol.ReasonTargetDuplicate, protocol.SafeMessage(protocol.ReasonTargetDuplicate))
		case "ambiguous":
			return result, nil, "", protocol.Fail(protocol.ReasonTargetAmbiguous, protocol.SafeMessage(protocol.ReasonTargetAmbiguous))
		case "conflicting":
			return result, nil, "", protocol.Fail(protocol.ReasonTargetConflicting, protocol.SafeMessage(protocol.ReasonTargetConflicting))
		default:
			return result, nil, "", malformed()
		}
		if !validIdentity(observation.Identity) {
			return result, nil, "", malformed()
		}
		result.Identity = cloneIdentity(observation.Identity)
	case protocol.ObserveLifecycle:
		if observation.Lifecycle == nil || anyOtherResult(observation, operation) {
			return result, nil, "", malformed()
		}
		if !validLifecycle(observation.Lifecycle) {
			return result, nil, "", malformed()
		}
		result.Lifecycle = cloneLifecycle(observation.Lifecycle)
	case protocol.ObserveHealth:
		if observation.Health == nil || anyOtherResult(observation, operation) {
			return result, nil, "", malformed()
		}
		if !validHealth(observation.Health) {
			return result, nil, "", malformed()
		}
		result.Health = cloneHealth(observation.Health)
	case protocol.ObserveRestartInformation:
		if observation.Restart == nil || anyOtherResult(observation, operation) {
			return result, nil, "", malformed()
		}
		if !validRestart(observation.Restart) {
			return result, nil, "", malformed()
		}
		result.Restart = cloneRestart(observation.Restart)
	case protocol.ObserveStatisticsOnce:
		if observation.Statistics == nil || anyOtherResult(observation, operation) {
			return result, nil, "", malformed()
		}
		if !validStatistics(observation.Statistics) {
			return result, nil, "", malformed()
		}
		result.Statistics = cloneStatistics(observation.Statistics)
	default:
		return result, nil, "", protocol.Fail(protocol.ReasonOperationDenied, protocol.SafeMessage(protocol.ReasonOperationDenied))
	}
	limitations := slices.Clone(observation.Limitations)
	slices.Sort(limitations)
	for index := 1; index < len(limitations); index++ {
		if limitations[index] == limitations[index-1] {
			return protocol.ResultEnvelope{}, nil, "", malformed()
		}
	}
	for _, limitation := range limitations {
		if !slices.Contains([]protocol.Limitation{
			protocol.LimitationCgroupMode,
			protocol.LimitationFixtureOnly,
			protocol.LimitationNoTransport,
			protocol.LimitationOneShot,
			protocol.LimitationSynthetic,
		}, limitation) {
			return protocol.ResultEnvelope{}, nil, "", malformed()
		}
	}
	return result, limitations, observation.ProviderAPIVersion, nil
}

func anyOtherResult(observation upstream.Observation, operation protocol.Operation) bool {
	count := 0
	if observation.Health != nil {
		count++
	}
	if observation.Identity != nil {
		count++
	}
	if observation.Lifecycle != nil {
		count++
	}
	if observation.Restart != nil {
		count++
	}
	if observation.Statistics != nil {
		count++
	}
	return count != 1
}

func malformed() *protocol.Failure {
	return protocol.Fail(protocol.ReasonResponseMalformed, protocol.SafeMessage(protocol.ReasonResponseMalformed))
}

func validIdentity(value *protocol.IdentityResult) bool {
	return value.Resolution == "exact" &&
		protocol.ValidDigest(value.RuntimeIDReference) &&
		boundedASCII(value.RuntimeName, 128, false) &&
		boundedASCII(value.ComposeProject, 128, false) &&
		boundedASCII(value.ComposeService, 128, false) &&
		boundedASCII(value.ComposeContainerNumber, 16, false) &&
		boundedASCII(value.ImageReference, 256, true) &&
		(value.ImageDigest == "" || protocol.ValidDigest(value.ImageDigest)) &&
		boundedASCII(value.ProviderContext, 64, false)
}

func validLifecycle(value *protocol.LifecycleResult) bool {
	return slices.Contains([]string{"created", "dead", "exited", "paused", "restarting", "running", "unknown"}, value.State) &&
		validTimestamp(value.ObservedAt, false) &&
		validTimestamp(value.StartedAt, true) &&
		validTimestamp(value.FinishedAt, true) &&
		value.ExitCode >= -1 && value.ExitCode <= 255
}

func validHealth(value *protocol.HealthResult) bool {
	return slices.Contains([]string{"healthy", "none", "starting", "unhealthy", "unknown"}, value.State) &&
		value.FailingStreak >= 0 && validTimestamp(value.ObservedAt, false)
}

func validRestart(value *protocol.RestartResult) bool {
	return slices.Contains([]string{"restarting", "running", "stopped", "unknown"}, value.State) &&
		value.Count >= 0 && validTimestamp(value.ObservedAt, false)
}

func validStatistics(value *protocol.StatisticsResult) bool {
	return value.CPUOnlineCount >= 0 && value.CPUOnlineCount <= 1024 &&
		value.CPUSystemUsage >= 0 && value.CPUTotalUsage >= 0 &&
		value.MemoryCacheBasis >= 0 && value.MemoryLimit >= 0 && value.MemoryUsage >= 0 &&
		value.PIDsCurrent >= 0 &&
		slices.Contains([]string{"synthetic", "unknown", "v1", "v2"}, value.CgroupMode) &&
		validTimestamp(value.ReadAt, false)
}

func validTimestamp(value string, allowEmpty bool) bool {
	if value == "" {
		return allowEmpty
	}
	parsed, err := time.Parse(time.RFC3339Nano, value)
	return err == nil && parsed.Location() == time.UTC && strings.HasSuffix(value, "Z")
}

func boundedASCII(value string, maximum int, allowEmpty bool) bool {
	if value == "" {
		return allowEmpty
	}
	if len(value) > maximum {
		return false
	}
	for _, char := range []byte(value) {
		if char < 0x20 || char > 0x7e {
			return false
		}
	}
	return true
}

func cloneIdentity(value *protocol.IdentityResult) *protocol.IdentityResult {
	result := *value
	return &result
}

func cloneLifecycle(value *protocol.LifecycleResult) *protocol.LifecycleResult {
	result := *value
	return &result
}

func cloneHealth(value *protocol.HealthResult) *protocol.HealthResult {
	result := *value
	return &result
}

func cloneRestart(value *protocol.RestartResult) *protocol.RestartResult {
	result := *value
	return &result
}

func cloneStatistics(value *protocol.StatisticsResult) *protocol.StatisticsResult {
	result := *value
	return &result
}
