package main

import (
	"calyvim/internal/db"
	"calyvim/internal/handlers"
	"log"
	"os"

	"github.com/joho/godotenv"
	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
)

func main() {
	// Load .env
    if err := godotenv.Load(); err != nil {
        log.Println("No .env file found, using system environment.")
    }

	e := echo.New()

	// DB Connect
    dbConn := db.Connect()
	defer dbConn.Close()

	// Static file middleware
    e.Use(middleware.StaticWithConfig(middleware.StaticConfig{
        Root:   "dist", // serves files from ./dist/
		Browse: false,           // Optional: prevent directory listing in production
		HTML5:  true,            // Important: serves index.html for SPA routing (like Vue router)
    }))

	// Handler Context
	handler := &handlers.HandlerContext{DB: dbConn}

    // Register all routes under /api
    handler.RegisterRoutes(e)

    port := os.Getenv("PORT")
    if port == "" {
        port = "8080"
    }

    e.Logger.Fatal(e.Start(":" + port))
}
