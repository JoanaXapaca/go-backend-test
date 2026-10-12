// Package main is the entry point for the Go backend pipeline test.
//
// This project serves as a test bed for the CI/CD pipeline. It contains
// three simple functions (Add, Subtract, and main) that are used to
// validate that the pipeline runs correctly for Go projects.
//
// The pipeline is defined in the Jenkinsfile at the root of the repository
// and follows the ISO 13485:2016 standard for medical device software.
package main

import "fmt"

// Add returns the sum of two integers.
//
// This function is intentionally simple so that the pipeline can verify
// the full cycle of build, test, and static analysis.
func Add(a, b int) int {
	return a + b
}

// Subtract returns the difference between two integers.
func Subtract(a, b int) int {
	return a - b
}

// main is the entry point of the program.
//
// It prints the results of Add and Subtract to standard output. The
// output is captured by the E2E tests (in main_e2e_test.go) and
// verified line by line to ensure the compiled binary behaves as
// expected.
func main() {
	fmt.Println("Go backend pipeline test")
	fmt.Println("Add 2+3 =", Add(2, 3))
	fmt.Println("Subtract 10-4 =", Subtract(10, 4))
}