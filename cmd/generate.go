package cmd

import (
	"fmt"
	"os"
	"path/filepath"
	"time"

	"github.com/spf13/cobra"
)

var generateCmd = &cobra.Command{
	Use:   "generate [name]",
	Short: "Generate migration files",
	Args:  cobra.ExactArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		name := args[0]
		timestamp := time.Now().Format("20060102150405")

		migrationFile := filepath.Join("internal", "db", "migrations", fmt.Sprintf("%s_%s.sql", timestamp, name))

		if err := os.MkdirAll("migrations", os.ModePerm); err != nil {
			fmt.Printf("Failed to create migrations folder: %v\n", err)
			return
		}

		if _, err := os.Create(migrationFile); err != nil {
			fmt.Printf("Failed to create %s: %v\n", migrationFile, err)
			return
		}

		fmt.Printf("Migration file created: %s\n", migrationFile)
	},
}

func init() {
	rootCmd.AddCommand(generateCmd)
}
