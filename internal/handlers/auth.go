package handlers

import (
	"net/http"

	"github.com/labstack/echo/v4"
)

func (a *HandlerContext) Login (c echo.Context) error {
	// Dummy credentials (in real case, you'd parse JSON or form input)
    username := c.QueryParam("username")
    password := c.QueryParam("password")

    // Dummy validation
    if username == "admin" && password == "secret" {
        return c.JSON(http.StatusOK, map[string]string{
            "message": "Login successful",
            "token":   "dummy-jwt-token",
        })
    }

    return c.JSON(http.StatusUnauthorized, map[string]string{
        "error": "invalid credentials",
    })
}