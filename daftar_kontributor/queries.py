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
    SELECT nama,
       CASE
           WHEN t1.id IN (SELECT t2.id FROM pacilflix.penulis_skenario t2)
                AND t1.id IN (SELECT t3.id FROM pacilflix.sutradara t3)
                AND t1.id NOT IN (SELECT t2.id
                                  FROM pacilflix.penulis_skenario t2
                                  LEFT JOIN pacilflix.sutradara t3 ON t2.id = t3.id
                                  WHERE t3.id IS NULL)
           THEN 'Penulis Skenario, Sutradara'
           
           WHEN t1.id IN (SELECT t2.id FROM pacilflix.penulis_skenario t2)
                AND t1.id IN (SELECT t4.id FROM pacilflix.pemain t4)
                AND t1.id NOT IN (SELECT t2.id
                                  FROM pacilflix.penulis_skenario t2
                                  LEFT JOIN pacilflix.pemain t4 ON t2.id = t4.id
                                  WHERE t4.id IS NULL)
           THEN 'Penulis Skenario, Pemain'
           
           WHEN t1.id IN (SELECT t3.id FROM pacilflix.sutradara t3)
                AND t1.id IN (SELECT t4.id FROM pacilflix.pemain t4)
                AND t1.id NOT IN (SELECT t3.id
                                  FROM pacilflix.sutradara t3
                                  LEFT JOIN pacilflix.pemain t4 ON t3.id = t4.id
                                  WHERE t4.id IS NULL)
           THEN 'Sutradara, Pemain'
           
           WHEN t1.id IN (SELECT t2.id FROM pacilflix.penulis_skenario t2)
                AND t1.id IN (SELECT t3.id FROM pacilflix.sutradara t3)
                AND t1.id IN (SELECT t4.id FROM pacilflix.pemain t4)
                AND t1.id NOT IN (SELECT t2.id
                                  FROM pacilflix.penulis_skenario t2
                                  LEFT JOIN pacilflix.sutradara t3 ON t2.id = t3.id
                                  LEFT JOIN pacilflix.pemain t4 ON t2.id = t4.id
                                  WHERE t3.id IS NULL OR t4.id IS NULL)
           THEN 'Penulis Skenario, Sutradara, Pemain'
           WHEN id IN (SELECT id FROM pacilflix.penulis_skenario) THEN 'Penulis Skenario'
            WHEN id IN (SELECT id FROM pacilflix.sutradara) THEN 'Sutradara'
            WHEN id IN (SELECT id FROM pacilflix.pemain) THEN 'Pemain' 
           ELSE 'Tidak ada Role'
       END AS type,
    CASE
        WHEN jenis_kelamin=0 THEN 'Laki-Laki'
        WHEN jenis_kelamin=1 THEN 'Perempuan'
    END AS jenis_kelamin,
    kewarganegaraan
    FROM 
    pacilflix.contributors t1;
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
    CASE
           WHEN t1.id IN (SELECT t2.id FROM pacilflix.penulis_skenario t2)
                AND t1.id IN (SELECT t3.id FROM pacilflix.sutradara t3)
                AND t1.id NOT IN (SELECT t2.id
                                  FROM pacilflix.penulis_skenario t2
                                  LEFT JOIN pacilflix.sutradara t3 ON t2.id = t3.id
                                  WHERE t3.id IS NULL)
           THEN 'Penulis Skenario, Sutradara'
           
           WHEN t1.id IN (SELECT t2.id FROM pacilflix.penulis_skenario t2)
                AND t1.id IN (SELECT t4.id FROM pacilflix.pemain t4)
                AND t1.id NOT IN (SELECT t2.id
                                  FROM pacilflix.penulis_skenario t2
                                  LEFT JOIN pacilflix.pemain t4 ON t2.id = t4.id
                                  WHERE t4.id IS NULL)
           THEN 'Penulis Skenario, Pemain'
           
           WHEN t1.id IN (SELECT t3.id FROM pacilflix.sutradara t3)
                AND t1.id IN (SELECT t4.id FROM pacilflix.pemain t4)
                AND t1.id NOT IN (SELECT t3.id
                                  FROM pacilflix.sutradara t3
                                  LEFT JOIN pacilflix.pemain t4 ON t3.id = t4.id
                                  WHERE t4.id IS NULL)
           THEN 'Sutradara, Pemain'
           
           WHEN t1.id IN (SELECT t2.id FROM pacilflix.penulis_skenario t2)
                AND t1.id IN (SELECT t3.id FROM pacilflix.sutradara t3)
                AND t1.id IN (SELECT t4.id FROM pacilflix.pemain t4)
                AND t1.id NOT IN (SELECT t2.id
                                  FROM pacilflix.penulis_skenario t2
                                  LEFT JOIN pacilflix.sutradara t3 ON t2.id = t3.id
                                  LEFT JOIN pacilflix.pemain t4 ON t2.id = t4.id
                                  WHERE t3.id IS NULL OR t4.id IS NULL)
           THEN 'Penulis Skenario, Sutradara, Pemain'
           WHEN id IN (SELECT id FROM pacilflix.penulis_skenario) THEN 'Penulis Skenario'
            WHEN id IN (SELECT id FROM pacilflix.sutradara) THEN 'Sutradara'
            WHEN id IN (SELECT id FROM pacilflix.pemain) THEN 'Pemain' 
           ELSE 'Tidak ada Role'
       END AS type,
    CASE
        WHEN jenis_kelamin=0 THEN 'Laki-Laki'
        WHEN jenis_kelamin=1 THEN 'Perempuan'
    END AS jenis_kelamin,
    kewarganegaraan
    FROM 
    pacilflix.contributors t1
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
    CASE
           WHEN t1.id IN (SELECT t2.id FROM pacilflix.penulis_skenario t2)
                AND t1.id IN (SELECT t3.id FROM pacilflix.sutradara t3)
                AND t1.id NOT IN (SELECT t2.id
                                  FROM pacilflix.penulis_skenario t2
                                  LEFT JOIN pacilflix.sutradara t3 ON t2.id = t3.id
                                  WHERE t3.id IS NULL)
           THEN 'Penulis Skenario, Sutradara'
           
           WHEN t1.id IN (SELECT t2.id FROM pacilflix.penulis_skenario t2)
                AND t1.id IN (SELECT t4.id FROM pacilflix.pemain t4)
                AND t1.id NOT IN (SELECT t2.id
                                  FROM pacilflix.penulis_skenario t2
                                  LEFT JOIN pacilflix.pemain t4 ON t2.id = t4.id
                                  WHERE t4.id IS NULL)
           THEN 'Penulis Skenario, Pemain'
           
           WHEN t1.id IN (SELECT t3.id FROM pacilflix.sutradara t3)
                AND t1.id IN (SELECT t4.id FROM pacilflix.pemain t4)
                AND t1.id NOT IN (SELECT t3.id
                                  FROM pacilflix.sutradara t3
                                  LEFT JOIN pacilflix.pemain t4 ON t3.id = t4.id
                                  WHERE t4.id IS NULL)
           THEN 'Sutradara, Pemain'
           
           WHEN t1.id IN (SELECT t2.id FROM pacilflix.penulis_skenario t2)
                AND t1.id IN (SELECT t3.id FROM pacilflix.sutradara t3)
                AND t1.id IN (SELECT t4.id FROM pacilflix.pemain t4)
                AND t1.id NOT IN (SELECT t2.id
                                  FROM pacilflix.penulis_skenario t2
                                  LEFT JOIN pacilflix.sutradara t3 ON t2.id = t3.id
                                  LEFT JOIN pacilflix.pemain t4 ON t2.id = t4.id
                                  WHERE t3.id IS NULL OR t4.id IS NULL)
           THEN 'Penulis Skenario, Sutradara, Pemain'
           WHEN id IN (SELECT id FROM pacilflix.penulis_skenario) THEN 'Penulis Skenario'
            WHEN id IN (SELECT id FROM pacilflix.sutradara) THEN 'Sutradara'
            WHEN id IN (SELECT id FROM pacilflix.pemain) THEN 'Pemain' 
           ELSE 'Tidak ada Role'
       END AS type,
    CASE
        WHEN jenis_kelamin=0 THEN 'Laki-Laki'
        WHEN jenis_kelamin=1 THEN 'Perempuan'
    END AS jenis_kelamin,
    kewarganegaraan
    FROM 
    pacilflix.contributors t1
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
    CASE
           WHEN t1.id IN (SELECT t2.id FROM pacilflix.penulis_skenario t2)
                AND t1.id IN (SELECT t3.id FROM pacilflix.sutradara t3)
                AND t1.id NOT IN (SELECT t2.id
                                  FROM pacilflix.penulis_skenario t2
                                  LEFT JOIN pacilflix.sutradara t3 ON t2.id = t3.id
                                  WHERE t3.id IS NULL)
           THEN 'Penulis Skenario, Sutradara'
           
           WHEN t1.id IN (SELECT t2.id FROM pacilflix.penulis_skenario t2)
                AND t1.id IN (SELECT t4.id FROM pacilflix.pemain t4)
                AND t1.id NOT IN (SELECT t2.id
                                  FROM pacilflix.penulis_skenario t2
                                  LEFT JOIN pacilflix.pemain t4 ON t2.id = t4.id
                                  WHERE t4.id IS NULL)
           THEN 'Penulis Skenario, Pemain'
           
           WHEN t1.id IN (SELECT t3.id FROM pacilflix.sutradara t3)
                AND t1.id IN (SELECT t4.id FROM pacilflix.pemain t4)
                AND t1.id NOT IN (SELECT t3.id
                                  FROM pacilflix.sutradara t3
                                  LEFT JOIN pacilflix.pemain t4 ON t3.id = t4.id
                                  WHERE t4.id IS NULL)
           THEN 'Sutradara, Pemain'
           
           WHEN t1.id IN (SELECT t2.id FROM pacilflix.penulis_skenario t2)
                AND t1.id IN (SELECT t3.id FROM pacilflix.sutradara t3)
                AND t1.id IN (SELECT t4.id FROM pacilflix.pemain t4)
                AND t1.id NOT IN (SELECT t2.id
                                  FROM pacilflix.penulis_skenario t2
                                  LEFT JOIN pacilflix.sutradara t3 ON t2.id = t3.id
                                  LEFT JOIN pacilflix.pemain t4 ON t2.id = t4.id
                                  WHERE t3.id IS NULL OR t4.id IS NULL)
           THEN 'Penulis Skenario, Sutradara, Pemain'
           WHEN id IN (SELECT id FROM pacilflix.penulis_skenario) THEN 'Penulis Skenario'
            WHEN id IN (SELECT id FROM pacilflix.sutradara) THEN 'Sutradara'
            WHEN id IN (SELECT id FROM pacilflix.pemain) THEN 'Pemain' 
           ELSE 'Tidak ada Role'
       END AS type,
    CASE
        WHEN jenis_kelamin=0 THEN 'Laki-Laki'
        WHEN jenis_kelamin=1 THEN 'Perempuan'
    END AS jenis_kelamin,
    kewarganegaraan
    FROM pacilflix.contributors t1
    WHERE id IN (SELECT id FROM pacilflix.penulis_skenario);
    """))
    
    list = cur.fetchall()
    # result.append(user_data)

    conn.close()
    return list