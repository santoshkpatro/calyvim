package middlewares

import (
	"calyvim/internal/utils"
	"net/http"

	"github.com/labstack/echo/v4"
)

func CookieAuthMiddleware(next echo.HandlerFunc) echo.HandlerFunc {
	return func(c echo.Context) error {
		cookie, err := c.Cookie("session_id")
		if err != nil || cookie.Value == "" {
			return utils.ResponseError(c, http.StatusUnauthorized, "Unauthorized access", nil)
		}

		// Optionally: validate cookie.Value (e.g., check in DB)
		c.Set("user_id", cookie.Value)

		return next(c)
	}
}
