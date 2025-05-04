package main

import (
	"calyvim/cmd"
	"log"

	"github.com/spf13/cobra"
)

var rootCmd = &cobra.Command{
	Use:   "calyvim",
	Short: "Calyvim CLI - manage your app and utilities",
}

func main() {
	// Register all subcommands
	rootCmd.AddCommand(cmd.ServeCmd)
	rootCmd.AddCommand(cmd.CreateMigrationCmd)
	rootCmd.AddCommand(cmd.SetupDatabaseCmd)
	rootCmd.AddCommand(cmd.MigrateCmd)

	if err := rootCmd.Execute(); err != nil {
		log.Fatal(err)
	}
}
