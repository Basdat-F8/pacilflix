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
            SELECT d.judul, d.timestamp
            FROM pacilflix.daftar_favorit d
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

def fetch_favorite_details(username, nama_fav):
    conn = initialize_connection()
    cur = conn.cursor()
    try:
        query = """
            SELECT t.judul, t.id
            FROM pacilflix.tayangan_memiliki_daftar_favorit tf,
            pacilflix.daftar_favorit f, pacilflix.tayangan t
            WHERE t.id = tf.id_tayangan AND tf.timestamp = f.timestamp AND tf.username = f.username
            AND tf.username = %s AND f.judul = %s;
        """
        cur.execute(query, [username, nama_fav])
        favorite_details = cur.fetchall()
        conn.close()
        return favorite_details
    except Exception as e:
        conn.rollback()
        conn.close()
        print(f"Error fetching favorite details: {e}")
        raise e

def add_to_favorites(username, judul):
    conn = initialize_connection()
    cur = conn.cursor()
    try:
        query = """
            INSERT INTO pacilflix.daftar_favorit (timestamp, username, judul)
            VALUES (NOW(), %s, %s);
        """
        cur.execute(query, [username, judul])
        conn.commit()
        conn.close()
    except Exception as e:
        conn.rollback()
        conn.close()
        print(f"Error adding to favorites: {e}")
        raise e
    
def add_tayangan_to_favorite(tayangan_id, username, judul):
    conn = initialize_connection()
    cur = conn.cursor()
    try:
        timestamp = """
            SELECT timestamp
            FROM pacilflix.tayangan_memiliki_daftar_favorit
            WHERE username = '%s' AND judul = '%s'
            ORDER BY timestamp DESC
            LIMIT 1;
        """
        cur.execute(timestamp, [username, judul])
        timestamp = cur.fetchone()
        query = """
            INSERT INTO pacilflix.tayangan_memiliki_daftar_favorit
            VALUES (%s, %s, %s);
        """
        cur.execute(query, [tayangan_id, timestamp, username])
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
            INSERT INTO pacilflix.daftar_favorit (username, favorite_list_name)
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

# def fetch_favorite_lists(username):
#     conn = initialize_connection()
#     cur = conn.cursor()
#     try:
#         query = """
#             SELECT judul
#             FROM pacilflix.daftar_favorit
#             WHERE username = %s;
#         """
#         cur.execute(query, [username])
#         favorite_lists = cur.fetchall()
#         conn.close()
#         return favorite_lists
#     except Exception as e:
#         conn.rollback()
#         conn.close()
#         print(f"Error fetching favorite lists: {e}")
#         raise e

def remove_from_favorites(username, nama_fav):
    conn = initialize_connection()
    cur = conn.cursor()
    try:
        query = """
            DELETE FROM pacilflix.daftar_favorit
            WHERE username = %s AND judul = %s;
        """
        cur.execute(query, [username, nama_fav])
        conn.commit()
        conn.close()
    except Exception as e:
        conn.rollback()
        conn.close()
        print(f"Error removing from favorites: {e}")
        raise e
    
def remove_from_list_favorite(username, tayangan_id):
    conn = initialize_connection()
    cur = conn.cursor()
    try:
        query = """
            DELETE FROM pacilflix.tayangan_memiliki_daftar_favorit
            WHERE username = %s AND id_tayangan = %s;
        """
        cur.execute(query, [username, tayangan_id])
        conn.commit()
        conn.close()
    except Exception as e:
        conn.rollback()
        conn.close()
        print(f"Error removing from favorites: {e}")
        raise e
    
def fetch_tipe(judul_tayangan):
    conn = initialize_connection()
    cur = conn.cursor()
    print(judul_tayangan)
    try:
        query = """
            SET search_path to pacilflix;
            (SELECT t.id, 'Film' AS tipe
            FROM tayangan t, film f
            WHERE t.id = f.id_tayangan AND t.judul = %s)
            UNION ALL
            (SELECT t.id, 'Series' AS tipe
            FROM tayangan t, series s
            WHERE t.id = s.id_tayangan AND t.judul = %s)
        """
        cur.execute(query,[judul_tayangan,judul_tayangan])
        tipe = cur.fetchone()
        conn.close()
        return tipe
    except Exception as e:
        conn.rollback()
        conn.close()
        print(f"Error removing from favorites: {e}")
        raise e
