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

def contributors():
    # result = []
    conn = initialize_connection()
    cur = conn.cursor()
    cur.execute(sql.SQL("""
        SELECT 
    nama,
    CASE            
        WHEN id IN (SELECT id FROM pacilflix.penulis_skenario) THEN 'Penulis Skenario'
        WHEN id IN (SELECT id FROM pacilflix.sutradara) THEN 'Sutradara'
        WHEN id IN (SELECT id FROM pacilflix.pemain) THEN 'Pemain' 
        WHEN id IN (SELECT id FROM (
            select id  from pacilflix.penulis_skenario
            union all
            select id from pacilflix.sutradara
        ) ps) THEN 'Penulis Skenario, Sutradara'
        WHEN id IN (SELECT id FROM (
            select id  from pacilflix.sutradara
            union all
            select id from pacilflix.pemain
        ) sp) THEN 'Sutradara, Pemain'
        WHEN id IN (SELECT id FROM (
            select id  from pacilflix.pemain 
            union all
            select id from pacilflix.penulis_skenario
        ) pp) THEN 'Pemain, Penulis Skenario'     
    END AS type,
    CASE
        WHEN jenis_kelamin=0 THEN 'Laki-Laki'
        WHEN jenis_kelamin=1 THEN 'Perempuan'
    END AS jenis_kelamin,
    kewarganegaraan
    FROM 
    pacilflix.contributors;
    """))
    
    list = cur.fetchall()
    # result.append(user_data)

    conn.close()
    return list

def sutradara():
    # result = []
    conn = initialize_connection()
    cur = conn.cursor()
    cur.execute(sql.SQL("""
        SELECT 
    nama,
    'Sutradara' AS type,
    CASE
        WHEN jenis_kelamin=0 THEN 'Laki-Laki'
        WHEN jenis_kelamin=1 THEN 'Perempuan'
    END AS jenis_kelamin,
    kewarganegaraan
    FROM 
    pacilflix.contributors
    WHERE id IN (SELECT id FROM pacilflix.sutradara);
    """))
    
    list = cur.fetchall()
    # result.append(user_data)

    conn.close()
    return list

def pemain():
    # result = []
    conn = initialize_connection()
    cur = conn.cursor()
    cur.execute(sql.SQL("""
        SELECT 
    nama,
    'Pemain' AS type,
    CASE
        WHEN jenis_kelamin=0 THEN 'Laki-Laki'
        WHEN jenis_kelamin=1 THEN 'Perempuan'
    END AS jenis_kelamin,
    kewarganegaraan
    FROM 
    pacilflix.contributors
    WHERE id IN (SELECT id FROM pacilflix.pemain);
    """))
    
    list = cur.fetchall()
    # result.append(user_data)

    conn.close()
    return list

def penulis():
    # result = []
    conn = initialize_connection()
    cur = conn.cursor()
    cur.execute(sql.SQL("""
        SELECT 
    nama,
    'Penulis Skenario' AS type,
    CASE
        WHEN jenis_kelamin=0 THEN 'Laki-Laki'
        WHEN jenis_kelamin=1 THEN 'Perempuan'
    END AS jenis_kelamin,
    kewarganegaraan
    FROM pacilflix.contributors
    WHERE id IN (SELECT id FROM pacilflix.penulis_skenario);
    """))
    
    list = cur.fetchall()
    # result.append(user_data)

    conn.close()
    return list