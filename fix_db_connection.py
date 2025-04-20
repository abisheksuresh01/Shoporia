import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    print("Database Connection Fix Script")
    print("=============================")
    
    # Get database credentials
    print("\nPlease enter your PostgreSQL credentials:")
    username = input("Username (default: postgres): ") or "postgres"
    password = input("Password: ")
    host = input("Host (default: localhost): ") or "localhost"
    port = input("Port (default: 5432): ") or "5432"
    db_name = input("Database name (default: ecommerce_agent): ") or "ecommerce_agent"
    
    # Update .env file
    print("\nUpdating .env file...")
    db_url = f"postgresql://{username}:{password}@{host}:{port}/{db_name}"
    
    with open(".env", "r") as f:
        env_content = f.read()
    
    # Replace or add DATABASE_URL
    if "DATABASE_URL=" in env_content:
        env_content = env_content.replace(
            env_content[env_content.find("DATABASE_URL="):env_content.find("\n", env_content.find("DATABASE_URL="))],
            f'DATABASE_URL="{db_url}"'
        )
    else:
        env_content += f'\nDATABASE_URL="{db_url}"\n'
    
    with open(".env", "w") as f:
        f.write(env_content)
    
    print(f"Updated .env file with DATABASE_URL: {db_url}")
    
    # Update alembic.ini file
    print("\nUpdating alembic.ini file...")
    with open("alembic.ini", "r") as f:
        alembic_content = f.read()
    
    # Replace sqlalchemy.url
    alembic_content = alembic_content.replace(
        alembic_content[alembic_content.find("sqlalchemy.url = "):alembic_content.find("\n", alembic_content.find("sqlalchemy.url = "))],
        f"sqlalchemy.url = {db_url}"
    )
    
    with open("alembic.ini", "w") as f:
        f.write(alembic_content)
    
    print(f"Updated alembic.ini file with sqlalchemy.url: {db_url}")
    
    print("\nSetup complete!")
    print("\nNow you can run the following commands:")
    print("1. Create the database: psql -U postgres -c \"CREATE DATABASE ecommerce_agent\"")
    print("2. Run migrations: alembic upgrade head")

if __name__ == "__main__":
    main() 