package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
)

// Add returns the sum of two integers.
func Add(a, b int) int {
	return a + b
}

// Subtract returns the difference between two integers.
func Subtract(a, b int) int {
	return a - b
}

// HealthHandler is used by Docker/Integration tests to check if the API is up.
func HealthHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.WriteHeader(http.StatusOK)
	if err := json.NewEncoder(w).Encode(map[string]string{"status": "healthy"}); err != nil {
		log.Printf("Error encoding response: %v", err)
	}
}

// run contains the actual logic of the application. It is separated from main
// so that it can be tested.
func run() error {
	fmt.Println("Go backend pipeline test running on port 8081...")
	http.HandleFunc("/api/health", HealthHandler)
	return http.ListenAndServe(":8081", nil)
}

func main() {
	if err := run(); err != nil {
		log.Printf("Error: %v", err)
		os.Exit(1)
	}
}