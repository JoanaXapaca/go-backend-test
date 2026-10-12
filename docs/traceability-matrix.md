Traceability Matrix



Project: Go Backend Test

Standard: ISO 13485:2016 — SOP 7.3.2 + 7.3.5



Requirement -> Test Matrix

| Requirement | Description | Test | File | Status |

| REQ-01 | Integer addition | TestAdd | main\_test.go | OK |

| REQ-01 | Addition edge cases | TestAddEdgeCases | main\_test.go | OK |

| REQ-02 | Integer subtraction | TestSubtract | main\_test.go | OK |

| REQ-02 | Subtraction edge cases | TestSubtractEdgeCases | main\_test.go | OK |

| REQ-03 | Main execution | TestMain | main\_test.go | OK |

| NFR-01 | Coverage >= 80% | go test -coverprofile | Pipeline | 100% |

| NFR-02 | Quality Gate | SonarQube | Pipeline | OK |

| REG-01 | Traceability | HTML report | gerar\_relatorio.py | OK |

| REG-03 | Audit records | archiveArtifacts | Jenkinsfile | OK |



E2E Tests

| ID | Test | File | Status |

| E2E-01 | Build compiles the binary | main\_e2e\_test.go | OK |

| E2E-02 | Binary outputs "Add 2+3 = 5" | main\_e2e\_test.go | OK |

| E2E-03 | Binary outputs "Subtract 10-4 = 6" | main\_e2e\_test.go | OK |



References

\- ISO 13485:2016 sec. 7.3.2 (Inputs) and sec. 7.3.5 (Verification)

\- Quality Manual GlobeStar v01.47

