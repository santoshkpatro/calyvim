package db

import (
	"fmt"
	"os"
	"path/filepath"
	"sort"
	"strconv"
	"strings"
	"time"
)

func CreateMigration(name string) error {
	timestamp := time.Now().Unix()
	safeName := strings.ToLower(strings.ReplaceAll(name, " ", "_"))
	fileName := fmt.Sprintf("%d_%s.sql", timestamp, safeName)
	fullPath := filepath.Join("migrations", fileName)

	if err := os.MkdirAll("migrations", 0755); err != nil {
		return fmt.Errorf("failed to create migrations folder: %w", err)
	}

	content := fmt.Sprintf("-- migration: %s\n\n", name)
	if err := os.WriteFile(fullPath, []byte(content), 0644); err != nil {
		return fmt.Errorf("failed to write migration file: %w", err)
	}

	fmt.Println("✅ Created migration:", fullPath)
	return nil
}

func SetupDatabase() error {
	dbConn := Connect()
	defer dbConn.Close()

	query := `
	CREATE TABLE IF NOT EXISTS schema_migrations (
		timestamp BIGINT PRIMARY KEY,
		applied_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
	);`

	if _, err := dbConn.Exec(query); err != nil {
		return fmt.Errorf("failed to create schema_migrations table: %w", err)
	}

	return nil
}

func ApplyMigrations() error {
	dbConn := Connect()
	defer dbConn.Close()

	// 1. Ensure schema_migrations table
	_, err := dbConn.Exec(`
		CREATE TABLE IF NOT EXISTS schema_migrations (
			timestamp BIGINT PRIMARY KEY,
			applied_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
		);
	`)
	if err != nil {
		return fmt.Errorf("failed to ensure schema_migrations table: %w", err)
	}

	// 2. Fetch already applied timestamps
	rows, err := dbConn.Query(`SELECT timestamp FROM schema_migrations`)
	if err != nil {
		return fmt.Errorf("failed to read applied migrations: %w", err)
	}
	defer rows.Close()

	applied := make(map[int64]bool)
	for rows.Next() {
		var ts int64
		_ = rows.Scan(&ts)
		applied[ts] = true
	}

	// 3. Scan all .sql files
	entries, err := os.ReadDir("migrations")
	if err != nil {
		return fmt.Errorf("failed to read migrations directory: %w", err)
	}

	var pending []string
	for _, entry := range entries {
		if entry.IsDir() || !strings.HasSuffix(entry.Name(), ".sql") {
			continue
		}

		parts := strings.SplitN(entry.Name(), "_", 2)
		if len(parts) < 2 {
			continue
		}

		ts, err := strconv.ParseInt(parts[0], 10, 64)
		if err != nil {
			continue
		}

		if !applied[ts] {
			pending = append(pending, entry.Name())
		}
	}

	sort.Strings(pending)

	// 4. Apply each pending file
	for _, fname := range pending {
		fullPath := filepath.Join("migrations", fname)
		content, err := os.ReadFile(fullPath)
		if err != nil {
			return fmt.Errorf("failed to read %s: %w", fname, err)
		}

		fmt.Println("🔁 Applying migration:", fname)
		if _, err := dbConn.Exec(string(content)); err != nil {
			return fmt.Errorf("failed to execute %s: %w", fname, err)
		}

		tsStr := strings.SplitN(fname, "_", 2)[0]
		ts, _ := strconv.ParseInt(tsStr, 10, 64)
		_, err = dbConn.Exec(`INSERT INTO schema_migrations (timestamp, applied_at) VALUES ($1, $2)`, ts, time.Now())
		if err != nil {
			return fmt.Errorf("failed to record migration %s: %w", fname, err)
		}

		fmt.Println("✅ Applied:", fname)
	}

	fmt.Println("🚀 All pending migrations complete.")
	return nil
}
