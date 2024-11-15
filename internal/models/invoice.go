package models

import "time"

type Invoice struct {
	ID            int       `db:"id" json:"id"`
	UserId        int       `db:"user_id" json:"-"`
	InvoiceType   string    `db:"invoice_type" json:"invoiceType"`
	InvoiceNumber string    `db:"invoice_number" json:"invoiceNumber"`
	OrderName     string    `db:"order_name" json:"orderName"`
	IssueDate     time.Time `db:"issue_date" json:"issueDate"`
	PaymentStatus string    `db:"payment_status" json:"paymentStatus"`
	IsArchived    bool      `db:"is_archived" json:"-"`
	CreatedAt     time.Time `db:"created_at" json:"createdAt"`
	UpdatedAt     time.Time `db:"updated_at" json:"updatedAt"`
}
