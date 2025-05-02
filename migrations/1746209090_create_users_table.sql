-- migration: create_users_table

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,

    first_name VARCHAR(100),
    last_name VARCHAR(100),

    is_active BOOLEAN DEFAULT TRUE,
    activated_at TIMESTAMP,
    verified_at TIMESTAMP,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
