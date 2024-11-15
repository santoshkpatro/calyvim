CREATE TABLE invoices (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    invoice_type VARCHAR(20) DEFAULT 'standard',
    invoice_number VARCHAR(50) UNIQUE NOT NULL,
    order_name VARCHAR(50),
    issue_date DATE NOT NULL,
    payment_status VARCHAR (20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);