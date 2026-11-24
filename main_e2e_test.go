//go:build e2e

package main

import (
	"os/exec"
	"strings"
	"testing"
)

// TestE2E_Output builds the binary and verifies its stdout.
func TestE2E_Output(t *testing.T) {
	// Build the binary.
	build := exec.Command("go", "build", "-o", "test_app.exe", ".")
	if err := build.Run(); err != nil {
		t.Fatalf("Build failed: %v", err)
	}

	// Run the binary and capture its output.
	output, err := exec.Command("./test_app.exe").Output()
	if err != nil {
		t.Fatalf("Execution failed: %v", err)
	}

	// Verify the output contains the expected lines.
	out := string(output)
	if !strings.Contains(out, "Add 2+3 = 5") {
		t.Error("Output does not contain 'Add 2+3 = 5'")
	}
	if !strings.Contains(out, "Subtract 10-4 = 6") {
		t.Error("Output does not contain 'Subtract 10-4 = 6'")
	}
}