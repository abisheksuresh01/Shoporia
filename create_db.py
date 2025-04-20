import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment
db_url = os.getenv("DATABASE_URL")

# Parse the database URL to get the database name
db_name = db_url.split("/")[-1]

# Create a connection to the default PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    user="postgres",
    password="postgres",
    database="postgres"
)

# Set autocommit to True to create the database
conn.autocommit = True

# Create a cursor
cursor = conn.cursor()

# Check if the database exists
cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
exists = cursor.fetchone()

if not exists:
    # Create the database
    cursor.execute(f"CREATE DATABASE {db_name}")
    print(f"Database '{db_name}' created successfully.")
else:
    print(f"Database '{db_name}' already exists.")

# Close the cursor and connection
cursor.close()
conn.close() 