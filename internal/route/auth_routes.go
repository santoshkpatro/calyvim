package route

import (
	"github.com/labstack/echo/v4"
	"github.com/santoshkpatro/calyvim/internal/handler"
	"github.com/santoshkpatro/calyvim/internal/middleware"
)

func RegisterAuthRoutes(e *echo.Echo) {
	authGroup := e.Group("/api/auth")
	{
		authGroup.POST("/login", handler.Login)
		authGroup.POST("/register", handler.Register)
		authGroup.GET("/profile", handler.Profile, middleware.JWTAuth)
	}
}
