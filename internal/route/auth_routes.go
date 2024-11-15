package route

import (
	"github.com/labstack/echo/v4"
	"github.com/santoshkpatro/calyvim/internal/handler"
)

func RegisterAuthRoute(e *echo.Echo) {
	authGroup := e.Group("/api/auth")
	{
		authGroup.POST("/login", handler.Login)
	}
}
