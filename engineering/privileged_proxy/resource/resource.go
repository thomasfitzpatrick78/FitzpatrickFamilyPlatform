package resource

import (
	"sync"
	"time"

	"fitzpatrickfamilyplatform/engineering/privileged_proxy/protocol"
)

type Limits struct {
	AuditRetention         time.Duration
	GlobalConcurrency      int
	MaximumRecords         int
	MaximumRequestBytes    int
	MaximumResponseBytes   int
	PerIdentityConcurrency int
	RateBurst              int
	RatePerMinute          int
	ReplayRetention        time.Duration
	ShutdownGrace          time.Duration
	TotalTimeout           time.Duration
	UpstreamTimeout        time.Duration
}

func GovernedLimits() Limits {
	return Limits{
		AuditRetention:         90 * 24 * time.Hour,
		GlobalConcurrency:      4,
		MaximumRecords:         protocol.MaximumResultRecords,
		MaximumRequestBytes:    protocol.MaximumRequestBytes,
		MaximumResponseBytes:   protocol.MaximumResponseBytes,
		PerIdentityConcurrency: 2,
		RateBurst:              2,
		RatePerMinute:          6,
		ReplayRetention:        24 * time.Hour,
		ShutdownGrace:          15 * time.Second,
		TotalTimeout:           10 * time.Second,
		UpstreamTimeout:        3 * time.Second,
	}
}

func (limits Limits) Validate() *protocol.Failure {
	expected := GovernedLimits()
	if limits != expected {
		return protocol.Fail(protocol.ReasonInternalFailClosed, "Resource policy differs from the governed configuration.")
	}
	return nil
}

type bucket struct {
	last   time.Time
	tokens float64
}

type Admission struct {
	buckets  map[string]bucket
	global   int
	identity map[string]int
	limits   Limits
	mutex    sync.Mutex
}

func NewAdmission(limits Limits) (*Admission, *protocol.Failure) {
	if failure := limits.Validate(); failure != nil {
		return nil, failure
	}
	return &Admission{
		buckets:  make(map[string]bucket),
		identity: make(map[string]int),
		limits:   limits,
	}, nil
}

func (admission *Admission) Acquire(
	serviceIdentity, targetReference string,
	now time.Time,
) (func(), *protocol.Failure) {
	admission.mutex.Lock()
	defer admission.mutex.Unlock()
	if admission.global >= admission.limits.GlobalConcurrency ||
		admission.identity[serviceIdentity] >= admission.limits.PerIdentityConcurrency {
		return nil, protocol.Fail(protocol.ReasonConcurrencyExhausted, protocol.SafeMessage(protocol.ReasonConcurrencyExhausted))
	}
	key := serviceIdentity + "\x00" + targetReference
	current, exists := admission.buckets[key]
	if !exists {
		current = bucket{last: now, tokens: float64(admission.limits.RateBurst)}
	}
	if now.Before(current.last) {
		return nil, protocol.Fail(protocol.ReasonRateLimited, "Rate clock moved backwards.")
	}
	elapsedMinutes := now.Sub(current.last).Minutes()
	current.tokens += elapsedMinutes * float64(admission.limits.RatePerMinute)
	if current.tokens > float64(admission.limits.RateBurst) {
		current.tokens = float64(admission.limits.RateBurst)
	}
	current.last = now
	if current.tokens < 1 {
		admission.buckets[key] = current
		return nil, protocol.Fail(protocol.ReasonRateLimited, protocol.SafeMessage(protocol.ReasonRateLimited))
	}
	current.tokens--
	admission.buckets[key] = current
	admission.global++
	admission.identity[serviceIdentity]++
	released := false
	return func() {
		admission.mutex.Lock()
		defer admission.mutex.Unlock()
		if released {
			return
		}
		released = true
		admission.global--
		admission.identity[serviceIdentity]--
	}, nil
}

// EvaluateTimeoutBudget performs deterministic, clock-injected policy
// evaluation only. It does not create a timer or provide transport/process
// enforcement. A later transport gate must re-prove actual deadline behavior.
func (admission *Admission) EvaluateTimeoutBudget(
	requestedAt, deadline, now time.Time,
) (time.Duration, *protocol.Failure) {
	if !deadline.After(requestedAt) || deadline.Sub(requestedAt) > admission.limits.TotalTimeout {
		return 0, protocol.Fail(protocol.ReasonDeadlineInvalid, protocol.SafeMessage(protocol.ReasonDeadlineInvalid))
	}
	if !now.Before(deadline) {
		return 0, protocol.Fail(protocol.ReasonRequestTimedOut, protocol.SafeMessage(protocol.ReasonRequestTimedOut))
	}
	budget := deadline.Sub(now)
	if budget > admission.limits.UpstreamTimeout {
		budget = admission.limits.UpstreamTimeout
	}
	return budget, nil
}
