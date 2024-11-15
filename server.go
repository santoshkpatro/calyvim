package main

import (
	"net/http"
	"os"

	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
	"github.com/santoshkpatro/calyvim/cmd"
	"github.com/santoshkpatro/calyvim/internal/route"
)

func main() {
	// Check if the first argument is a CLI command
	if len(os.Args) > 1 {
		cmd.Execute() // Run the CLI commands
		return
	}

	e := echo.New()

	e.Use(middleware.LoggerWithConfig(middleware.LoggerConfig{
		Format: "method=${method}, uri=${uri}, status=${status}\n",
	}))

	e.GET("/up", func(c echo.Context) error {
		return c.String(http.StatusOK, "All good!")
	})

	route.RegisterAuthRoutes(e)
	route.RegisterInvoiceRoutes(e)

	e.Use(middleware.StaticWithConfig(middleware.StaticConfig{
		Root:   "dist",
		Browse: false,
		HTML5:  true,
	}))

	e.Logger.Fatal(e.Start(":8000"))
}
