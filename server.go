package main

import (
	"net/http"
	"os"

	"github.com/labstack/echo/v4"
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

	e.GET("/up", func(c echo.Context) error {
		return c.String(http.StatusOK, "All good!")
	})

	route.RegisterAuthRoute(e)

	e.Logger.Fatal(e.Start(":8000"))
}
