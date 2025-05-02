package cmd

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"time"

	"github.com/spf13/cobra"
)

var CreateMigrationCmd = &cobra.Command{
    Use:   "create_migration [name]",
    Short: "Create a new SQL migration",
    Args:  cobra.ExactArgs(1),
    Run: func(cmd *cobra.Command, args []string) {
        name := args[0]
        timestamp := time.Now().Unix()
        safeName := strings.ToLower(strings.ReplaceAll(name, " ", "_"))
        fileName := fmt.Sprintf("%d_%s.sql", timestamp, safeName)
        fullPath := filepath.Join("migrations", fileName)

        os.MkdirAll("migrations", 0755)
        content := fmt.Sprintf("-- migration: %s\n\n", name)
        _ = os.WriteFile(fullPath, []byte(content), 0644)

        fmt.Println("✅ Created migration:", fullPath)
    },
}
