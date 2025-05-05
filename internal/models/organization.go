package models

import (
	"time"

	"github.com/google/uuid"
)

type Organization struct {
	ID        uuid.UUID `db:"id"`
	Name      string    `db:"name"`
	Slug      string    `db:"slug"`
	OwnerID   uuid.UUID `db:"owner_id"`
	CreatedAt time.Time `db:"created_at"`
	UpdatedAt time.Time `db:"updated_at"`
}

type OrganizationSerializer struct {
	ID        uuid.UUID `json:"id"`
	Name      string    `json:"name"`
	Slug      string    `json:"slug"`
	OwnerID   uuid.UUID `json:"owner_id"`
	CreatedAt time.Time `json:"created_at"`
}

func (org Organization) Serialized() OrganizationSerializer {
	return OrganizationSerializer{
		ID:        org.ID,
		Name:      org.Name,
		Slug:      org.Slug,
		OwnerID:   org.OwnerID,
		CreatedAt: org.CreatedAt,
	}
}
