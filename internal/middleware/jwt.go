package middleware

import (
	"errors"
	"log"
	"net/http"
	"strings"
	"time"

	"github.com/golang-jwt/jwt/v5"
	"github.com/labstack/echo/v4"
	"github.com/santoshkpatro/calyvim/internal/config"
)

// Custom claims structure
type Claims struct {
	UserID string `json:"user_id"`
	jwt.RegisteredClaims
}

func JWTAuth(next echo.HandlerFunc) echo.HandlerFunc {
	return func(c echo.Context) error {
		cfg := config.LoadConfig()

		// Get the Authorization header
		authHeader := c.Request().Header.Get("Authorization")
		if authHeader == "" {
			return echo.NewHTTPError(http.StatusUnauthorized, "missing authorization header")
		}

		// Check if it's a Bearer token
		headerParts := strings.Split(authHeader, " ")
		if len(headerParts) != 2 || headerParts[0] != "Bearer" {
			return echo.NewHTTPError(http.StatusUnauthorized, "invalid authorization header format")
		}

		tokenString := headerParts[1]

		// Parse and validate the token
		token, err := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
			// Validate the signing method
			if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
				return nil, errors.New("unexpected signing method")
			}
			return []byte(cfg.JWTSecretKey), nil
		})

		if err != nil {
			log.Printf("Error parsing token: %v", err)
			return echo.NewHTTPError(http.StatusUnauthorized, "invalid token")
		}

		// Extract claims
		claims, ok := token.Claims.(jwt.MapClaims)
		if !ok || !token.Valid {
			return echo.NewHTTPError(http.StatusUnauthorized, "invalid token claims")
		}

		// Check if token is expired
		if exp, ok := claims["exp"].(float64); ok {
			if float64(time.Now().Unix()) > exp {
				return echo.NewHTTPError(http.StatusUnauthorized, "token has expired")
			}
		}

		// Extract user ID from 'sub' claim and set in context
		if userID, ok := claims["sub"]; ok {
			c.Set("user_id", userID)
		} else {
			return echo.NewHTTPError(http.StatusUnauthorized, "missing user id in token")
		}
		return next(c)
	}
}
