package cmd

import (
	"calyvim/internal/db"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"sort"
	"strconv"
	"strings"
	"time"

	"github.com/joho/godotenv"
	"github.com/spf13/cobra"
)

var MigrateCmd = &cobra.Command{
    Use:   "migrate",
    Short: "Apply pending SQL migrations",
    Run: func(cmd *cobra.Command, args []string) {
		_ = godotenv.Load()
		
        dbConn := db.Connect()
        defer dbConn.Close()

        // 1. Ensure schema_migrations table
        _, err := dbConn.Exec(`
            CREATE TABLE IF NOT EXISTS schema_migrations (
                timestamp BIGINT PRIMARY KEY,
                applied_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
        `)
        if err != nil {
            log.Fatalf("❌ Failed to ensure schema_migrations table: %v", err)
        }

        // 2. Fetch already applied timestamps
        rows, err := dbConn.Query(`SELECT timestamp FROM schema_migrations`)
        if err != nil {
            log.Fatalf("❌ Failed to read applied migrations: %v", err)
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
            log.Fatalf("❌ Failed to read migrations directory: %v", err)
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
                log.Fatalf("❌ Failed to read %s: %v", fname, err)
            }

            fmt.Println("🔁 Applying migration:", fname)
            if _, err := dbConn.Exec(string(content)); err != nil {
                log.Fatalf("❌ Failed to execute %s: %v", fname, err)
            }

            tsStr := strings.SplitN(fname, "_", 2)[0]
            ts, _ := strconv.ParseInt(tsStr, 10, 64)
            _, err = dbConn.Exec(`INSERT INTO schema_migrations (timestamp, applied_at) VALUES ($1, $2)`, ts, time.Now())
            if err != nil {
                log.Fatalf("❌ Failed to record migration %s: %v", fname, err)
            }

            fmt.Println("✅ Applied:", fname)
        }

        fmt.Println("🚀 All pending migrations complete.")
    },
}
