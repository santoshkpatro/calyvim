package cmd

import (
	"calyvim/internal/db"
	"fmt"
	"log"

	"github.com/joho/godotenv"
	"github.com/spf13/cobra"
)

var MigrateCmd = &cobra.Command{
    Use:   "migrate",
    Short: "Apply pending SQL migrations",
    Run: func(cmd *cobra.Command, args []string) {
        _ = godotenv.Load()

		if err := db.ApplyMigrations(); err != nil {
			log.Fatalf("❌ %v", err)
		} else {
			fmt.Println("🎉 Migration run completed successfully.")
		}
    },
}
