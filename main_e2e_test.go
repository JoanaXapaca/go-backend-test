//go:build e2e

package main

import (
	"os/exec"
	"strings"
	"testing"
)

func TestE2E_Output(t *testing.T) {
	build := exec.Command("go", "build", "-o", "test_app.exe", ".")
	if err := build.Run(); err != nil {
		t.Fatalf("Build falhou: %v", err)
	}

	output, err := exec.Command("./test_app.exe").Output()
	if err != nil {
		t.Fatalf("Execução falhou: %v", err)
	}

	out := string(output)
	if !strings.Contains(out, "Soma 2+3 = 5") {
		t.Error("Output não contém 'Soma 2+3 = 5'")
	}
	if !strings.Contains(out, "Subtrai 10-4 = 6") {
		t.Error("Output não contém 'Subtrai 10-4 = 6'")
	}
}