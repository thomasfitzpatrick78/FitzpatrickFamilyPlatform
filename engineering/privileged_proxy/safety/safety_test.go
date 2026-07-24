package safety

import (
	"os"
	"path/filepath"
	"testing"
)

func TestRepositorySourcePassesStaticSafety(t *testing.T) {
	root, err := filepath.Abs("..")
	if err != nil {
		t.Fatal(err)
	}
	findings, err := ValidateTree(root)
	if err != nil {
		t.Fatal(err)
	}
	if len(findings) != 0 {
		t.Fatalf("static safety findings: %+v", findings)
	}
}

func TestStaticSafetyDetectsNetworkShellEnvironmentAndFilesystemCapability(t *testing.T) {
	root := t.TempDir()
	source := `package unsafeexample
import (
	"net"
	"os"
	"os/exec"
)
func prohibited() {
	_ = net.IPv4len
	_ = os.Getenv("X")
	_, _ = os.ReadFile("/unbounded")
	_ = exec.Command("sh")
}`
	if err := os.WriteFile(filepath.Join(root, "unsafe.go"), []byte(source), 0o600); err != nil {
		t.Fatal(err)
	}
	findings, err := ValidateTree(root)
	if err != nil {
		t.Fatal(err)
	}
	if len(findings) < 4 {
		t.Fatalf("expected at least four findings, got %+v", findings)
	}
}
