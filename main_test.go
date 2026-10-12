package main

import "testing"

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

// TestMain ensures main() runs without panicking.
func TestMain(t *testing.T) {
	defer func() {
		if r := recover(); r != nil {
			t.Errorf("main() panicked: %v", r)
		}
	}()
	main()
}