package handlers

import (
	"github.com/jmoiron/sqlx"
	"github.com/redis/go-redis/v9"
)

type HandlerContext struct {
	DB    *sqlx.DB
	Cache *redis.Client
}
