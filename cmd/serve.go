package cmd

import (
	"calyvim/internal/db"
	"calyvim/internal/handlers"
	"fmt"
	"os"

	"github.com/joho/godotenv"
	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
	"github.com/spf13/cobra"
)

var ServeCmd = &cobra.Command{
    Use:   "serve",
    Short: "Start the web server",
    Run: func(cmd *cobra.Command, args []string) {
        _ = godotenv.Load()

        dbConn := db.Connect()
        defer dbConn.Close()

        e := echo.New()
        e.Use(middleware.StaticWithConfig(middleware.StaticConfig{
            Root:   "dist",
            Browse: false,
            HTML5:  true,
        }))

        handler := &handlers.HandlerContext{DB: dbConn}
        handler.RegisterRoutes(e)

        port := os.Getenv("PORT")
        if port == "" {
            port = "8080"
        }

        fmt.Println("🚀 Starting server on port", port)
        e.Logger.Fatal(e.Start(":" + port))
    },
}
