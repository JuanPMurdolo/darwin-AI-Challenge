@echo off
echo Setting up PostgreSQL for Telegram Expense Bot...

echo.
echo 1. Installing PostgreSQL using Chocolatey (if not installed)...
where choco >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Chocolatey not found. Please install it first from https://chocolatey.org/install
    pause
    exit /b 1
)

choco install postgresql --version=15.4 -y

echo.
echo 2. Starting PostgreSQL service...
net start postgresql-x64-15

echo.
echo 3. Creating database and user...
set PGPASSWORD=postgres
createdb -U postgres expense_bot

echo.
echo 4. Setting up environment variables...
echo DATABASE_URL=postgresql://postgres:postgres@localhost:5432/expense_bot > .env
echo PORT=8000 >> .env
echo ENVIRONMENT=development >> .env

echo.
echo ✅ PostgreSQL setup complete!
echo.
echo Your database connection string is:
echo postgresql://postgres:postgres@localhost:5432/expense_bot
echo.
echo You can now run: python main.py
pause
