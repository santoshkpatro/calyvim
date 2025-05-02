package db

import (
	"log"
	"os"
	"time"

	_ "github.com/jackc/pgx/v5/stdlib"
	"github.com/jmoiron/sqlx"
)

func Connect() *sqlx.DB {
	dsn := os.Getenv("DATABASE_URL")

	db, err := sqlx.Connect("pgx", dsn)
	if err != nil {
		log.Fatalf("Database connection failed: %v", err)
	}

	// Set connection timeout for ping
	db.SetConnMaxLifetime(time.Minute * 5)

	// Ping the database to ensure it's alive
	if err := db.Ping(); err != nil {
		log.Fatalf("Database ping failed: %v", err)
	}

	log.Println("Database connection established and ping successful")
	return db
}
