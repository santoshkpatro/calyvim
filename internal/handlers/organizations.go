package handlers

import (
	"calyvim/internal/models"
	"calyvim/internal/utils"
	"net/http"

	"github.com/google/uuid"
	"github.com/labstack/echo/v4"
)

type organizationCreateRequest struct {
	Name string `json:"name" validate:"required"`
	Slug string `json:"slug" validate:"required"`
}

func (h *HandlerContext) ListOrganizations(c echo.Context) error {
	organizations := []models.Organization{}
	err := h.DB.Select(&organizations, `
		SELECT o.*
		FROM organizations o
		JOIN organization_memberships om ON om.organization_id = o.id
		WHERE om.user_id = $1;
	`, c.Get("user_id").(string))

	if err != nil {
		return utils.ResponseError(c, http.StatusBadGateway, "Something wen't wrong", err)
	}

	data := make([]models.OrganizationSerializer, 0, len(organizations))
	for _, org := range organizations {
		data = append(data, org.Serialized())
	}

	return utils.ResponseOK(c, data, "Successfull")
}

func (h *HandlerContext) CreateOrganization(c echo.Context) error {
	var req organizationCreateRequest
	if err := c.Bind(&req); err != nil {
		return utils.ResponseError(c, http.StatusBadRequest, "Invalid Request", err)
	}

	if err := validate.Struct(req); err != nil {
		return utils.ResponseError(c, http.StatusBadRequest, "Validation error", err)
	}

	userId := c.Get("user_id").(string)

	tx := h.DB.MustBegin()
	var orgID uuid.UUID

	err := tx.QueryRowx(
		"INSERT INTO organizations (name, slug, owner_id) VALUES ($1, $2, $3) RETURNING id",
		req.Name, req.Slug, userId,
	).Scan(&orgID)

	if err != nil {
		tx.Rollback()
		return utils.ResponseError(c, http.StatusInternalServerError, "Failed to create organization", err)
	}

	_, err = tx.Exec(
		"INSERT INTO organization_memberships (organization_id, user_id, role) VALUES ($1, $2, $3)",
		orgID, userId, "owner",
	)
	if err != nil {
		tx.Rollback()
		return utils.ResponseError(c, http.StatusInternalServerError, "Failed to add membership", err)
	}

	if err := tx.Commit(); err != nil {
		return utils.ResponseError(c, http.StatusInternalServerError, "Transaction failed", err)
	}

	var org models.Organization
	err = h.DB.Get(&org, "SELECT * FROM organizations WHERE id = $1", orgID)
	if err != nil {
		return utils.ResponseError(c, http.StatusInternalServerError, "Failed to fetch organization", err)
	}

	return utils.ResponseOK(c, org, "Successfull")
}
