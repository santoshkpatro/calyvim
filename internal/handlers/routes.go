package handlers

import (
	"net/http"

	"github.com/labstack/echo/v4"
)

func (h *HandlerContext) RegisterRoutes(e *echo.Echo) {
	api := e.Group("/api")

	// Base health and root check
	api.GET("/", func(c echo.Context) error {
		return c.String(http.StatusOK, "Welcome to Calyvim API")
	})

	// Auth routes
	api.GET("/login", h.Login)
	api.POST("/register", h.Register)

	// Health check route
	api.GET("/health", h.HealthCheck)
}
