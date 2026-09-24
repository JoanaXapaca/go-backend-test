.PHONY: install lint type-check test build sonar clean

install:
	go mod download

lint:
	golangci-lint run ./...

type-check:
	go vet ./...

test:
	go test -coverprofile=coverage.out ./...
	powershell -Command "(Get-Content coverage.out) -replace 'github.com/JoanaXapaca/go-backend-test/', '' | Set-Content coverage.out"


build:
	go build -o bin/app.exe .

sonar:
	npx sonar-scanner -Dsonar.qualitygate.wait=true

clean:
	rm -rf bin coverage.out reports .scannerwork
