package models

import "time"

type User struct {
	ID           int       `db:"id" json:"id"`
	FirstName    string    `db:"first_name" json:"firstName"`
	LastName     string    `db:"last_name" json:"lastName"`
	Email        string    `db:"email" json:"email"`
	Password     string    `db:"password" json:"-"`
	PasswordHash string    `db:"password_hash" json:"-"`
	IsActive     bool      `db:"is_active" json:"isActive"`
	IsAdmin      bool      `db:"is_admin" json:"isAdmin"`
	CreatedAt    time.Time `db:"created_at" json:"createdAt"`
	UpdatedAt    time.Time `db:"updated_at" json:"updatedAt"`
}
