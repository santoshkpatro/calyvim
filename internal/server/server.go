package server

import (
	"calyvim/internal/cache"
	"calyvim/internal/db"
	"calyvim/internal/handlers"
	"fmt"
	"os"

	"github.com/joho/godotenv"
	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
)

func StartServer() {
	_ = godotenv.Load()

	dbConn := db.Connect()
	defer dbConn.Close()

	redisConn := cache.Connect()
	defer redisConn.Close()

	e := echo.New()
	e.Use(middleware.StaticWithConfig(middleware.StaticConfig{
		Root:   "dist",
		Browse: false,
		HTML5:  true,
	}))

	handler := &handlers.HandlerContext{DB: dbConn, Cache: redisConn}
	handler.RegisterRoutes(e)

	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	fmt.Println("🚀 Starting server on port", port)
	e.Logger.Fatal(e.Start(":" + port))
}
