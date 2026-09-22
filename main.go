package main

import "fmt"

// Soma retorna a soma de dois inteiros.
func Soma(a, b int) int {
	return a + b
}

// Subtrai retorna a diferença entre dois inteiros.
func Subtrai(a, b int) int {
	return a - b
}

func main() {
	fmt.Println("Go backend pipeline test")
	fmt.Println("Soma 2+3 =", Soma(2, 3))
	fmt.Println("Subtrai 10-4 =", Subtrai(10, 4))
}