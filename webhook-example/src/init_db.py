"""Initialize the database."""
import os
import psycopg2
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
env_path = Path(__file__).parent.parent / '.env'
if env_path.exists():
    load_dotenv(env_path)
else:
    load_dotenv()

# Create table with URL as primary key
conn = psycopg2.connect(os.environ["DATABASE_URL"])
cur = conn.cursor()

# Drop existing table if it has the old schema
cur.execute("DROP TABLE IF EXISTS images")

cur.execute("""
    CREATE TABLE IF NOT EXISTS images (
        url TEXT PRIMARY KEY,
        has_magnus BOOLEAN,
        caption TEXT,
        status TEXT DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        processed_at TIMESTAMP
    )
""")
conn.commit()
conn.close()
print("Table 'images' created successfully with URL as primary key") 