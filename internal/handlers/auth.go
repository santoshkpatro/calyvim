package handlers

import (
	"net/http"
	"strings"

	"github.com/labstack/echo/v4"
	"golang.org/x/crypto/bcrypt"
)

type RegisterRequest struct {
	Email    string `json:"email"`
	Password string `json:"password"`
}

func (h *HandlerContext) Login (c echo.Context) error {
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

func (h *HandlerContext) Register (c echo.Context) error {
    var req RegisterRequest
    if err := c.Bind(&req); err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{"error": "Invalid request"})
	}

    req.Email = strings.TrimSpace(req.Email)
	req.Password = strings.TrimSpace(req.Password)

    if req.Email == "" || req.Password == "" {
		return c.JSON(http.StatusBadRequest, map[string]string{"error": "Email and password are required"})
	}

    var count int
	err := h.DB.Get(&count, "SELECT COUNT(1) FROM users WHERE email = $1", req.Email)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]string{"error": "Database error"})
	}
	if count > 0 {
		return c.JSON(http.StatusConflict, map[string]string{"error": "Email already registered"})
	}

    // Hash the password
	hash, err := bcrypt.GenerateFromPassword([]byte(req.Password), bcrypt.DefaultCost)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]string{"error": "Failed to hash password"})
	}

    // Insert the user
	_, err = h.DB.Exec(`
    INSERT INTO users (email, password_hash)
    VALUES ($1, $2)
    `, req.Email, string(hash))

    if err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]string{"error": "Failed to register user"})
	}

    return c.JSON(http.StatusCreated, map[string]string{"message": "User registered successfully"})
}