// Package assignment implements the logic for assigning nurse call alerts

package assignment
import "errors"

// AlertType represents the priority level of a nurse call alert.
type AlertType int

const (
	// Info is a low priority alert (e.g., patient request).
	Info AlertType = iota
	// Warning is a medium priority alert (e.g., patient needs assistance).
	Warning
	// Critical is a high priority alert (e.g., emergency).
	Critical
)

// Alert represents a nurse call event coming from a specific room.
type Alert struct {
	Room string
	Type AlertType
}

// Specialty represents a nurse's area of expertise.
type Specialty string

const (
	// General is a general duty nurse.
	General Specialty = "general"
	// Emergency is an emergency room nurse.
	Emergency Specialty = "emergency"
	// ICU is an intensive care unit nurse.
	ICU Specialty = "icu"
)

// Nurse represents a nurse that can receive alerts.
type Nurse struct {
	Name          string
	Specialty     Specialty
	Available     bool
	AssignedCount int
}

// ErrNoNurseAvailable is returned when no suitable nurse can be assigned.
var ErrNoNurseAvailable = errors.New("no nurse available for this alert")

// requiredSpecialty returns the specialty required for a given alert type.
// If the alert is Info, any specialty is acceptable (returns empty string).
func requiredSpecialty(alertType AlertType) Specialty {
	switch alertType {
	case Critical:
		return ICU
	case Warning:
		return Emergency
	default:
		return "" // any specialty
	}
}

// isSuitable checks if a nurse is suitable for the given alert type.
func isSuitable(nurse Nurse, alertType AlertType) bool {
	if !nurse.Available {
		return false
	}
	required := requiredSpecialty(alertType)
	if required == "" {
		return true // Info alerts accept any specialty
	}
	return nurse.Specialty == required
}

// Assign finds the most appropriate nurse for the given alert.
//
// The selection criteria, in order:
//  1. Nurse must be available
//  2. Nurse must have the required specialty (or any specialty for Info alerts)
//  3. Nurse with the lowest AssignedCount is preferred (load balancing)
//
// Returns the selected nurse and a nil error on success.
// Returns an empty nurse and ErrNoNurseAvailable if no suitable nurse is found.
func Assign(alert Alert, nurses []Nurse) (Nurse, error) {
	var best *Nurse

	for i := range nurses {
		nurse := nurses[i]
		if !isSuitable(nurse, alert.Type) {
			continue
		}
		if best == nil || nurse.AssignedCount < best.AssignedCount {
			best = &nurses[i]
		}
	}

	if best == nil {
		return Nurse{}, ErrNoNurseAvailable
	}

	// Increment the assigned count on the original slice
	best.AssignedCount++

	return *best, nil
}