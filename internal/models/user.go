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

func (u User) IsActive() bool {
	return u.ActivatedAt.Valid
}

func (u User) IsVerified() bool {
	return !u.VerifiedAt.Valid
}
