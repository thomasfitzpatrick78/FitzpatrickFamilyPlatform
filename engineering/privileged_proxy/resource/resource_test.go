package resource

import (
	"testing"
	"time"

	"fitzpatrickfamilyplatform/engineering/privileged_proxy/protocol"
)

func TestAdmissionConcurrencyAndRateLimits(t *testing.T) {
	admission, failure := NewAdmission(GovernedLimits())
	if failure != nil {
		t.Fatal(failure)
	}
	now := time.Date(2026, 7, 23, 12, 0, 0, 0, time.UTC)
	first, failure := admission.Acquire("identity", "target", now)
	if failure != nil {
		t.Fatal(failure)
	}
	second, failure := admission.Acquire("identity", "target", now)
	if failure != nil {
		t.Fatal(failure)
	}
	if _, failure = admission.Acquire("identity", "target", now); failure == nil ||
		failure.Reason != protocol.ReasonConcurrencyExhausted {
		t.Fatalf("expected concurrency denial, got %v", failure)
	}
	first()
	second()
	if _, failure = admission.Acquire("identity", "target", now); failure == nil ||
		failure.Reason != protocol.ReasonRateLimited {
		t.Fatalf("expected rate denial, got %v", failure)
	}
	release, failure := admission.Acquire("identity", "target", now.Add(10*time.Second))
	if failure != nil {
		t.Fatal(failure)
	}
	release()
}

func TestGovernedResourcePolicyRejectsDrift(t *testing.T) {
	limits := GovernedLimits()
	limits.GlobalConcurrency++
	if _, failure := NewAdmission(limits); failure == nil {
		t.Fatal("drifted limits unexpectedly accepted")
	}
}

func TestLogicalTimeoutBudgetEvaluation(t *testing.T) {
	admission, failure := NewAdmission(GovernedLimits())
	if failure != nil {
		t.Fatal(failure)
	}
	requestedAt := time.Date(2026, 7, 23, 12, 0, 0, 0, time.UTC)
	deadline := requestedAt.Add(10 * time.Second)
	if budget, failure := admission.EvaluateTimeoutBudget(requestedAt, deadline, requestedAt); failure != nil ||
		budget != GovernedLimits().UpstreamTimeout {
		t.Fatalf("budget = %v, failure = %v", budget, failure)
	}
	if budget, failure := admission.EvaluateTimeoutBudget(
		requestedAt, deadline, deadline.Add(-time.Second),
	); failure != nil || budget != time.Second {
		t.Fatalf("short budget = %v, failure = %v", budget, failure)
	}
	if _, failure := admission.EvaluateTimeoutBudget(requestedAt, deadline, deadline); failure == nil ||
		failure.Reason != protocol.ReasonRequestTimedOut {
		t.Fatalf("expected request timeout, got %v", failure)
	}
	if _, failure := admission.EvaluateTimeoutBudget(
		requestedAt, deadline.Add(time.Nanosecond), requestedAt,
	); failure == nil || failure.Reason != protocol.ReasonDeadlineInvalid {
		t.Fatalf("expected deadline denial, got %v", failure)
	}
}
