# Stage 1: Builder
FROM golang:1.20-alpine AS builder

WORKDIR /app

# Copy go.mod and go.sum, then download modules
COPY go.mod go.sum ./
RUN go mod download

COPY . .

# Build the application
RUN go build -o server ./cmd/server

# Stage 2: Final (runtime)
FROM alpine:3.17

RUN apk --no-cache add ca-certificates

WORKDIR /app

COPY --from=builder /app/server .
COPY db/ ./db

EXPOSE 8080

ENV BACKEND_PORT=8080

CMD ["./server"] 