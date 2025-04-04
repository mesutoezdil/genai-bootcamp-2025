package database

import (
	"database/sql"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"path/filepath"
	"strings"
)

func Migrate(db *sql.DB) error {
	migrationDir := "migrations"
	files, err := ioutil.ReadDir(migrationDir)
	if err != nil {
		return fmt.Errorf("failed to read migration directory: %w", err)
	}

	// Sort files by name to ensure proper order
	var migrationFiles []os.FileInfo
	for _, file := range files {
		if strings.HasSuffix(file.Name(), ".sql") {
			migrationFiles = append(migrationFiles, file)
		}
	}

	for _, file := range migrationFiles {
		filePath := filepath.Join(migrationDir, file.Name())
		content, err := ioutil.ReadFile(filePath)
		if err != nil {
			return fmt.Errorf("failed to read migration file %s: %w", file.Name(), err)
		}

		sqlStatements := strings.Split(string(content), ";")
		for _, stmt := range sqlStatements {
			stmt = strings.TrimSpace(stmt)
			if stmt == "" {
				continue
			}

			_, err := db.Exec(stmt)
			if err != nil {
				return fmt.Errorf("failed to execute migration statement: %w", err)
			}
		}

		log.Printf("Successfully executed migration: %s", file.Name())
	}

	return nil
}
