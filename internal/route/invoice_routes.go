package route

import (
	"github.com/labstack/echo/v4"
	"github.com/santoshkpatro/calyvim/internal/handler"
	"github.com/santoshkpatro/calyvim/internal/middleware"
)

func RegisterInvoiceRoutes(e *echo.Echo) {
	invoiceGroup := e.Group("/api/invoices")
	{
		invoiceGroup.GET("", handler.GetInvoices, middleware.JWTAuth)
		invoiceGroup.POST("", handler.CreateInvoice, middleware.JWTAuth)
		invoiceGroup.PATCH("/:id/archive", handler.ArchiveInvoice, middleware.JWTAuth)
	}
}
