package handlers

import (
	"net/http"

	"github.com/labstack/echo/v4"
)

func (h *HandlerContext) HealthCheck(c echo.Context) error {
	return c.JSON(http.StatusOK, map[string]string{
		"status": "ok",
	})
}
