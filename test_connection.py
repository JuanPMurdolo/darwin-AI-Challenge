import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

async def test_connections():
    """Test different PostgreSQL connection strings"""
    
    # Different connection strings to try
    connection_strings = [
        "postgresql://postgres:postgres@localhost:5432/expense_bot",
        "postgresql://postgres:postgres@127.0.0.1:5432/expense_bot",
        "postgresql://postgres:postgres@localhost:5432/postgres",
        "postgresql://postgres:postgres@127.0.0.1:5432/postgres",
    ]
    
    for i, conn_str in enumerate(connection_strings, 1):
        print(f"\n--- Test {i}: {conn_str} ---")
        try:
            # Try to connect with a simple connection (not pool)
            conn = await asyncpg.connect(conn_str, timeout=5)
            print("✅ Connection successful!")
            
            # Test query
            result = await conn.fetchrow("SELECT version()")
            print(f"PostgreSQL version: {result['version'][:50]}...")
            
            # List databases
            databases = await conn.fetch("SELECT datname FROM pg_database WHERE datistemplate = false")
            print(f"Available databases: {[db['datname'] for db in databases]}")
            
            await conn.close()
            print("✅ This connection works!")
            return conn_str
            
        except Exception as e:
            print(f"❌ Connection failed: {e}")
    
    return None

if __name__ == "__main__":
    working_conn = asyncio.run(test_connections())
    if working_conn:
        print(f"\n🎉 Working connection string: {working_conn}")
        print("\nAdd this to your .env file:")
        print(f"DATABASE_URL={working_conn}")
    else:
        print("\n😞 No working connection found")
        print("\nTroubleshooting steps:")
        print("1. Check if Docker container is running: docker ps")
        print("2. Check container logs: docker logs expense_bot_postgres")
        print("3. Try connecting to container directly: docker exec -it expense_bot_postgres psql -U postgres")
