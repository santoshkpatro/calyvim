package handler

import (
	"log"
	"net/http"
	"time"

	"github.com/golang-jwt/jwt/v5"
	"github.com/labstack/echo/v4"
	"github.com/santoshkpatro/calyvim/internal/config"
	"github.com/santoshkpatro/calyvim/internal/db"
	"github.com/santoshkpatro/calyvim/internal/models"
	"golang.org/x/crypto/bcrypt"
)

type RegisterRequest struct {
	FirstName string `json:"firstName"`
	LastName  string `json:"lastName"`
	Password  string `json:"password"`
	Email     string `json:"email"`
}

type LoginRequest struct {
	Email    string `json:"email"`
	Password string `json:"password"`
}

func Login(c echo.Context) error {
	var req LoginRequest
	if err := c.Bind(&req); err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{"error": "Invalid input"})
	}

	// Check if user exists
	var user models.User
	dbConn := db.GetDBConnection()
	defer dbConn.Close()

	err := dbConn.QueryRow("SELECT id, email, password_hash FROM users WHERE email = $1", req.Email).Scan(&user.ID, &user.Email, &user.PasswordHash)
	if err != nil {
		log.Println("Error fetching user:", err)
		return c.JSON(http.StatusUnauthorized, map[string]string{"error": "Invalid username or password"})
	}

	// Compare passwords
	err = bcrypt.CompareHashAndPassword([]byte(user.PasswordHash), []byte(req.Password))
	if err != nil {
		return c.JSON(http.StatusUnauthorized, map[string]string{"error": "Invalid username or password"})
	}

	// Create JWT token
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
		"sub": user.ID,
		"iat": time.Now().Unix(),
		"exp": time.Now().Add(time.Hour * 24).Unix(), // token expires in 24 hours
	})

	cfg := config.LoadConfig()

	tokenString, err := token.SignedString([]byte(cfg.JWTSecretKey))
	if err != nil {
		log.Println("Error creating JWT token:", err)
		return c.JSON(http.StatusInternalServerError, map[string]string{"error": "Internal server error"})
	}

	// Return the JWT token
	return c.JSON(http.StatusOK, map[string]string{"token": tokenString})
}

func Register(c echo.Context) error {
	var req RegisterRequest
	if err := c.Bind(&req); err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{"error": "Invalid input"})
	}

	// Hash password
	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(req.Password), bcrypt.DefaultCost)
	if err != nil {
		log.Println("Error hashing password:", err)
		return c.JSON(http.StatusInternalServerError, map[string]string{"error": "Internal server error"})
	}

	// Save the user to the database
	user := models.User{
		Email:     req.Email,
		Password:  string(hashedPassword),
		FirstName: req.FirstName,
		LastName:  req.LastName,
	}

	dbConn := db.GetDBConnection()
	defer dbConn.Close()

	_, err = dbConn.Exec("INSERT INTO users (email, password_hash, first_name, last_name) VALUES ($1, $2, $3, $4)", user.Email, user.Password, user.FirstName, user.LastName)
	if err != nil {
		log.Println("Error inserting user into the database:", err)
		return c.JSON(http.StatusInternalServerError, map[string]string{"error": "Internal server error"})
	}

	createdUser := models.User{}
	err = dbConn.Get(&createdUser, "SELECT * FROM users WHERE email=$1", user.Email)

	if err != nil {
		log.Println("Error :", err)
		return c.JSON(http.StatusInternalServerError, map[string]string{"error": "Internal server error"})
	}

	// Return success message
	return c.JSON(http.StatusCreated, createdUser)
}

func Profile(c echo.Context) error {
	// fmt.Println(c.Get("user_id"))
	user := models.User{}

	dbConn := db.GetDBConnection()
	defer dbConn.Close()

	err := dbConn.Get(&user, "SELECT * FROM users WHERE id = $1", c.Get("user_id"))
	if err != nil {
		log.Println("Error :", err)
		return c.JSON(http.StatusInternalServerError, map[string]string{"error": "Internal server error"})
	}

	return c.JSON(http.StatusOK, user)
}
