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

def fetch_favorites(username):
    conn = initialize_connection()
    cur = conn.cursor()
    try:
        query = """
            SELECT t.judul, d.timestamp
            FROM pacilflix.daftar_favorit d
            JOIN pacilflix.tayangan t ON d.judul = t.judul
            WHERE d.username = %s;
        """
        cur.execute(query, [username])
        favorites_list = cur.fetchall()
        conn.close()
        return favorites_list
    except Exception as e:
        conn.rollback()
        conn.close()
        print(f"Error fetching favorites: {e}")
        raise e

def fetch_favorite_details(username, tayangan_id):
    conn = initialize_connection()
    cur = conn.cursor()
    try:
        query = """
            SELECT t.judul, t.sinopsis, d.timestamp
            FROM pacilflix.daftar_favorit d
            JOIN pacilflix.tayangan t ON d.judul = t.judul
            WHERE d.username = %s AND t.id = %s;
        """
        cur.execute(query, [username, tayangan_id])
        favorite_details = cur.fetchone()
        conn.close()
        return favorite_details
    except Exception as e:
        conn.rollback()
        conn.close()
        print(f"Error fetching favorite details: {e}")
        raise e

def add_to_favorites(username, tayangan_id, favorite_list_name):
    conn = initialize_connection()
    cur = conn.cursor()
    try:
        query = """
            INSERT INTO pacilflix.daftar_favorit (username, tayangan_id, timestamp, favorite_list_name)
            VALUES (%s, %s, NOW(), %s);
        """
        cur.execute(query, [username, tayangan_id, favorite_list_name])
        conn.commit()
        conn.close()
    except Exception as e:
        conn.rollback()
        conn.close()
        print(f"Error adding to favorites: {e}")
        raise e

def create_new_favorite_list(username, favorite_list_name):
    conn = initialize_connection()
    cur = conn.cursor()
    try:
        query = """
            INSERT INTO pacilflix.favorite_lists (username, favorite_list_name)
            VALUES (%s, %s);
        """
        cur.execute(query, [username, favorite_list_name])
        conn.commit()
        conn.close()
    except Exception as e:
        conn.rollback()
        conn.close()
        print(f"Error creating new favorite list: {e}")
        raise e

def fetch_favorite_lists(username):
    conn = initialize_connection()
    cur = conn.cursor()
    try:
        query = """
            SELECT favorite_list_name
            FROM pacilflix.favorite_lists
            WHERE username = %s;
        """
        cur.execute(query, [username])
        favorite_lists = cur.fetchall()
        conn.close()
        return favorite_lists
    except Exception as e:
        conn.rollback()
        conn.close()
        print(f"Error fetching favorite lists: {e}")
        raise e

def remove_from_favorites(username, tayangan_id):
    conn = initialize_connection()
    cur = conn.cursor()
    try:
        query = """
            DELETE FROM pacilflix.daftar_favorit
            WHERE username = %s AND tayangan_id = %s;
        """
        cur.execute(query, [username, tayangan_id])
        conn.commit()
        conn.close()
    except Exception as e:
        conn.rollback()
        conn.close()
        print(f"Error removing from favorites: {e}")
        raise e
