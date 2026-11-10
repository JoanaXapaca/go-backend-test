package main

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"
)

// TestAdd verifies Add with a table of input/expected pairs.
func TestAdd(t *testing.T) {
	cases := []struct {
		a, b, expected int
	}{
		{2, 3, 5},
		{-1, 1, 0},
		{0, 0, 0},
		{100, 200, 300},
	}

	for _, c := range cases {
		result := Add(c.a, c.b)
		if result != c.expected {
			t.Errorf("Add(%d, %d) = %d; expected %d", c.a, c.b, result, c.expected)
		}
	}
}

// TestSubtract verifies Subtract with a table of input/expected pairs.
func TestSubtract(t *testing.T) {
	cases := []struct {
		a, b, expected int
	}{
		{10, 4, 6},
		{0, 0, 0},
		{-5, -5, 0},
	}

	for _, c := range cases {
		result := Subtract(c.a, c.b)
		if result != c.expected {
			t.Errorf("Subtract(%d, %d) = %d; expected %d", c.a, c.b, result, c.expected)
		}
	}
}

// TestAddEdgeCases covers boundary values for Add.
func TestAddEdgeCases(t *testing.T) {
	if Add(-100, -200) != -300 {
		t.Error("Add with negative numbers failed")
	}
	if Add(1000000, 2000000) != 3000000 {
		t.Error("Add with large numbers failed")
	}
	if Add(-1, 1) != 0 {
		t.Error("Add with opposite numbers failed")
	}
}

// TestSubtractEdgeCases covers boundary values for Subtract.
func TestSubtractEdgeCases(t *testing.T) {
	if Subtract(-100, -200) != 100 {
		t.Error("Subtract with negative numbers failed")
	}
	if Subtract(1000000, 1) != 999999 {
		t.Error("Subtract with large numbers failed")
	}
	if Subtract(0, 100) != -100 {
		t.Error("Subtract with negative result failed")
	}
}

// TestHealthHandler verifies the HTTP handler returns 200 and the correct JSON.
func TestHealthHandler(t *testing.T) {
	req, err := http.NewRequest("GET", "/api/health", nil)
	if err != nil {
		t.Fatal(err)
	}

	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(HealthHandler)
	handler.ServeHTTP(rr, req)

	if status := rr.Code; status != http.StatusOK {
		t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusOK)
	}

	var response map[string]string
	if err := json.Unmarshal(rr.Body.Bytes(), &response); err != nil {
		t.Fatalf("failed to unmarshal response: %v", err)
	}
	if response["status"] != "healthy" {
		t.Errorf("handler returned unexpected body: got %v want %v", response["status"], "healthy")
	}
}

// TestRun verifies that the server starts and responds on the health endpoint.
// It covers the run() function so that the coverage includes main.go.
func TestRun(t *testing.T) {
	// Start the server in a background goroutine
	go func() {
		if err := run(); err != nil && err != http.ErrServerClosed {
			t.Logf("run() returned: %v", err)
		}
	}()

	// Give the server time to start
	time.Sleep(1 * time.Second)

	// Make a request to the health endpoint
	resp, err := http.Get("http://localhost:8081/api/health")
	if err != nil {
		t.Fatalf("Failed to make request: %v", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		t.Errorf("Expected status 200, got %d", resp.StatusCode)
	}
}