import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# CSV Path
CSV_FILE = r"data/olympic_final_dataset.csv"

def import_data():
    print("🚀 Starting data import...")
    
    # 1. Read CSV
    if not os.path.exists(CSV_FILE):
        print(f"❌ Error: File not found at {CSV_FILE}")
        return

    try:
        df = pd.read_csv(CSV_FILE)
        print(f"✅ Loaded CSV with {len(df)} rows.")
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return

    # 2. Connect to Database
    try:
        conn = psycopg2.connect(
            user=os.environ.get("user"),
            password=os.environ.get("password"),
            host=os.environ.get("host"),
            port=os.environ.get("port"),
            dbname=os.environ.get("dbname")
        )
        cur = conn.cursor()
        print("✅ Connected to database.")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return

    # 3. Clean Table (Optional but safer for re-runs)
    try:
        print("🧹 Clearing existing data in 'olympic_stats'...")
        cur.execute("TRUNCATE TABLE olympic_stats RESTART IDENTITY;")
        conn.commit()
    except Exception as e:
         print(f"⚠️ Warning during truncate (table might be empty or missing): {e}")
         conn.rollback()

    # 4. Insert Data
    print("💾 Inserting rows...")
    success_count = 0
    error_count = 0

    insert_query = """
    INSERT INTO olympic_stats (
        year, slug_game, country_3_letter_code, bronze_medals, gold_medals, silver_medals,
        total_medals, total_athletes, avg_age_athletes, medals_in_current_year,
        game_slug, city, season, game_name, cumulative_medals, is_host
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    for _, row in df.iterrows():
        try:
            # Handle potential NaN values
            avg_age = row['avg_age_athletes'] if pd.notna(row['avg_age_athletes']) else None
            
            # Note: CSV columns must match the order here
            values = (
                int(row['year']),
                row['slug_game'],
                row['country_3_letter_code'],
                int(row['bronze_medals']),
                int(row['gold_medals']),
                int(row['silver_medals']),
                int(row['total_medals']),
                int(row['total_athletes']) if pd.notna(row['total_athletes']) else 0, # Handle missing total_athletes
                avg_age,
                int(row['medals_in_current_year']),
                row['game_slug'],
                row['city'],
                row['season'],
                row['game_name'],
                float(row['cumulative_medals']),
                int(row['is_host'])
            )
            
            cur.execute(insert_query, values)
            success_count += 1
            
        except Exception as e:
            print(f"⚠️ Error inserting row {row['slug_game']}-{row['country_3_letter_code']}: {e}")
            error_count += 1
            conn.rollback() # Rollback the single failed transaction to continue? 
            # Ideally we want batch insert but row-by-row is easier to debug for this size (~2k rows)
            # psycopg2 requires rollback after error to continue using connection
            continue

    conn.commit()
    cur.close()
    conn.close()

    print("\n========================================")
    print(f"🎉 Import Completed!")
    print(f"✅ Successful inserts: {success_count}")
    print(f"❌ Failed inserts: {error_count}")
    print("========================================")

if __name__ == "__main__":
    import_data()
