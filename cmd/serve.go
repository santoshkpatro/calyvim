package cmd

import (
	"calyvim/internal/server"

	"github.com/spf13/cobra"
)

var ServeCmd = &cobra.Command{
    Use:   "serve",
    Short: "Start the web server",
    Run: func(cmd *cobra.Command, args []string) {
		server.StartServer()
	},
}
