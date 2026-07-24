package protocol

const (
	ProtocolVersion          = "1.0"
	AuthorizationVersion     = "1.0"
	MaximumRequestBytes      = 16_384
	MaximumResponseBytes     = 65_536
	MaximumResultRecords     = 1
	MaximumCollectionEntries = 64
	MaximumNestingDepth      = 12
	MaximumStringBytes       = 512
)

type Operation string

const (
	ResolveTargetIdentity      Operation = "ResolveTargetIdentity"
	ObserveLifecycle           Operation = "ObserveLifecycle"
	ObserveHealth              Operation = "ObserveHealth"
	ObserveRestartInformation  Operation = "ObserveRestartInformation"
	ObserveStatisticsOnce      Operation = "ObserveStatisticsOnce"
	CheckProviderCompatibility Operation = "CheckProviderCompatibility"
)

type Category string

const (
	IdentityDiscovery    Category = "IdentityDiscovery"
	LifecycleObservation Category = "LifecycleObservation"
	HealthObservation    Category = "HealthObservation"
	RestartInformation   Category = "RestartInformation"
	Statistics           Category = "Statistics"
	System               Category = "System"
)

type PeerContext struct {
	GID               uint32
	IdentitySource    string
	PID               int32
	ServiceIdentity   string
	UID               uint32
	VerificationState string
}

// AuthorizationEnvelope contains bounded signed one-shot authorization.
// Signature is detached from the canonical signing content.
type AuthorizationEnvelope struct {
	AdapterArtifactDigest     string      `json:"adapter_artifact_digest"`
	AdapterIdentity           string      `json:"adapter_identity"`
	Algorithm                 string      `json:"algorithm"`
	AllowedOperations         []Operation `json:"allowed_operations"`
	AllowedSignals            []string    `json:"allowed_signals"`
	ApprovalReference         string      `json:"approval_reference"`
	AuthorizationDigest       string      `json:"authorization_digest"`
	AuthorizationReference    string      `json:"authorization_reference"`
	AuthorizationVersion      string      `json:"authorization_version"`
	ComposeProject            string      `json:"compose_project"`
	ComposeService            string      `json:"compose_service"`
	ConfigurationDigest       string      `json:"configuration_digest"`
	CorrelationID             string      `json:"correlation_id"`
	DeploymentBundleDigest    string      `json:"deployment_bundle_digest"`
	GovernedRuntimeName       string      `json:"governed_runtime_name"`
	HostReference             string      `json:"host_reference"`
	KeyID                     string      `json:"key_id"`
	MaxAttempts               int         `json:"max_attempts"`
	Nonce                     string      `json:"nonce"`
	PolicyDigest              string      `json:"policy_digest"`
	ProxyImplementationDigest string      `json:"proxy_implementation_digest"`
	RegistryRecordDigest      string      `json:"registry_record_digest"`
	SelectorKind              string      `json:"selector_kind"`
	Signature                 string      `json:"signature"`
	SignerIdentity            string      `json:"signer_identity"`
	SubjectID                 string      `json:"subject_id"`
	TrustAnchorDigest         string      `json:"trust_anchor_digest"`
	TrustBindingDigest        string      `json:"trust_binding_digest"`
	ValidFrom                 string      `json:"valid_from"`
	ValidUntil                string      `json:"valid_until"`
}

type TargetReference struct {
	ComposeProject         string `json:"compose_project"`
	ComposeService         string `json:"compose_service"`
	ExpectedImageDigest    string `json:"expected_image_digest"`
	ExpectedImageReference string `json:"expected_image_reference"`
	GovernedRuntimeName    string `json:"governed_runtime_name"`
	HostReference          string `json:"host_reference"`
	RegistryRecordDigest   string `json:"registry_record_digest"`
	RegistryReference      string `json:"registry_reference"`
	SelectorKind           string `json:"selector_kind"`
	SubjectID              string `json:"subject_id"`
}

type RequestEnvelope struct {
	AdapterArtifactDigest     string                `json:"adapter_artifact_digest"`
	Authorization             AuthorizationEnvelope `json:"authorization"`
	ConfigurationDigest       string                `json:"configuration_digest"`
	CorrelationID             string                `json:"correlation_id"`
	Deadline                  string                `json:"deadline"`
	DeploymentBundleDigest    string                `json:"deployment_bundle_digest"`
	Operation                 Operation             `json:"operation"`
	PolicyDigest              string                `json:"policy_digest"`
	ProtocolVersion           string                `json:"protocol_version"`
	ProxyImplementationDigest string                `json:"proxy_implementation_digest"`
	RequestID                 string                `json:"request_id"`
	RequestedAt               string                `json:"requested_at"`
	RequestedSignals          []string              `json:"requested_signals"`
	Target                    TargetReference       `json:"target"`
	TrustBindingDigest        string                `json:"trust_binding_digest"`
}

type Limitation string

const (
	LimitationFixtureOnly Limitation = "fixture_only"
	LimitationNoTransport Limitation = "no_transport"
	LimitationOneShot     Limitation = "one_shot"
	LimitationSynthetic   Limitation = "synthetic_upstream"
	LimitationCgroupMode  Limitation = "cgroup_mode_unverified"
)

type IdentityResult struct {
	ComposeContainerNumber string `json:"compose_container_number"`
	ComposeProject         string `json:"compose_project"`
	ComposeService         string `json:"compose_service"`
	ImageDigest            string `json:"image_digest"`
	ImageReference         string `json:"image_reference"`
	ProviderContext        string `json:"provider_context"`
	Resolution             string `json:"resolution"`
	RuntimeIDReference     string `json:"runtime_id_reference"`
	RuntimeName            string `json:"runtime_name"`
}

type LifecycleResult struct {
	Dead       bool   `json:"dead"`
	ExitCode   int    `json:"exit_code"`
	FinishedAt string `json:"finished_at"`
	OOMKilled  bool   `json:"oom_killed"`
	ObservedAt string `json:"observed_at"`
	Paused     bool   `json:"paused"`
	Restarting bool   `json:"restarting"`
	Running    bool   `json:"running"`
	StartedAt  string `json:"started_at"`
	State      string `json:"state"`
}

type HealthResult struct {
	Configured    bool   `json:"configured"`
	FailingStreak int    `json:"failing_streak"`
	ObservedAt    string `json:"observed_at"`
	State         string `json:"state"`
}

type RestartResult struct {
	Count      int    `json:"count"`
	Occurred   bool   `json:"occurred"`
	ObservedAt string `json:"observed_at"`
	State      string `json:"state"`
}

type StatisticsResult struct {
	CPUOnlineCount           int    `json:"cpu_online_count"`
	CPUSystemUsage           int64  `json:"cpu_system_usage"`
	CPUTotalUsage            int64  `json:"cpu_total_usage"`
	CalculationInputComplete bool   `json:"calculation_input_complete"`
	CgroupMode               string `json:"cgroup_mode"`
	MemoryCacheBasis         int64  `json:"memory_cache_basis"`
	MemoryLimit              int64  `json:"memory_limit"`
	MemoryUsage              int64  `json:"memory_usage"`
	PIDsCurrent              int64  `json:"pids_current"`
	ReadAt                   string `json:"read_at"`
}

type ResultEnvelope struct {
	Health     *HealthResult     `json:"health,omitempty"`
	Identity   *IdentityResult   `json:"identity,omitempty"`
	Lifecycle  *LifecycleResult  `json:"lifecycle,omitempty"`
	Restart    *RestartResult    `json:"restart,omitempty"`
	Statistics *StatisticsResult `json:"statistics,omitempty"`
}

type ProxyIdentity struct {
	ArtifactDigest      string `json:"artifact_digest"`
	ConfigurationDigest string `json:"configuration_digest"`
	ProxyID             string `json:"proxy_id"`
	Version             string `json:"version"`
}

type ResponseTarget struct {
	HostReference string `json:"host_reference"`
	SubjectID     string `json:"subject_id"`
}

type ResponseEnvelope struct {
	AuditCorrelationID string          `json:"audit_correlation_id"`
	CompletedAt        string          `json:"completed_at"`
	CorrelationID      string          `json:"correlation_id"`
	Decision           string          `json:"decision"`
	Limitations        []Limitation    `json:"limitations"`
	Operation          Operation       `json:"operation"`
	ProtocolVersion    string          `json:"protocol_version"`
	ProviderAPIVersion string          `json:"provider_api_version"`
	ProxyIdentity      ProxyIdentity   `json:"proxy_identity"`
	ReasonCode         ReasonCode      `json:"reason_code"`
	RequestID          string          `json:"request_id"`
	Result             *ResultEnvelope `json:"result,omitempty"`
	SafeMessage        string          `json:"safe_message"`
	StartedAt          string          `json:"started_at"`
	TargetReference    ResponseTarget  `json:"target_reference"`
}
