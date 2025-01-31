import psycopg2
from psycopg2 import sql

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='infodb',
            user='postgres',  
            password='1234'  
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        raise

def init_db():
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS cves (
                id TEXT PRIMARY KEY,
                description TEXT,
                published_date TEXT,
                last_modified_date TEXT,
                status TEXT
            );
        ''')
        conn.commit()
        cur.close()
    except Exception as e:
        print(f"Error initializing the database: {e}")
    finally:
        if conn:
            conn.close()  
