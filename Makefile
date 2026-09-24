.PHONY: install lint type-check test build sonar clean

install:
	go mod download

lint:
	golangci-lint run ./...

type-check:
	go vet ./...

test:
	go test -coverprofile=coverage.out -covermode count ./...
	C:\Users\jrego\go\bin\go-bcov.exe -format sonar-cover-report < coverage.out > coverage.xml


build:
	go build -o bin/app.exe .

sonar:
	npx sonar-scanner -Dsonar.qualitygate.wait=true

clean:
	rm -rf bin coverage.out reports .scannerwork
