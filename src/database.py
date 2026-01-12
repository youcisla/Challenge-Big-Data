import os
import psycopg2
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

@st.cache_resource
def get_db_connection():
    """
    Establishes a connection to the PostgreSQL database using psycopg2.
    Returns the connection object.
    """
    try:
        conn = psycopg2.connect(
            user=os.environ.get("user"),
            password=os.environ.get("password"),
            host=os.environ.get("host"),
            port=os.environ.get("port"),
            dbname=os.environ.get("dbname")
        )
        return conn
    except Exception as e:
        st.error(f"Error connecting to database: {e}")
        return None

def run_query(query, params=None):
    """
    Executes a SQL query and returns the results.
    """
    conn = get_db_connection()
    if conn is None:
        return None
        
    try:
        cur = conn.cursor()
        cur.execute(query, params)
        
        # Check if the query returns rows (SELECT)
        if cur.description:
            columns = [desc[0] for desc in cur.description]
            data = cur.fetchall()
            # Return as list of dicts for easier consumption or DataFrame creation
            result = [dict(zip(columns, row)) for row in data]
            cur.close()
            return result
        else:
            conn.commit()
            cur.close()
            return None
            
    except Exception as e:
        st.error(f"Query failed: {e}")
        # In case of error, we might want to rollback
        conn.rollback()
        return None
