package assignment

import (
	"errors"
	"testing"
)

// helper to build a nurse quickly
func nurse(name string, specialty Specialty, available bool, assigned int) Nurse {
	return Nurse{
		Name:          name,
		Specialty:     specialty,
		Available:     available,
		AssignedCount: assigned,
	}
}

func TestAssign_CriticalAlertGoesToICUNurse(t *testing.T) {
	nurses := []Nurse{
		nurse("Alice", General, true, 0),
		nurse("Bob", ICU, true, 0),
		nurse("Carol", Emergency, true, 0),
	}

	alert := Alert{Room: "101", Type: Critical}
	assigned, err := Assign(alert, nurses)

	if err != nil {
		t.Fatalf("Expected no error, got %v", err)
	}
	if assigned.Name != "Bob" {
		t.Errorf("Expected Bob (ICU), got %s", assigned.Name)
	}
}

func TestAssign_WarningAlertGoesToEmergencyNurse(t *testing.T) {
	nurses := []Nurse{
		nurse("Alice", General, true, 0),
		nurse("Bob", ICU, true, 0),
		nurse("Carol", Emergency, true, 0),
	}

	alert := Alert{Room: "102", Type: Warning}
	assigned, err := Assign(alert, nurses)

	if err != nil {
		t.Fatalf("Expected no error, got %v", err)
	}
	if assigned.Name != "Carol" {
		t.Errorf("Expected Carol (Emergency), got %s", assigned.Name)
	}
}

func TestAssign_InfoAlertAcceptsAnySpecialty(t *testing.T) {
	nurses := []Nurse{
		nurse("Alice", General, true, 0),
	}

	alert := Alert{Room: "103", Type: Info}
	assigned, err := Assign(alert, nurses)

	if err != nil {
		t.Fatalf("Expected no error, got %v", err)
	}
	if assigned.Name != "Alice" {
		t.Errorf("Expected Alice, got %s", assigned.Name)
	}
}

func TestAssign_ReturnsErrorWhenNoNurseAvailable(t *testing.T) {
	nurses := []Nurse{
		nurse("Alice", General, false, 0),
		nurse("Bob", ICU, false, 0),
	}

	alert := Alert{Room: "101", Type: Critical}
	_, err := Assign(alert, nurses)

	if !errors.Is(err, ErrNoNurseAvailable) {
		t.Errorf("Expected ErrNoNurseAvailable, got %v", err)
	}
}

func TestAssign_ReturnsErrorWhenNoMatchingSpecialty(t *testing.T) {
	nurses := []Nurse{
		nurse("Alice", General, true, 0),
		nurse("Carol", Emergency, true, 0),
	}

	alert := Alert{Room: "101", Type: Critical} // needs ICU
	_, err := Assign(alert, nurses)

	if !errors.Is(err, ErrNoNurseAvailable) {
		t.Errorf("Expected ErrNoNurseAvailable, got %v", err)
	}
}

func TestAssign_PicksLeastLoadedNurse(t *testing.T) {
	nurses := []Nurse{
		nurse("Alice", ICU, true, 5),
		nurse("Bob", ICU, true, 2),
		nurse("Carol", ICU, true, 8),
	}

	alert := Alert{Room: "101", Type: Critical}
	assigned, err := Assign(alert, nurses)

	if err != nil {
		t.Fatalf("Expected no error, got %v", err)
	}
	if assigned.Name != "Bob" {
		t.Errorf("Expected Bob (lowest count 2), got %s", assigned.Name)
	}
}

func TestAssign_IncrementsAssignedCount(t *testing.T) {
	nurses := []Nurse{
		nurse("Alice", ICU, true, 3),
	}

	alert := Alert{Room: "101", Type: Critical}
	_, _ = Assign(alert, nurses)

	if nurses[0].AssignedCount != 4 {
		t.Errorf("Expected AssignedCount to be 4, got %d", nurses[0].AssignedCount)
	}
}

func TestAssign_HandlesEmptyNurseList(t *testing.T) {
	nurses := []Nurse{}

	alert := Alert{Room: "101", Type: Critical}
	_, err := Assign(alert, nurses)

	if !errors.Is(err, ErrNoNurseAvailable) {
		t.Errorf("Expected ErrNoNurseAvailable, got %v", err)
	}
}

func TestAssign_IgnoresUnavailableNursesEvenIfSpecialtyMatches(t *testing.T) {
	nurses := []Nurse{
		nurse("Alice", ICU, false, 0), // unavailable
		nurse("Bob", ICU, true, 10),   // available but busier
	}

	alert := Alert{Room: "101", Type: Critical}
	assigned, err := Assign(alert, nurses)

	if err != nil {
		t.Fatalf("Expected no error, got %v", err)
	}
	if assigned.Name != "Bob" {
		t.Errorf("Expected Bob (only available), got %s", assigned.Name)
	}
}

func TestRequiredSpecialty(t *testing.T) {
	cases := []struct {
		alertType AlertType
		expected  Specialty
	}{
		{Critical, ICU},
		{Warning, Emergency},
		{Info, ""},
	}

	for _, c := range cases {
		got := requiredSpecialty(c.alertType)
		if got != c.expected {
			t.Errorf("requiredSpecialty(%v) = %s; expected %s", c.alertType, got, c.expected)
		}
	}
}

func TestIsSuitable_UnavailableNurse(t *testing.T) {
	n := nurse("Alice", ICU, false, 0)
	if isSuitable(n, Critical) {
		t.Error("Unavailable nurse should not be suitable")
	}
}

func TestIsSuitable_WrongSpecialty(t *testing.T) {
	n := nurse("Alice", General, true, 0)
	if isSuitable(n, Critical) {
		t.Error("General nurse should not be suitable for Critical alert")
	}
}

func TestIsSuitable_MatchingSpecialty(t *testing.T) {
	n := nurse("Alice", ICU, true, 0)
	if !isSuitable(n, Critical) {
		t.Error("ICU nurse should be suitable for Critical alert")
	}
}