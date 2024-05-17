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
            SELECT judul, timestamp
            FROM pacilflix.daftar_favorit
            WHERE username = %s;
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

def fetch_favorite_details(username, judul_favorit):
    conn = initialize_connection()
    cur = conn.cursor()
    try:
        query = """
            SELECT t.judul
            FROM pacilflix.tayangan t
            JOIN pacilflix.tayangan_memiliki_daftar_favorit tf ON t.id = tf.id_tayangan
            JOIN pacilflix.daftar_favorit df ON tf.username = df.username
            WHERE df.username = %s AND df.judul = %s;
        """
        cur.execute(query, [username, judul_favorit])
        favorite_list_details = cur.fetchall()
        conn.close()
        return favorite_list_details
    except Exception as e:
        conn.rollback()
        conn.close()
        print(f"Error fetching favorite list details: {e}")
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

def remove_from_favorites(username, judul):
    conn = initialize_connection()
    cur = conn.cursor()
    try:
        query = """
            DELETE FROM pacilflix.daftar_favorit
            WHERE username = %s AND judul = %s;
        """
        cur.execute(query, [username, judul])
        conn.commit()
        conn.close()
    except Exception as e:
        conn.rollback()
        conn.close()
        print(f"Error removing from favorites: {e}")
        raise e

def remove_tayangan_from_favorites(username, judul_favorit, judul_tayangan):
    conn = initialize_connection()
    cur = conn.cursor()
    try:
        query = """
            DELETE FROM pacilflix.tayangan_memiliki_daftar_favorit
            WHERE id_tayangan IN (
                SELECT t.id
                FROM pacilflix.tayangan t
                WHERE t.judul = %s
            )
            AND id_daftar_favorit IN (
                SELECT df.id
                FROM pacilflix.daftar_favorit df
                WHERE df.username = %s AND df.judul = %s
            );
        """
        cur.execute(query, [judul_tayangan, username, judul_favorit])
        conn.commit()
        conn.close()
    except Exception as e:
        conn.rollback()
        conn.close()
        print(f"Error removing tayangan from favorites: {e}")
        raise e
