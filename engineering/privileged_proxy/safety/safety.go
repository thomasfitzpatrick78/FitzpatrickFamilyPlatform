package safety

import (
	"go/ast"
	"go/parser"
	"go/token"
	"io/fs"
	"path/filepath"
	"strconv"
	"strings"
)

type Finding struct {
	File    string
	Message string
}

var forbiddenImports = []string{
	"C",
	"crypto/tls",
	"crypto/x509",
	"net",
	"os/exec",
	"os/user",
	"plugin",
	"reflect",
	"runtime",
	"syscall",
	"unsafe",
}

var forbiddenImportPrefixes = []string{
	"github.com/docker/",
	"github.com/moby/",
	"golang.org/x/crypto/ssh",
	"golang.org/x/sys/",
	"google.golang.org/grpc",
	"k8s.io/",
}

var forbiddenCalls = map[string]map[string]struct{}{
	"os": {
		"Chmod":      {},
		"Chown":      {},
		"Chdir":      {},
		"Environ":    {},
		"Executable": {},
		"ExpandEnv":  {},
		"Getenv":     {},
		"Getegid":    {},
		"Geteuid":    {},
		"Getgid":     {},
		"Getgroups":  {},
		"Getpid":     {},
		"Getppid":    {},
		"Getuid":     {},
		"Hostname":   {},
		"LookupEnv":  {},
		"Setenv":     {},
		"Unsetenv":   {},
	},
	"time": {
		"Now": {},
	},
}

var filesystemCalls = map[string]struct{}{
	"Create":    {},
	"Mkdir":     {},
	"MkdirAll":  {},
	"Open":      {},
	"OpenFile":  {},
	"ReadDir":   {},
	"ReadFile":  {},
	"Remove":    {},
	"RemoveAll": {},
	"Rename":    {},
	"WriteFile": {},
}

// ValidateTree performs deterministic AST validation of the Go source tree.
// Filesystem I/O is restricted to tests plus the ordinary-file audit/replay
// test-store packages. No exception permits network, socket, Docker, shell,
// environment-derived configuration, dynamic loading, or cgo capability.
func ValidateTree(root string) ([]Finding, error) {
	findings := make([]Finding, 0)
	err := filepath.WalkDir(root, func(path string, entry fs.DirEntry, walkErr error) error {
		if walkErr != nil {
			return walkErr
		}
		if entry.IsDir() || filepath.Ext(path) != ".go" {
			return nil
		}
		fileSet := token.NewFileSet()
		file, parseErr := parser.ParseFile(fileSet, path, nil, parser.ParseComments)
		if parseErr != nil {
			findings = append(findings, Finding{File: path, Message: "source does not parse"})
			return nil
		}
		aliases := make(map[string]string)
		for _, imported := range file.Imports {
			importPath, quoteErr := strconv.Unquote(imported.Path.Value)
			if quoteErr != nil {
				findings = append(findings, Finding{File: path, Message: "import path is invalid"})
				continue
			}
			if importForbidden(importPath) {
				findings = append(findings, Finding{File: path, Message: "prohibited import: " + importPath})
			}
			name := filepath.Base(importPath)
			if imported.Name != nil {
				name = imported.Name.Name
			}
			aliases[name] = importPath
		}
		ast.Inspect(file, func(node ast.Node) bool {
			call, ok := node.(*ast.CallExpr)
			if !ok {
				return true
			}
			selector, ok := call.Fun.(*ast.SelectorExpr)
			if !ok {
				return true
			}
			identifier, ok := selector.X.(*ast.Ident)
			if !ok {
				return true
			}
			importPath := aliases[identifier.Name]
			if calls, exists := forbiddenCalls[importPath]; exists {
				if _, forbidden := calls[selector.Sel.Name]; forbidden {
					testPermissionFixture := strings.HasSuffix(path, "_test.go") &&
						importPath == "os" && selector.Sel.Name == "Chmod"
					if !testPermissionFixture {
						findings = append(findings, Finding{File: path, Message: "prohibited call: " + importPath + "." + selector.Sel.Name})
					}
				}
			}
			if importPath == "os" {
				if _, fileCall := filesystemCalls[selector.Sel.Name]; fileCall && !filesystemAllowed(path) {
					findings = append(findings, Finding{File: path, Message: "filesystem call outside test-store boundary: os." + selector.Sel.Name})
				}
			}
			return true
		})
		return nil
	})
	return findings, err
}

func importForbidden(importPath string) bool {
	for _, forbidden := range forbiddenImports {
		if importPath == forbidden || forbidden == "net" && strings.HasPrefix(importPath, "net/") {
			return true
		}
	}
	for _, prefix := range forbiddenImportPrefixes {
		if strings.HasPrefix(importPath, prefix) {
			return true
		}
	}
	return false
}

func filesystemAllowed(path string) bool {
	slashPath := filepath.ToSlash(path)
	return strings.HasSuffix(path, "_test.go") ||
		strings.Contains(slashPath, "/privileged_proxy/audit/") ||
		strings.Contains(slashPath, "/privileged_proxy/replay/")
}
