package handlers

import "github.com/jmoiron/sqlx"

type HandlerContext struct {
    DB *sqlx.DB
}