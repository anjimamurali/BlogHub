import psycopg2
from psycopg2 import sql

def create_database():
    # Connect to the default 'postgres' database
    conn = psycopg2.connect(
        host="localhost",
        user="postgres",
        password="your_postgres_password",  # You'll need to replace this
        dbname="postgres"
    )
    conn.autocommit = True
    cursor = conn.cursor()
    
    # Create user if not exists
    try:
        cursor.execute("CREATE USER bloguser WITH PASSWORD 'blogpass';")
        print("✅ User 'bloguser' created successfully")
    except Exception as e:
        print(f"ℹ️ User 'bloguser' already exists or error: {e}")
    
    # Create database if not exists
    try:
        cursor.execute("CREATE DATABASE blogdb;")
        print("✅ Database 'blogdb' created successfully")
    except Exception as e:
        print(f"ℹ️ Database 'bloguser' already exists or error: {e}")
    
    # Grant privileges
    try:
        cursor.execute("GRANT ALL PRIVILEGES ON DATABASE blogdb TO bloguser;")
        print("✅ Granted all privileges on 'blogdb' to 'bloguser'")
    except Exception as e:
        print(f"❌ Error granting privileges: {e}")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    print("Setting up PostgreSQL database...")
    create_database()
    print("✅ Database setup completed!")
