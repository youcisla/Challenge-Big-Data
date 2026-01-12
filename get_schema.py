import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

try:
    conn = psycopg2.connect(
        user=os.environ.get("user"),
        password=os.environ.get("password"),
        host=os.environ.get("host"),
        port=os.environ.get("port"),
        dbname=os.environ.get("dbname")
    )
    cur = conn.cursor()
    
    # Query to list all tables in the public schema
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public';
    """)
    
    tables = cur.fetchall()
    print("Tables found:", tables)
    
    # For each table, let's get the columns to understand the schema
    for table in tables:
        table_name = table[0]
        print(f"\nSchema for table '{table_name}':")
        cur.execute(f"""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = '{table_name}';
        """)
        columns = cur.fetchall()
        for col in columns:
            print(f"  - {col[0]}: {col[1]}")

    cur.close()
    conn.close()

except Exception as e:
    print(f"Error: {e}")
