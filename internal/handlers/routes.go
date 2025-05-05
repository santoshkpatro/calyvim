package handlers

import (
	"calyvim/internal/middlewares"

	"github.com/labstack/echo/v4"
)

func (h *HandlerContext) RegisterRoutes(e *echo.Echo) {
	api := e.Group("/api")

	// Public routes (unauthenticated)
	public := api.Group("")

	// Protected routes (authenticated)
	auth := api.Group("")
	auth.Use(middlewares.CookieAuthMiddleware) // Or JWT, etc.

	// Auth routes
	public.POST("/login", h.Login)
	public.POST("/register", h.Register)
	auth.GET("/profile", h.Profile)

	// Health check route
	public.GET("/health", h.HealthCheck)

	// Organizations
	auth.GET("/organizations", h.ListOrganizations)
	auth.POST("/organizations", h.CreateOrganization)
}
