# Stage 1: Build
FROM golang:1.27-alpine AS builder
WORKDIR /app
COPY go.mod ./
# Se tiveres o go.sum, descomenta a linha abaixo
# COPY go.sum ./
RUN go mod download
COPY . .
RUN go build -o main .

# Stage 2: Run
FROM alpine:3.21
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
WORKDIR /app
COPY --from=builder /app/main .
EXPOSE 8080
USER appuser
CMD ["./main"]