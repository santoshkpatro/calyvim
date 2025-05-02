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

		if err := db.SetupDatabase(); err != nil {
			log.Fatalf("❌ %v", err)
		}

		fmt.Println("✅ schema_migrations table ensured successfully.")
    },
}
