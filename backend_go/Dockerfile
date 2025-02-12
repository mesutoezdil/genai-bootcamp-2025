FROM golang:1.21-alpine
WORKDIR /app
COPY . .
RUN go mod init myapp && go mod tidy && go get github.com/gin-gonic/gin
RUN go build -o main .
EXPOSE 8080
CMD ["./main"]
