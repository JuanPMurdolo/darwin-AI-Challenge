-- This file will be automatically executed when the PostgreSQL container starts

-- Create the database (already created by POSTGRES_DB)
-- CREATE DATABASE expense_bot;

-- Connect to the database
\c expense_bot;

-- The tables will be created automatically by the Python application
-- This file is just for any additional setup if needed

-- You can add test data here if you want
-- INSERT INTO users (telegram_id, username, first_name) VALUES ('123456789', 'testuser', 'Test User');
