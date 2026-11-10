DOCKER_EXE = C:\Users\jrego\AppData\Local\Programs\DockerDesktop\resources\bin\docker.exe

.PHONY: install lint type-check test test-e2e coverage a11y test-integration build sonar clean

install:
	go mod download

lint:
	golangci-lint run ./...

type-check:
	go vet ./...

test:
	$(DOCKER_EXE) run --rm -v "$(CURDIR):/app" -w /app golang:1.27-alpine sh -c "go test -coverprofile=/tmp/coverage.out ./... > /dev/null && cat /tmp/coverage.out" > coverage.out
	C:\Users\jrego\go\bin\go-bcov.exe -format sonar-cover-report < coverage.out > coverage.xml

test-e2e:
	go test -tags=e2e -v ./...

coverage:
	$(DOCKER_EXE) run --rm -v "$(CURDIR):/app" -w /app golang:1.27-alpine sh -c "go test -coverprofile=/tmp/coverage.out ./... > /dev/null && cat /tmp/coverage.out" > coverage.out
	C:\Users\jrego\go\bin\go-bcov.exe -format sonar-cover-report < coverage.out > coverage.xml

a11y:
	@echo "Accessibility: not applicable to Go"

test-integration:
	@echo "Container integration not applicable"

build:
	go build -o bin/app.exe .

sonar:
	npx sonar-scanner -Dsonar.qualitygate.wait=true

clean:
	rm -rf bin coverage.out coverage.xml reports .scannerwork .gotmp