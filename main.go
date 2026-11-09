package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
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
	json.NewEncoder(w).Encode(map[string]string{"status": "healthy"})
}

func main() {
	fmt.Println("Go backend pipeline test running on port 8080...")
	
	http.HandleFunc("/api/health", HealthHandler)
	
	// Start the server
	if err := http.ListenAndServe(":8080", nil); err != nil {
		log.Fatal(err)
	}
}