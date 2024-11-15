package cmd

import (
	"database/sql"
	"fmt"
	"log"
	"os"
	"path/filepath"

	"github.com/santoshkpatro/calyvim/internal/config"
	"github.com/santoshkpatro/calyvim/internal/db"
	"github.com/spf13/cobra"

	_ "github.com/lib/pq" // Import Postgres driver
)

var migrateCmd = &cobra.Command{
	Use:   "migrate",
	Short: "Run database migrations",
	Run: func(cmd *cobra.Command, args []string) {
		cfg := config.LoadConfig()

		conn, err := db.Connect(cfg.DatabaseURL)
		if err != nil {
			log.Printf("Failed to connect to the database: %v", err)
		}

		defer conn.Close()

		log.Println("Running database migrations...")

		// Ensure the schema_migrations table exists
		if err := ensureSchemaMigrationsTable(conn); err != nil {
			log.Fatalf("Failed to ensure schema_migrations table: %v", err)
		}

		// Define the migrations folder path
		migrationsFolder := "internal/db/migrations"

		// Read migrations files from the migrations folder
		files, err := os.ReadDir(migrationsFolder)
		if err != nil {
			log.Fatalf("Failed to read migrations folder: %v", err)
		}

		// Loop through the files in the migrations folder
		for _, file := range files {
			if filepath.Ext(file.Name()) == ".sql" {
				// Check if the migration has already been applied
				if hasMigrationBeenApplied(conn, file.Name()) {
					log.Printf("Migration %s has already been applied. Skipping.", file.Name())
					continue
				}

				// Read the migration SQL file
				migrationFilePath := filepath.Join(migrationsFolder, file.Name())
				migrationSQL, err := os.ReadFile(migrationFilePath)
				if err != nil {
					log.Fatalf("Failed to read migration file %s: %v", file.Name(), err)
				}

				// Execute the migration SQL
				if _, err := conn.Exec(string(migrationSQL)); err != nil {
					log.Fatalf("Failed to execute migration %s: %v", file.Name(), err)
				}

				// Insert the timestamp of the applied migration into schema_migrations
				if err := recordMigrationTimestamp(conn, file.Name()); err != nil {
					log.Fatalf("Failed to record migration timestamp for %s: %v", file.Name(), err)
				}

				log.Printf("Migration %s executed successfully.", file.Name())
			}
		}

		log.Println("All migrations executed successfully.")
	},
}

func init() {
	rootCmd.AddCommand(migrateCmd)
}

func ensureSchemaMigrationsTable(conn *sql.DB) error {
	var tableExists bool
	query := `SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'schema_migrations');`

	err := conn.QueryRow(query).Scan(&tableExists)
	if err != nil {
		return fmt.Errorf("failed to check if schema_migrations table exists: %v", err)
	}

	// If the table does not exist, create it
	if !tableExists {
		log.Println("Creating schema_migrations table...")
		createTableQuery := `CREATE TABLE schema_migrations (
			timestamp BIGINT PRIMARY KEY
		);`
		_, err := conn.Exec(createTableQuery)
		if err != nil {
			return fmt.Errorf("failed to create schema_migrations table: %v", err)
		}
		log.Println("Created schema_migrations table successfully.")
	}

	return nil
}

// hasMigrationBeenApplied checks if a migration has already been applied
func hasMigrationBeenApplied(conn *sql.DB, migrationName string) bool {
	var count int
	// Use the migration name as the identifier for the migration timestamp
	query := `SELECT COUNT(*) FROM schema_migrations WHERE timestamp = $1`
	// Use the migration's timestamp as the identifier
	timestamp := getMigrationTimestamp(migrationName)
	err := conn.QueryRow(query, timestamp).Scan(&count)
	if err != nil {
		log.Printf("Failed to check migration %s: %v", migrationName, err)
		return false
	}
	return count > 0
}

// recordMigrationTimestamp records the timestamp of the applied migration in schema_migrations
func recordMigrationTimestamp(conn *sql.DB, migrationName string) error {
	// Use the migration's timestamp as the identifier
	timestamp := getMigrationTimestamp(migrationName)
	_, err := conn.Exec(`INSERT INTO schema_migrations (timestamp) VALUES ($1)`, timestamp)
	if err != nil {
		return fmt.Errorf("failed to record migration timestamp for %s: %v", migrationName, err)
	}
	return nil
}

// getMigrationTimestamp generates a timestamp from the migration name (e.g., 1625562923_add_users.sql)
func getMigrationTimestamp(migrationName string) int64 {
	// Extract the timestamp from the file name (assuming the format is 'timestamp_description.sql')
	var timestamp int64
	_, err := fmt.Sscanf(migrationName, "%d_", &timestamp)
	if err != nil {
		log.Fatalf("Failed to parse timestamp from migration file %s: %v", migrationName, err)
	}
	return timestamp
}
