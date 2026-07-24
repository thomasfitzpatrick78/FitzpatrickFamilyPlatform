package upstream

import (
	"context"
	"sync"

	"fitzpatrickfamilyplatform/engineering/privileged_proxy/protocol"
	"fitzpatrickfamilyplatform/engineering/privileged_proxy/target"
)

// Observer is deliberately closed and typed. It cannot express an address,
// connection, method, route, query, header, body, stream, or generic request.
type Observer interface {
	ObserveHealth(context.Context, target.Derived) (Observation, *protocol.Failure)
	ObserveLifecycle(context.Context, target.Derived) (Observation, *protocol.Failure)
	ObserveRestartInformation(context.Context, target.Derived) (Observation, *protocol.Failure)
	ObserveStatisticsOnce(context.Context, target.Derived) (Observation, *protocol.Failure)
	ResolveTargetIdentity(context.Context, target.Derived) (Observation, *protocol.Failure)
}

type Observation struct {
	Health             *protocol.HealthResult
	Identity           *protocol.IdentityResult
	Lifecycle          *protocol.LifecycleResult
	Limitations        []protocol.Limitation
	PayloadSizeBytes   int
	ProviderAPIVersion string
	RecordCount        int
	Restart            *protocol.RestartResult
	Statistics         *protocol.StatisticsResult
	TargetHost         string
	TargetSubject      string
	UnexpectedFields   []string
}

type SyntheticResults struct {
	Health     Observation
	Identity   Observation
	Lifecycle  Observation
	Restart    Observation
	Statistics Observation
}

// SyntheticObserver returns injected typed observations and records invocations.
// It has no I/O capability.
type SyntheticObserver struct {
	failures    map[protocol.Operation]*protocol.Failure
	invocations map[protocol.Operation]int
	mutex       sync.Mutex
	results     SyntheticResults
}

func NewSyntheticObserver(results SyntheticResults) *SyntheticObserver {
	return &SyntheticObserver{
		failures:    make(map[protocol.Operation]*protocol.Failure),
		invocations: make(map[protocol.Operation]int),
		results:     results,
	}
}

func (observer *SyntheticObserver) SetFailure(operation protocol.Operation, failure *protocol.Failure) {
	observer.mutex.Lock()
	defer observer.mutex.Unlock()
	observer.failures[operation] = failure
}

func (observer *SyntheticObserver) SetObservation(operation protocol.Operation, observation Observation) {
	observer.mutex.Lock()
	defer observer.mutex.Unlock()
	switch operation {
	case protocol.ResolveTargetIdentity:
		observer.results.Identity = observation
	case protocol.ObserveLifecycle:
		observer.results.Lifecycle = observation
	case protocol.ObserveHealth:
		observer.results.Health = observation
	case protocol.ObserveRestartInformation:
		observer.results.Restart = observation
	case protocol.ObserveStatisticsOnce:
		observer.results.Statistics = observation
	}
}

func (observer *SyntheticObserver) InvocationCount(operation protocol.Operation) int {
	observer.mutex.Lock()
	defer observer.mutex.Unlock()
	return observer.invocations[operation]
}

func (observer *SyntheticObserver) ObserveHealth(_ context.Context, _ target.Derived) (Observation, *protocol.Failure) {
	return observer.result(protocol.ObserveHealth, observer.results.Health)
}

func (observer *SyntheticObserver) ObserveLifecycle(_ context.Context, _ target.Derived) (Observation, *protocol.Failure) {
	return observer.result(protocol.ObserveLifecycle, observer.results.Lifecycle)
}

func (observer *SyntheticObserver) ObserveRestartInformation(_ context.Context, _ target.Derived) (Observation, *protocol.Failure) {
	return observer.result(protocol.ObserveRestartInformation, observer.results.Restart)
}

func (observer *SyntheticObserver) ObserveStatisticsOnce(_ context.Context, _ target.Derived) (Observation, *protocol.Failure) {
	return observer.result(protocol.ObserveStatisticsOnce, observer.results.Statistics)
}

func (observer *SyntheticObserver) ResolveTargetIdentity(_ context.Context, _ target.Derived) (Observation, *protocol.Failure) {
	return observer.result(protocol.ResolveTargetIdentity, observer.results.Identity)
}

func (observer *SyntheticObserver) result(operation protocol.Operation, observation Observation) (Observation, *protocol.Failure) {
	observer.mutex.Lock()
	defer observer.mutex.Unlock()
	observer.invocations[operation]++
	if failure := observer.failures[operation]; failure != nil {
		return Observation{}, failure
	}
	return observation, nil
}

func Dispatch(
	ctx context.Context,
	observer Observer,
	operation protocol.Operation,
	derived target.Derived,
) (Observation, *protocol.Failure) {
	switch operation {
	case protocol.ResolveTargetIdentity:
		return observer.ResolveTargetIdentity(ctx, derived)
	case protocol.ObserveLifecycle:
		return observer.ObserveLifecycle(ctx, derived)
	case protocol.ObserveHealth:
		return observer.ObserveHealth(ctx, derived)
	case protocol.ObserveRestartInformation:
		return observer.ObserveRestartInformation(ctx, derived)
	case protocol.ObserveStatisticsOnce:
		return observer.ObserveStatisticsOnce(ctx, derived)
	default:
		return Observation{}, protocol.Fail(protocol.ReasonOperationDenied, protocol.SafeMessage(protocol.ReasonOperationDenied))
	}
}
