-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    telegram_id TEXT UNIQUE NOT NULL,
    username TEXT,
    first_name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create expenses table
CREATE TABLE IF NOT EXISTS expenses (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    description TEXT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    category TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create categories table for reference
CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    description TEXT
);

-- Insert default categories
INSERT INTO categories (name, description) VALUES
    ('Food', 'Meals, groceries, restaurants'),
    ('Transportation', 'Gas, public transport, rideshare'),
    ('Housing', 'Rent, utilities, maintenance'),
    ('Entertainment', 'Movies, games, hobbies'),
    ('Healthcare', 'Medical, pharmacy, insurance'),
    ('Shopping', 'Clothes, electronics, general purchases'),
    ('Education', 'Books, courses, training'),
    ('Other', 'Miscellaneous expenses')
ON CONFLICT (name) DO NOTHING;

-- Insert a test user (replace with your actual Telegram ID)
INSERT INTO users (telegram_id, username, first_name) VALUES
    ('123456789', 'testuser', 'Test User')
ON CONFLICT (telegram_id) DO NOTHING;
