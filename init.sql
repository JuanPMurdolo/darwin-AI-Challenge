-- Create the database and user
CREATE DATABASE IF NOT EXISTS expenses_db;

-- Create tables
CREATE TABLE IF NOT EXISTS users (
  id VARCHAR(255) PRIMARY KEY,
  telegram_id VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS expenses (
  id SERIAL PRIMARY KEY,
  user_id VARCHAR(255) NOT NULL,
  description TEXT NOT NULL,
  amount DECIMAL(10,2) NOT NULL,
  category TEXT NOT NULL,
  added_at TIMESTAMP NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Add test users
INSERT INTO users (id, telegram_id)
VALUES 
  ('test_user_123', '123456789'),
  ('user_1', '987654321')
ON CONFLICT (telegram_id) DO NOTHING;

-- Add some test expenses
INSERT INTO expenses (user_id, description, amount, category, added_at)
VALUES 
  ('test_user_123', 'Coffee', 4.50, 'Food', NOW()),
  ('test_user_123', 'Bus ticket', 2.25, 'Transportation', NOW()),
  ('test_user_123', 'Lunch', 12.00, 'Food', NOW())
ON CONFLICT DO NOTHING;
