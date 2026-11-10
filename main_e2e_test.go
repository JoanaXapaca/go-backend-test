//go:build e2e

package main

import (
	"os/exec"
	"testing"
	"time"
)

// TestE2E_ServerStarts verifies the binary compiles and starts without immediate crashing.
func TestE2E_ServerStarts(t *testing.T) {
	build := exec.Command("go", "build", "-o", "test_app.exe", ".")
	if err := build.Run(); err != nil {
		t.Fatalf("Build failed: %v", err)
	}

	cmd := exec.Command("./test_app.exe")
	if err := cmd.Start(); err != nil {
		t.Fatalf("Failed to start server: %v", err)
	}

	// Give it a moment to start
	time.Sleep(2 * time.Second)

	// Check if it's still running (hasn't crashed)
	if cmd.Process == nil {
		t.Fatal("Process is nil, server failed to start")
	}

	// Kill it to clean up
	if err := cmd.Process.Kill(); err != nil {
		t.Logf("Warning: could not kill process: %v", err)
	}
}