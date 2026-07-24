package policy

import (
	"slices"

	"fitzpatrickfamilyplatform/engineering/privileged_proxy/protocol"
)

const PublishedVersion = "constrained-proxy-policy-v1.0"

type State string

const (
	Allowed              State = "Allowed"
	ConditionallyAllowed State = "ConditionallyAllowed"
	Denied               State = "Denied"
	Future               State = "Future"
)

type Entry struct {
	AllowedMethods   []string `json:"allowed_methods"`
	ContractVersion  string   `json:"contract_version"`
	EndpointCategory string   `json:"endpoint_category"`
	State            State    `json:"state"`
}

type Source struct {
	ContractVersion string  `json:"contract_version"`
	DefaultState    State   `json:"default_state"`
	Entries         []Entry `json:"entries"`
	FixtureOnly     bool    `json:"fixture_only"`
	PolicyDigest    string  `json:"policy_digest"`
	PolicyVersion   string  `json:"policy_version"`
}

type compiledEntry struct {
	allowedReadOnly bool
	state           State
}

// Policy is a compiled, closed view of the published Proxy Foundation policy.
// It has no runtime registration or fallback mechanism.
type Policy struct {
	digest  string
	entries map[string]compiledEntry
}

var publishedCategories = []string{
	"Archive",
	"Build",
	"Configuration",
	"Events",
	"Exec",
	"Filesystem",
	"HealthObservation",
	"IdentityDiscovery",
	"Images",
	"LifecycleObservation",
	"Networks",
	"Plugins",
	"RestartInformation",
	"Secrets",
	"Statistics",
	"Swarm",
	"System",
	"Volumes",
}

func Compile(source Source) (Policy, *protocol.Failure) {
	if source.ContractVersion != protocol.ProtocolVersion || source.PolicyVersion != PublishedVersion ||
		source.DefaultState != Denied || !source.FixtureOnly {
		return Policy{}, protocol.Fail(protocol.ReasonCategoryDenied, "Published policy metadata is invalid.")
	}
	if len(source.Entries) != len(publishedCategories) {
		return Policy{}, protocol.Fail(protocol.ReasonCategoryDenied, "Published policy category matrix is incomplete.")
	}
	content := sourceContent{
		ContractVersion: source.ContractVersion,
		DefaultState:    source.DefaultState,
		Entries:         source.Entries,
		FixtureOnly:     source.FixtureOnly,
		PolicyVersion:   source.PolicyVersion,
	}
	data, failure := protocol.EncodeCanonical(content, protocol.MaximumResponseBytes)
	if failure != nil || !protocol.ConstantDigestEqual(protocol.SHA256Digest(data), source.PolicyDigest) {
		return Policy{}, protocol.Fail(protocol.ReasonPolicyDigestMismatch, protocol.SafeMessage(protocol.ReasonPolicyDigestMismatch))
	}
	entries := make(map[string]compiledEntry, len(source.Entries))
	for _, entry := range source.Entries {
		if entry.ContractVersion != protocol.ProtocolVersion || slices.Contains(publishedCategories, entry.EndpointCategory) == false {
			return Policy{}, protocol.Fail(protocol.ReasonCategoryDenied, "Published policy entry is invalid.")
		}
		if _, exists := entries[entry.EndpointCategory]; exists {
			return Policy{}, protocol.Fail(protocol.ReasonCategoryDenied, "Published policy category is duplicated.")
		}
		readOnly := len(entry.AllowedMethods) == 1 && entry.AllowedMethods[0] == "ReadOnly"
		switch entry.State {
		case Allowed, ConditionallyAllowed:
			if !readOnly {
				return Policy{}, protocol.Fail(protocol.ReasonCategoryDenied, "Allowed category must be read-only.")
			}
		case Denied, Future:
			if len(entry.AllowedMethods) != 0 {
				return Policy{}, protocol.Fail(protocol.ReasonCategoryDenied, "Denied category exposes a method.")
			}
		default:
			return Policy{}, protocol.Fail(protocol.ReasonCategoryDenied, "Policy state is unsupported.")
		}
		entries[entry.EndpointCategory] = compiledEntry{allowedReadOnly: readOnly, state: entry.State}
	}
	for _, category := range publishedCategories {
		if _, exists := entries[category]; !exists {
			return Policy{}, protocol.Fail(protocol.ReasonCategoryDenied, "Published policy category is missing.")
		}
	}
	return Policy{digest: source.PolicyDigest, entries: entries}, nil
}

func (policy Policy) Digest() string {
	return policy.digest
}

func (policy Policy) Evaluate(operation protocol.Operation) *protocol.Failure {
	category, known := protocol.CategoryFor(operation)
	if !known {
		return protocol.Fail(protocol.ReasonOperationDenied, protocol.SafeMessage(protocol.ReasonOperationDenied))
	}
	entry, exists := policy.entries[string(category)]
	if !exists || !entry.allowedReadOnly || entry.state == Denied || entry.state == Future || category == protocol.System {
		return protocol.Fail(protocol.ReasonCategoryDenied, protocol.SafeMessage(protocol.ReasonCategoryDenied))
	}
	return nil
}

type sourceContent struct {
	ContractVersion string  `json:"contract_version"`
	DefaultState    State   `json:"default_state"`
	Entries         []Entry `json:"entries"`
	FixtureOnly     bool    `json:"fixture_only"`
	PolicyVersion   string  `json:"policy_version"`
}
