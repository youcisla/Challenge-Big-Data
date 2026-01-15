import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv
import numpy as np

# Load environment variables
load_dotenv()

# Database connection details
DB_USER = os.getenv("user")
DB_PASSWORD = os.getenv("password")
DB_HOST = os.getenv("host")
DB_PORT = os.getenv("port")
DB_NAME = os.getenv("dbname")

# CSV file path
CSV_FILE_PATH = os.path.join("data", "dataset.csv")

def import_data():
    if not os.path.exists(CSV_FILE_PATH):
        print(f"Error: File not found at {CSV_FILE_PATH}")
        return

    print("Reading CSV file...")
    try:
        df = pd.read_csv(CSV_FILE_PATH)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    # Data transformation to match DB Schema
    # 1. Rename 'country_3_letter_code_x' -> 'country_3_letter_code'
    if 'country_3_letter_code_x' in df.columns:
        df = df.rename(columns={'country_3_letter_code_x': 'country_3_letter_code'})
    
    # 2. Check for missing columns (e.g. game_slug is gone, which is good)
    expected_cols = [
        'year', 'slug_game', 'country_3_letter_code', 
        'bronze_medals', 'gold_medals', 'silver_medals', 'total_medals', 
        'total_athletes', 'avg_age_athletes', 'medals_in_current_year', 
        'city', 'season', 'game_name', 'cumulative_medals', 'is_host'
    ]
    
    # Fill NaN with None (for SQL NULL)
    df = df.replace({np.nan: None})

    print("Connecting to database...")
    try:
        conn = psycopg2.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME
        )
        cur = conn.cursor()

        # Optional: Truncate table before import
        print("Truncating table 'olympic_stats'...")
        cur.execute("TRUNCATE TABLE olympic_stats RESTART IDENTITY;")

        print("Inserting rows...")
        insert_query = """
            INSERT INTO olympic_stats (
                year, slug_game, country_3_letter_code, 
                bronze_medals, gold_medals, silver_medals, total_medals, 
                total_athletes, avg_age_athletes, medals_in_current_year, 
                city, season, game_name, cumulative_medals, is_host
            ) VALUES (
                %s, %s, %s, 
                %s, %s, %s, %s, 
                %s, %s, %s, 
                %s, %s, %s, %s, %s
            )
        """

        for _, row in df.iterrows():
            values = (
                row.get('year'), row.get('slug_game'), row.get('country_3_letter_code'),
                row.get('bronze_medals'), row.get('gold_medals'), row.get('silver_medals'), row.get('total_medals'),
                row.get('total_athletes'), row.get('avg_age_athletes'), row.get('medals_in_current_year'),
                row.get('city'), row.get('season'), row.get('game_name'), row.get('cumulative_medals'), row.get('is_host')
            )
            cur.execute(insert_query, values)

        conn.commit()
        print(f"Successfully inserted {len(df)} rows.")

        cur.close()
        conn.close()

    except Exception as e:
        print(f"Database error: {e}")

if __name__ == "__main__":
    import_data()
