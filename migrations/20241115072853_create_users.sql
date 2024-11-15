CREATE TABLE users (
    id SERIAL PRIMARY KEY,                
    email VARCHAR(255) NOT NULL UNIQUE,   
    password_hash VARCHAR(255) NOT NULL,   
    first_name VARCHAR(255),               
    last_name VARCHAR(255),                
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    is_active BOOLEAN DEFAULT TRUE,        
    is_admin BOOLEAN DEFAULT FALSE
);
