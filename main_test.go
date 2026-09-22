package main

import "testing"

func TestSoma(t *testing.T) {
	casos := []struct {
		a, b, esperado int
	}{
		{2, 3, 5},
		{-1, 1, 0},
		{0, 0, 0},
		{100, 200, 300},
	}

	for _, c := range casos {
		resultado := Soma(c.a, c.b)
		if resultado != c.esperado {
			t.Errorf("Soma(%d, %d) = %d; esperado %d", c.a, c.b, resultado, c.esperado)
		}
	}
}

func TestSubtrai(t *testing.T) {
	casos := []struct {
		a, b, esperado int
	}{
		{10, 4, 6},
		{0, 0, 0},
		{-5, -5, 0},
	}

	for _, c := range casos {
		resultado := Subtrai(c.a, c.b)
		if resultado != c.esperado {
			t.Errorf("Subtrai(%d, %d) = %d; esperado %d", c.a, c.b, resultado, c.esperado)
		}
	}
}