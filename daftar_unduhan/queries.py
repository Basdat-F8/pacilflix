import psycopg2
from psycopg2 import sql

DB_NAME = 'postgres'
DB_USER = 'postgres.jcktthwwciswkjbgaxgv'
DB_PASS = 'FasilkomFlixF8'
DB_HOST = 'aws-0-ap-southeast-1.pooler.supabase.com'
DB_PORT = '5432'

def initialize_connection():
    return psycopg2.connect(
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )

def hapus_unduhan(username, tayangan_id):
    conn = initialize_connection()
    cur = conn.cursor()
    try:
        query = """
            DELETE FROM pacilflix.tayangan_terunduh
            WHERE username = %s AND id_tayangan =%s;
        """
        cur.execute(query, [username, tayangan_id])
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error deleting download: {e}")
        raise e
    finally:
        conn.close()


def fetch_unduhan(username):
    conn = initialize_connection()
    cur = conn.cursor()
    try:
        query = """
            SELECT t.judul, tt.timestamp, tt.id_tayangan
            FROM pacilflix.tayangan_terunduh tt
            JOIN pacilflix.tayangan t ON tt.id_tayangan = t.id
            WHERE tt.username = %s;
        """
        cur.execute(query, [username])
        unduhan_list = cur.fetchall()
        conn.close()
        return unduhan_list
    except Exception as e:
        conn.rollback()
        conn.close()
        print(f"Error fetching data: {e}")
        raise e
