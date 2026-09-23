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

func TestSomaEdgeCases(t *testing.T) {
	if Soma(-100, -200) != -300 {
		t.Error("Soma com negativos falhou")
	}
	if Soma(1000000, 2000000) != 3000000 {
		t.Error("Soma com numeros grandes falhou")
	}
	if Soma(-1, 1) != 0 {
		t.Error("Soma com opostos falhou")
	}
}

func TestSubtraiEdgeCases(t *testing.T) {
	if Subtrai(-100, -200) != 100 {
		t.Error("Subtrai com negativos falhou")
	}
	if Subtrai(1000000, 1) != 999999 {
		t.Error("Subtrai com numeros grandes falhou")
	}
	if Subtrai(0, 100) != -100 {
		t.Error("Subtrai com resultado negativo falhou")
	}
}

func TestMain(t *testing.T) {
	defer func() {
		if r := recover(); r != nil {
			t.Errorf("main() panicou: %v", r)
		}
	}()
	main()
}