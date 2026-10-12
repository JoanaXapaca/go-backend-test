\# Go Backend Test



Go demonstration project for the CI/CD pipeline, used as a base to replicate across other technologies.



\## Pipeline



Runs on Jenkins, with the following stages:



1\. Checkout — clones the Git repository

2\. Install — `go mod download`

3\. Lint — `golangci-lint run ./...`

4\. Type-check — `go vet ./...`

5\. Unit Tests — `go test -coverprofile=coverage.out -covermode count ./...` + `go-bcov`

6\. E2E Tests — `go test -tags=e2e -v ./...`

7\. SonarQube — `sonar-scanner -Dsonar.qualitygate.wait=true`

8\. Build — `go build -o bin/app.exe .`

9\. Audit Report — `python scripts/gerar\_relatorio.py`



Trigger: Poll SCM every 5 minutes. Every push to the `main` branch triggers the pipeline.



\## Running locally



Requirements: Go 1.27+, `golangci-lint`, `go-bcov`.



Installation:



```bash

go mod download


Commands:

Command	What it does
make install	Downloads dependencies
make lint	Runs golangci-lint
make type-check	Runs go vet
make test	Runs unit tests + coverage
make test-e2e	Runs E2E tests
make build	Builds the binary to bin/app.exe
make clean	Removes build artifacts

Before pushing, run:
make lint
make type-check
make test
make build

Interpreting results
Jenkins:

Green: pipeline passed

Red: some stage failed; check Console Output

Artifacts: bin/ and reports/ archived on each build

SonarQube:

Dashboard: http://localhost:9000/dashboard?id=go-backend-test

Quality Gate must be Passed

Coverage is read from coverage.xml

Stack
Layer	Technology
Language	Go 1.27
Lint	golangci-lint
Type-check	go vet
Tests	go test + go-bcov
CI/CD	Jenkins
Static analysis	SonarQube

Structure
go-backend-test/
├── Jenkinsfile
├── Makefile
├── sonar-project.properties
├── main.go
├── main_test.go
├── main_e2e_test.go
├── scripts/
│   └── gerar_relatorio.py
├── docs/
│   ├── design-development-plan.md
│   ├── requirements.md
│   ├── traceability-matrix.md
│   ├── qms-software-validation.md
│   ├── validation-plan.md
│   └── design-file/
│       └── README.md
├── bin/         (generated)
└── reports/     (generated)

Notes
go-bcov is used to convert Go coverage to SonarQube's generic format.

The coverage report is written to coverage.xml.

SonarQube runs on http://127.0.0.1:9000 (IPv4, to avoid WSL relay conflicts on Windows).

The Sonar token is read from C:\Users\jrego\sonar-token.txt.

Quality Gate is enforced with sonar.qualitygate.wait=true (no webhook needed in localhost).