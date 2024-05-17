from datetime import datetime
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

# Mendapatkan semua judul film dan series
def get_film_list():
    conn = initialize_connection()
    cur = conn.cursor()
    cur.execute(sql.SQL("""
        SET search_path TO pacilflix;
        SELECT id, judul, sinopsis_trailer, url_video_trailer, release_date_trailer
        FROM tayangan
        JOIN film ON tayangan.id = film.id_tayangan;
    """))
    
    films = cur.fetchall()

    conn.close()
    return films

def get_series_list():
    conn = initialize_connection()
    cur = conn.cursor()
    cur.execute(sql.SQL("""
        SET search_path TO pacilflix;
        SELECT id, judul, sinopsis_trailer, url_video_trailer, release_date_trailer
        FROM tayangan
        JOIN series ON tayangan.id = series.id_tayangan;
    """))
    
    series = cur.fetchall()

    conn.close()
    return series

# Mendapatkan detail dari film atau series
def get_film_by_id(id_film):
    conn = initialize_connection()
    cur = conn.cursor()
    cur.execute(sql.SQL("""
        SET search_path TO pacilflix;
        SELECT id, judul, sinopsis, url_video_film, release_date_film, asal_negara, id_sutradara, durasi_film
        FROM tayangan
        JOIN film ON tayangan.id = %s;
    """), [id_film])
    
    film = cur.fetchone()

    conn.close()
    return film

def get_series_by_id(id_series):
    conn = initialize_connection()
    cur = conn.cursor()
    cur.execute(sql.SQL("""
        SET search_path TO pacilflix;
        SELECT id, judul, sinopsis, asal_negara, id_sutradara
        FROM tayangan
        JOIN series ON tayangan.id = %s;
    """), [id_series])
    
    series = cur.fetchone()

    conn.close()
    return series

def get_rating(id_tayangan):
    conn = initialize_connection()
    cur = conn.cursor()
    cur.execute(sql.SQL("""
        SET search_path TO pacilflix;
        SELECT rating
        FROM ulasan
        WHERE id_tayangan = %s;
    """), [id_tayangan])
    
    rating = cur.fetchall()

    conn.close()
    return rating

def get_genre(id_tayangan):
    conn = initialize_connection()
    cur = conn.cursor()
    cur.execute(sql.SQL("""
        SET search_path TO pacilflix;
        SELECT genre
        FROM genre_tayangan
        WHERE id_tayangan = %s;
    """), [id_tayangan])
    
    genre = cur.fetchall()

    conn.close()
    return genre

def get_sutradara(id_sutradara):
    conn = initialize_connection()
    cur = conn.cursor()
    cur.execute(sql.SQL("""
        SET search_path TO pacilflix;
        SELECT nama
        FROM contributors
        WHERE id = %s;
    """), [id_sutradara])
    
    sutradara_tuple = cur.fetchone()

    conn.close()

    if sutradara_tuple:
        sutradara_name = sutradara_tuple[0]
        return sutradara_name
    else:
        return None
    
def get_pemain_list(id_tayangan):
    conn = initialize_connection()
    cur = conn.cursor()
    cur.execute(sql.SQL("""
        SET search_path TO pacilflix;
        SELECT c.nama
        FROM contributors c
        WHERE c.id IN (
            SELECT mt.id_pemain
            FROM memainkan_tayangan mt
            WHERE mt.id_tayangan = %s
        );
    """), [id_tayangan])
    
    pemain = cur.fetchall()

    conn.close()
    return pemain

def get_penulis_skenario_list(id_tayangan):
    conn = initialize_connection()
    cur = conn.cursor()
    cur.execute(sql.SQL("""
        SET search_path TO pacilflix;
        SELECT c.nama
        FROM contributors c
        WHERE c.id IN (
            SELECT mt.id_penulis_skenario
            FROM menulis_skenario_tayangan mt
            WHERE mt.id_tayangan = %s
        );
    """), [id_tayangan])
    
    penulis_skenario = cur.fetchall()

    conn.close()
    return penulis_skenario

def get_ulasan(id_tayangan):
    conn = initialize_connection()
    cur = conn.cursor()
    cur.execute(sql.SQL("""
        SET search_path TO pacilflix;
        SELECT username, rating, deskripsi
        FROM ulasan
        WHERE id_tayangan = %s
        ORDER BY timestamp DESC;
    """), [id_tayangan])
    
    ulasan = cur.fetchall()

    conn.close()
    return ulasan

def add_ulasan(id_tayangan, username, rating, deskripsi):
    conn = initialize_connection()
    cur = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cur.execute(sql.SQL("""
        SET search_path TO pacilflix;
        INSERT INTO ulasan (id_tayangan, username, timestamp, rating, deskripsi)
        VALUES (%s, %s, %s, %s, %s);
    """), [id_tayangan, username, timestamp, rating, deskripsi])
    
    conn.commit()
    conn.close()

def tambah_tayangan_terunduh(id_tayangan, username):
    conn = initialize_connection()
    cur = conn.cursor()
    
    cur.execute(sql.SQL("""
        SET search_path TO pacilflix;                
        INSERT INTO tayangan_terunduh (id_tayangan, username, timestamp)
        VALUES (%s, %s, NOW());
    """), [id_tayangan, username])
        
    conn.commit()
    conn.close()