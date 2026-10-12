Design Validation Plan



Project: Go Backend Test

Standard: ISO 13485:2016 - SOP 7.3.6



1\. Objective

Validate that the software meets user requirements in a simulated environment. The real clinical environment is out of scope.



2\. Validation Environment

| Item | Description |

| Operating system | Windows 11 |

| Runtime | Go 1.27 |

| User | Developer / QA |

| Scenario | Run the binary and verify the output |



3\. E2E Tests

| ID | Test | Scenario | Acceptance Criterion |

| E2E-001 | Compilation | go build | Binary generated without errors |

| E2E-002 | Execution | ./app.exe | Output contains "Add 2+3 = 5" |

| E2E-003 | Execution | ./app.exe | Output contains "Subtract 10-4 = 6" |



4\. Limitations

Validation in a real clinical environment is not applicable to this pipeline test project. The real product, ConnexALL, is validated at the customer site.

