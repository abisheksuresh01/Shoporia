import os
import subprocess
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def run_command(command):
    """Run a command and print its output"""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(f"Error: {result.stderr}")
    return result.returncode

def main():
    print("Database Setup Script")
    print("=====================")
    
    # Check if PostgreSQL is installed
    print("\nChecking if PostgreSQL is installed...")
    if run_command("psql --version") != 0:
        print("PostgreSQL is not installed or not in PATH.")
        print("Please install PostgreSQL from https://www.postgresql.org/download/")
        return
    
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
    
    # Create database
    print("\nCreating database...")
    create_db_cmd = f'psql -U {username} -h {host} -p {port} -c "CREATE DATABASE {db_name}"'
    if run_command(create_db_cmd) != 0:
        print("Failed to create database. You may need to create it manually.")
        print(f"Try running: {create_db_cmd}")
    
    # Run migrations
    print("\nRunning migrations...")
    if run_command("alembic upgrade head") != 0:
        print("Failed to run migrations. You may need to run them manually.")
        print("Try running: alembic upgrade head")
    
    print("\nSetup complete!")

if __name__ == "__main__":
    main() 