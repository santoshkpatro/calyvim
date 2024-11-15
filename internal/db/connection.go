package db

import (
	"database/sql"
	"log"

	_ "github.com/lib/pq" // Import Postgres driver
)

func Connect(dsn string) (*sql.DB, error) {
	db, err := sql.Open("postgres", dsn)

	if err != nil {
		log.Fatal("Unable to connect to the database.")
	}

	// Test the connection
	if err = db.Ping(); err != nil {
		return nil, err
	}

	log.Println("Successfully connected to the database")
	return db, nil
}
