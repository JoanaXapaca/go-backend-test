# Stage 1: Build
FROM golang:1.27-alpine AS builder
WORKDIR /app
COPY go.mod ./
RUN go mod download
COPY . .
RUN go build -o main .

# Stage 2: Run (Non-root for security)
FROM alpine:3.21
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
WORKDIR /app
COPY --from=builder /app/main .
EXPOSE 8081
USER appuser
CMD ["./main"]