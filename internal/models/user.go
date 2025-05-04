package models

import (
	"database/sql"
	"time"

	"github.com/google/uuid"
)

type User struct {
	ID           uuid.UUID    `db:"id"`
	Email        string       `db:"email"`
	PasswordHash string       `db:"password_hash"`
	FirstName    string       `db:"first_name"`
	LastName     string       `db:"last_name"`
	ActivatedAt  sql.NullTime `db:"activated_at"`
	VerifiedAt   sql.NullTime `db:"verified_at"`
	CreatedAt    time.Time    `db:"created_at"`
	UpdatedAt    time.Time    `db:"updated_at"`
}

type serializer struct {
	ID         uuid.UUID `json:"id"`
	Email      string    `json:"email"`
	FirstName  string    `json:"firstName"`
	LastName   string    `json:"lastName"`
	IsActive   bool      `json:"isActive"`
	IsVerified bool      `json:"isVerified"`
}

func (u User) IsActive() bool {
	return u.ActivatedAt.Valid
}

func (u User) IsVerified() bool {
	return !u.VerifiedAt.Valid
}

func (u User) Serialized() serializer {
	return serializer{
		ID:         u.ID,
		Email:      u.Email,
		FirstName:  u.FirstName,
		LastName:   u.LastName,
		IsActive:   u.IsActive(),
		IsVerified: u.IsVerified(),
	}
}
