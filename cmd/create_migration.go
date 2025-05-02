package cmd

import (
	"calyvim/internal/db"
	"fmt"

	"github.com/spf13/cobra"
)

var CreateMigrationCmd = &cobra.Command{
    Use:   "create_migration [name]",
    Short: "Create a new SQL migration",
    Args:  cobra.ExactArgs(1),
    Run: func(cmd *cobra.Command, args []string) {
        if err := db.CreateMigration(args[0]); err != nil {
			fmt.Println("❌", err)
		}
    },
}
