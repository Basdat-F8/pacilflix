from datetime import datetime
import psycopg2
from psycopg2 import sql, errors

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

def get_viewers_film(id_film):
    conn = initialize_connection()
    cur = conn.cursor()
    cur.execute(sql.SQL("""
        SET search_path TO pacilflix;
        WITH durasi_tayangan AS (
            SELECT
                f.id_tayangan,
                f.durasi_film,
                (f.durasi_film * 0.7) AS min_durasi_view
            FROM
                film f
            WHERE
                f.id_tayangan = %s
        ),
        durasi_nonton AS (
            SELECT
                rn.id_tayangan,
                rn.username,
                EXTRACT(EPOCH FROM (rn.end_date_time - rn.start_date_time)) / 60 AS durasi_nonton
            FROM
                riwayat_nonton rn
            WHERE
                rn.id_tayangan = %s
        )
        SELECT
            COUNT(*) AS jumlah_view
        FROM
            durasi_nonton dn
        JOIN
            durasi_tayangan dt ON dn.id_tayangan = dt.id_tayangan
        WHERE
            dn.durasi_nonton >= dt.min_durasi_view;
    """), [id_film, id_film])
    
    viewers = cur.fetchone()

    conn.close()
    return viewers

def get_viewers_series(id_series):
    conn = initialize_connection()
    cur = conn.cursor()
    cur.execute(sql.SQL("""
        SET search_path TO pacilflix;
        WITH durasi_tayangan AS (
            SELECT
                rt.id_tayangan,
                COALESCE(f.durasi_film, e.durasi) AS durasi_tayangan,
                (COALESCE(f.durasi_film, e.durasi) * 0.7) AS min_durasi_view
            FROM
                riwayat_nonton rt
            LEFT JOIN
                tayangan t ON rt.id_tayangan = t.id
            LEFT JOIN
                film f ON t.id = f.id_tayangan
            LEFT JOIN
                episode e ON t.id = e.id_series
            WHERE
                rt.id_tayangan = %s
        ),
        durasi_nonton AS (
            SELECT
                rn.id_tayangan,
                rn.username,
                EXTRACT(EPOCH FROM (rn.end_date_time - rn.start_date_time)) / 60 AS durasi_nonton
            FROM
                riwayat_nonton rn
            WHERE
                rn.id_tayangan = %s
        )
        SELECT
            COUNT(*) AS jumlah_view
        FROM
            durasi_nonton dn
        JOIN
            durasi_tayangan dt ON dn.id_tayangan = dt.id_tayangan
        WHERE
            dn.durasi_nonton >= dt.min_durasi_view;
    """), [id_series, id_series])
    
    viewers = cur.fetchone()

    conn.close()
    return viewers

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
    try:
        cur.execute(sql.SQL("""
            SET search_path TO pacilflix;
            INSERT INTO ulasan (id_tayangan, username, timestamp, rating, deskripsi)
            VALUES (%s, %s, NOW(), %s, %s);
        """), [id_tayangan, username, rating, deskripsi])
        
        conn.commit()
    except errors.UniqueViolation:
        conn.rollback()
        return 'Ulasan untuk tayangan ini oleh pengguna ini sudah ada.'
    except Exception as e:
        conn.rollback()
        return str(e)
    finally:
        conn.close()
    return None

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
    
def get_top_ten():
    conn = initialize_connection()
    cur = conn.cursor()
    cur.execute(sql.SQL("""
        SET search_path TO pacilflix;
        WITH watched_durations AS (
            SELECT
                rn.id_tayangan,
                (EXTRACT(EPOCH FROM (rn.end_date_time - rn.start_date_time)) / 60) AS watched_minutes
            FROM
                riwayat_nonton rn
            WHERE
                rn.start_date_time >= NOW() - INTERVAL '7 days'
        ),
        film_views AS (
            SELECT
                wd.id_tayangan,
                COUNT(*) AS views,
                'film' AS type
            FROM
                watched_durations wd
            JOIN
                film f ON wd.id_tayangan = f.id_tayangan
            WHERE
                wd.watched_minutes >= (f.durasi_film * 0.7)
            GROUP BY
                wd.id_tayangan
        ),
        episode_views AS (
            SELECT
                e.id_series AS id_tayangan,
                COUNT(DISTINCT rn.username) AS views,
                'series' AS type
            FROM
                watched_durations wd
            JOIN
                episode e ON wd.id_tayangan = e.id_series
            JOIN
                riwayat_nonton rn ON wd.id_tayangan = rn.id_tayangan
            WHERE
                wd.watched_minutes >= (e.durasi * 0.7)
                AND rn.start_date_time >= NOW() - INTERVAL '7 days'
            GROUP BY
                e.id_series
        ),
        total_views AS (
            SELECT
                f.id_tayangan,
                f.views,
                f.type
            FROM
                film_views f
            UNION ALL
            SELECT
                s.id_tayangan,
                s.views,
                s.type
            FROM
                episode_views s
        )
        SELECT
            tv.id,
            tv.judul,
            tv.sinopsis_trailer,
            tv.url_video_trailer,
            tv.release_date_trailer,
            COALESCE(tvv.total_views, 0) AS views_in_last_7_days,
            tvv.type
        FROM
            tayangan tv
        LEFT JOIN
            (SELECT id_tayangan, SUM(views) AS total_views, type FROM total_views GROUP BY id_tayangan, type) tvv
        ON
            tv.id = tvv.id_tayangan;
    """))
    top_ten = cur.fetchall()

    conn.close()
    return top_ten

def search_tayangan(query):
    conn = initialize_connection()
    cur = conn.cursor()
    cur.execute(sql.SQL("""
        SET search_path TO pacilflix;
        SELECT 
            t.*, 
            CASE 
                WHEN f.id_tayangan IS NOT NULL THEN 'film' 
                WHEN s.id_tayangan IS NOT NULL THEN 'series' 
            END AS jenis_tayangan
        FROM 
            tayangan t
        LEFT JOIN 
            film f ON t.id = f.id_tayangan
        LEFT JOIN 
            series s ON t.id = s.id_tayangan
        WHERE 
            t.judul ILIKE %s;
    """), ['%' + query + '%'])
    
    tayangan = cur.fetchall()

    conn.close()
    return tayangan

def get_episode(id_series):
    conn = initialize_connection()
    cur = conn.cursor()
    cur.execute(sql.SQL("""
        SET search_path TO pacilflix;
        SELECT
            e.id_series,
            e.sub_judul
        FROM
            episode e
        INNER JOIN
            tayangan t ON e.id_series = t.id
        WHERE
            t.id = %s;
    """), [id_series])
    
    episode = cur.fetchall()

    conn.close()
    return episode

def get_eps_detail(sub_judul):
    conn = initialize_connection()
    cur = conn.cursor()
    cur.execute(sql.SQL("""
        SET search_path TO pacilflix;
        SELECT
            e.sub_judul,
            e.sinopsis,
            e.durasi,
            e.url_video,
            e.release_date,
            t.judul AS judul_tayangan,
            e.id_series
        FROM
            episode e
        INNER JOIN
            tayangan t ON e.id_series = t.id
        WHERE
            e.sub_judul = %s;
    """), [sub_judul])
    
    episode = cur.fetchone()

    conn.close()
    return episode

def insert_riwayat_nonton(id_tayangan, username, start_date_time, end_date_time):
    conn = initialize_connection()
    cur = conn.cursor()
    
    cur.execute(sql.SQL("""
        SET search_path TO pacilflix;
        INSERT INTO riwayat_nonton (id_tayangan, username, start_date_time, end_date_time)
        VALUES (%s, %s, %s, %s);
    """), [id_tayangan, username, start_date_time, end_date_time])
        
    conn.commit()
    conn.close()
    
def get_durasi_series(id_series):
    conn = initialize_connection()
    cur = conn.cursor()
    cur.execute(sql.SQL("""
        SET search_path TO pacilflix;
        SELECT SUM(durasi) AS total_durasi
        FROM episode
        WHERE id_series = %s
        GROUP BY id_series;
    """), [id_series])
    
    durasi_series = cur.fetchone()

    conn.close()
    return durasi_series