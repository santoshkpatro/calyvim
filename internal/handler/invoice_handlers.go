package handler

import (
	"log"
	"net/http"

	"github.com/labstack/echo/v4"
	"github.com/santoshkpatro/calyvim/internal/db"
	"github.com/santoshkpatro/calyvim/internal/models"
)

type InvoiceCreateRequest struct {
	InvoiceType   string `json:"invoiceType"`
	InvoiceNumber string `json:"invoiceNumber"`
	OrderName     string `json:"orderName"`
}

func GetInvoices(c echo.Context) error {
	dbConn := db.GetDBConnection()

	invoices := []models.Invoice{}

	err := dbConn.Select(&invoices, "SELECT * FROM invoices WHERE user_id = $1 AND is_archived = false", c.Get("user_id"))

	if err != nil {
		log.Println("Error :", err)
		return c.JSON(http.StatusInternalServerError, map[string]string{"error": "Internal server error"})
	}

	return c.JSON(http.StatusOK, invoices)
}

func CreateInvoice(c echo.Context) error {
	// Parse the incoming request payload
	req := new(InvoiceCreateRequest)
	if err := c.Bind(req); err != nil {
		log.Println("Error binding request:", err)
		return c.JSON(http.StatusBadRequest, map[string]string{"error": "Invalid request payload"})
	}

	// Ensure InvoiceType defaults to "standard" if not provided
	if req.InvoiceType == "" {
		req.InvoiceType = "standard"
	}

	// Insert the new invoice into the database
	query := `
		INSERT INTO invoices (user_id, invoice_type, invoice_number, order_name, issue_date, payment_status)
		VALUES ($1, $2, $3, $4, CURRENT_DATE, 'unpaid')
		RETURNING id
	`

	dbConn := db.GetDBConnection()

	var invoiceID int
	err := dbConn.QueryRow(query, c.Get("user_id"), req.InvoiceType, req.InvoiceNumber, req.OrderName).Scan(&invoiceID)
	if err != nil {
		log.Println("Error inserting invoice:", err)
		return c.JSON(http.StatusInternalServerError, map[string]string{"error": "Could not create invoice"})
	}

	createdInvoice := models.Invoice{}
	err = dbConn.Get(&createdInvoice, "SELECT * FROM invoices WHERE id = $1", invoiceID)
	if err != nil {
		log.Println("Error :", err)
		return c.JSON(http.StatusInternalServerError, map[string]string{"error": "Internal server error."})
	}

	return c.JSON(http.StatusOK, createdInvoice)
}

func ArchiveInvoice(c echo.Context) error {
	// Parse the invoice ID from the request path
	invoiceID := c.Param("id")
	if invoiceID == "" {
		log.Println("Error: Missing invoice ID")
		return c.JSON(http.StatusBadRequest, map[string]string{"error": "Invoice ID is required"})
	}

	dbConn := db.GetDBConnection()
	query := "UPDATE invoices SET is_archived = true, updated_at = CURRENT_TIMESTAMP WHERE id = $1 AND user_id = $2"
	result, err := dbConn.Exec(query, invoiceID, c.Get("user_id"))
	if err != nil {
		log.Println("Error updating invoice:", err)
		return c.JSON(http.StatusInternalServerError, map[string]string{"error": "Could not archive the invoice"})
	}

	// Check if any row was actually updated
	rowsAffected, err := result.RowsAffected()
	if err != nil {
		log.Println("Error checking rows affected:", err)
		return c.JSON(http.StatusInternalServerError, map[string]string{"error": "Could not verify update"})
	}
	if rowsAffected == 0 {
		return c.JSON(http.StatusNotFound, map[string]string{"error": "Invoice not found or you are not authorized to archive it"})
	}

	// Respond with success
	return c.JSON(http.StatusOK, map[string]string{"message": "Invoice archived successfully"})
}
