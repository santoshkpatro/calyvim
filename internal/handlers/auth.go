package handlers

import (
	"calyvim/internal/models"
	"calyvim/internal/utils"
	"net/http"
	"strings"
	"time"

	"github.com/go-playground/validator/v10"
	"github.com/labstack/echo/v4"
	"golang.org/x/crypto/bcrypt"
)

type RegisterRequest struct {
	Email     string `json:"email"`
	Password  string `json:"password"`
	FirstName string `json:"firstName"`
	LastName  string `json:"lastName"`
}

type LoginRequest struct {
	Email    string `json:"email" validate:"required,email"`
	Password string `json:"password" validate:"required"`
}

var validate = validator.New()

func (h *HandlerContext) Login(c echo.Context) error {
	var req LoginRequest
	if err := c.Bind(&req); err != nil {
		return utils.ResponseError(c, http.StatusBadRequest, "Invalid Request", err)
	}

	if err := validate.Struct(req); err != nil {
		return utils.ResponseError(c, http.StatusBadRequest, "Validation error", err)
	}

	var storedHash string
	err := h.DB.Get(&storedHash, "SELECT password_hash FROM users WHERE email = $1", req.Email)
	if err != nil {
		return c.JSON(http.StatusUnauthorized, map[string]string{"error": "Invalid credentials"})
	}

	// Compare password
	if err := bcrypt.CompareHashAndPassword([]byte(storedHash), []byte(req.Password)); err != nil {
		return c.JSON(http.StatusUnauthorized, map[string]string{"error": "Invalid credentials"})
	}

	userData := models.User{}
	err = h.DB.Get(&userData, "SELECT id, email, first_name, last_name, is_active FROM users WHERE email=$1", req.Email)
	if err != nil {
		return utils.ResponseError(c, http.StatusBadGateway, "Something wen't wrong", err)
	}

	// Set cookie
	cookie := new(http.Cookie)
	cookie.Name = "session_id"
	cookie.Value = userData.ID.String()
	cookie.Path = "/"
	cookie.HttpOnly = true
	cookie.Secure = false // Set to true in production with HTTPS
	cookie.Expires = time.Now().Add(24 * time.Hour)

	c.SetCookie(cookie)

	return utils.ResponseOK(c, userData, "Login Successfull")
}

func (h *HandlerContext) Register(c echo.Context) error {
	var req RegisterRequest
	if err := c.Bind(&req); err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{"error": "Invalid request"})
	}

	req.Email = strings.TrimSpace(req.Email)
	req.Password = strings.TrimSpace(req.Password)

	if req.Email == "" || req.Password == "" || req.FirstName == "" {
		return c.JSON(http.StatusBadRequest, map[string]string{"error": "Email and password and First Name are required"})
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
    INSERT INTO users (email, password_hash, first_name, last_name)
    VALUES ($1, $2, $3, $4)
    `, req.Email, string(hash), req.FirstName, req.LastName)

	if err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]string{"error": "Failed to register user"})
	}

	return c.JSON(http.StatusCreated, map[string]string{"message": "User registered successfully"})
}

func (h *HandlerContext) Profile(c echo.Context) error {
	userID := c.Get("user_id").(string)

	var user models.User
	err := h.DB.Get(&user, "SELECT id, email, first_name, last_name, is_active FROM users WHERE id = $1", userID)
	if err != nil {
		return utils.ResponseError(c, http.StatusBadGateway, "Something wen't wrong", err)
	}

	return utils.ResponseOK(c, user, "Profile fetched successfully")
}
