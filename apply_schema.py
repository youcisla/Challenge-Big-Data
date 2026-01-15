import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("user")
DB_PASSWORD = os.getenv("password")
DB_HOST = os.getenv("host")
DB_PORT = os.getenv("port")
DB_NAME = os.getenv("dbname")

def apply_schema():
    try:
        conn = psycopg2.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME
        )
        cur = conn.cursor()
        
        with open('db.sql', 'r') as f:
            schema_sql = f.read()
            
        print("Applying schema...")
        cur.execute(schema_sql)
        conn.commit()
        print("Schema applied successfully.")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error applying schema: {e}")

if __name__ == "__main__":
    apply_schema()
