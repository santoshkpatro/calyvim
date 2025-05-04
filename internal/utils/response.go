package utils

import (
	"net/http"

	"github.com/labstack/echo/v4"
)

func ResponseOK(c echo.Context, data interface{}, message string) error {
	return c.JSON(http.StatusOK, map[string]interface{}{
		"ok":      true,
		"data":    data,
		"error":   nil,
		"message": message,
	})
}

func ResponseError(c echo.Context, status int, message string, err error) error {
	var errStr string
	if err != nil {
		errStr = err.Error()
	}
	return c.JSON(status, map[string]interface{}{
		"ok":      false,
		"data":    nil,
		"error":   errStr,
		"message": message,
	})
}
