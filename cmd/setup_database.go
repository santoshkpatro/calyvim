package cmd

import (
	"calyvim/internal/db"
	"fmt"
	"log"

	"github.com/joho/godotenv"
	"github.com/spf13/cobra"
)

var SetupDatabaseCmd = &cobra.Command{
    Use:   "setup_database",
    Short: "Create schema_migrations table if it does not exist",
    Run: func(cmd *cobra.Command, args []string) {
		_ = godotenv.Load()
		
        dbConn := db.Connect()
        defer dbConn.Close()

        query := `
        CREATE TABLE IF NOT EXISTS schema_migrations (
            timestamp BIGINT PRIMARY KEY,
            applied_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        `

        if _, err := dbConn.Exec(query); err != nil {
            log.Fatalf("❌ Failed to create schema_migrations table: %v", err)
        }

        fmt.Println("✅ schema_migrations table ensured successfully.")
    },
}
