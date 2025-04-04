package main

import (
	"os"
	"strings"
)

type Config struct {
	Port           string
	DatabasePath   string
	Environment    string
	LogLevel       string
}

func NewConfig() *Config {
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	return &Config{
		Port:         port,
		DatabasePath: os.Getenv("DATABASE_PATH") + ":words.db",
		Environment:  strings.ToLower(os.Getenv("ENVIRONMENT")),
		LogLevel:     strings.ToLower(os.Getenv("LOG_LEVEL")),
	}
}
