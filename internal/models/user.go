package models

import "github.com/google/uuid"

type User struct {
	ID        uuid.UUID `json:"id" db:"id"`
	Email     string    `json:"email" db:"email"`
	FirstName string    `json:"firstName" db:"first_name"`
	LastName  string    `json:"lastName" db:"last_name"`
	IsActive  bool      `json:"isActive" db:"is_active"`
}
