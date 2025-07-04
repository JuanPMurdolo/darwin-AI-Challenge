CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  telegram_id TEXT UNIQUE NOT NULL
  username TEXT UNIQUE NOT NULL,
  email TEXT,
  full_name TEXT,
);

CREATE TABLE IF NOT EXISTS expenses (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id),
  description TEXT NOT NULL,
  telegram_id TEXT NOT NULL,
  amount MONEY NOT NULL,
  category TEXT NOT NULL,
  added_at TIMESTAMP NOT NULL
);

-- Agregar tus IDs de Telegram permitidos
INSERT INTO users (telegram_id, username, email, full_name)
VALUES 
  ('JotapeJoplin'),
  ('5440711730', "Juan", "testing@testing.com", "Juan Perez"),
ON CONFLICT (telegram_id) DO NOTHING;
