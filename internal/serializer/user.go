package serializer

import (
	"calyvim/internal/models"

	"github.com/google/uuid"
)

type UserResponse struct {
	ID         uuid.UUID `json:"id"`
	Email      string    `json:"email"`
	FirstName  string    `json:"firstName"`
	LastName   string    `json:"lastName"`
	IsActive   bool      `json:"isActive"`
	IsVerified bool      `json:"isVerified"`
}

func UserSerializer(u models.User) UserResponse {
	return UserResponse{
		ID:         u.ID,
		Email:      u.Email,
		FirstName:  u.FirstName,
		LastName:   u.LastName,
		IsActive:   u.IsActive(),
		IsVerified: u.IsVerified(),
	}
}
