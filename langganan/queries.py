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

def getcurrent(username):
    # result = []
    conn = initialize_connection()
    cur = conn.cursor()
    cur.execute(sql.SQL("""
        SELECT p.nama AS username, p.harga AS total, p.resolusi_layar AS resolusi_layar, STRING_AGG(dp.dukungan_perangkat, ',') AS dukperangkat, t.start_date_time AS start_date_time, t.end_date_time AS end_date_time
FROM pacilflix.transaction t
JOIN pacilflix.paket p ON t.nama_paket = p.nama
JOIN pacilflix.pengguna pe ON t.username = pe.username
JOIN pacilflix.dukungan_perangkat dp ON p.nama = dp.nama_paket
WHERE t.start_date_time < NOW() AND NOW() < t.end_date_time AND t.username = %s
                        GROUP BY p.nama, t.start_date_time, t.end_date_time
ORDER BY t.start_date_time DESC
LIMIT 1
;
    """), [username])
    
    current = cur.fetchone()
    if current is None:
            print("No transactions found for user:", username)
            return None
    print(current)
    # result.append(user_data)

    conn.close()
    return current

def getpacks():
    conn = initialize_connection()
    cur = conn.cursor()
    cur.execute(sql.SQL("""
        SELECT
            paket.nama AS nama, paket.harga AS harga, paket.resolusi_layar AS resolusi,
            STRING_AGG(dukper.dukungan_perangkat, ',') AS dukperangkat
        FROM
            pacilflix.paket paket
        JOIN
            pacilflix.dukungan_perangkat dukper ON paket.nama = dukper.nama_paket
        GROUP BY
    paket.nama;
    """))
    
    package = cur.fetchall()
    # result.append(user_data)

    conn.close()
    return package
    
def gethistory(username):
    # result = []
    conn = initialize_connection()
    cur = conn.cursor()
    cur.execute(sql.SQL("""
        SELECT nama_paket, start_date_time, end_date_time, metode_pembayaran, timestamp_pembayaran,
                        CASE
        WHEN nama_paket = 'premium' THEN '269000'
        WHEN nama_paket = 'basic' THEN '159000'
        WHEN nama_paket = 'standar' THEN '219000'  
        END AS total
        FROM pacilflix.transaction 
        WHERE pacilflix.transaction.username = %s;
    """), [username])
    
    history = cur.fetchall()
    # result.append(user_data)

    conn.close()
    return history

def whatbuy(pack):
    # result = []
    conn = initialize_connection()
    cur = conn.cursor()
    cur.execute(sql.SQL("""
        SELECT
            pacilflix.paket.nama, pacilflix.paket.harga, pacilflix.paket.resolusi_layar,
            ARRAY_AGG(pacilflix.dukungan_perangkat.dukungan_perangkat ORDER BY pacilflix.dukungan_perangkat.dukungan_perangkat) AS Dukungan Perangkat
        FROM (
            SELECT pacilflix.paket.nama
            FROM pacilflix.paket
            LIMIT 3
        ) pacilflix.paket
        JOIN (
            SELECT pacilflix.dukungan_perangkat.nama, pacilflix.dukungan_perangkat.dukungan_perangkat
            FROM table2
            ORDER BY pacilflix.dukungan_perangkat.nama, pacilflix.dukungan_perangkat.dukungan_perangkat
        ) pacilflix.dukungan_perangkat ON pacilflix.paket.nama = pacilflix.dukungan_perangkat.nama
        WHERE pacilflix.paket.nama LIKE '%pack%'
        GROUP BY pacilflix.paket.nama;
    """), [pack])
    
    purchase = cur.fetchone()
    # result.append(user_data)

    conn.close()
    return purchase

def buypremium(username,  metode):
    # result = []
    conn = initialize_connection()
    cur = conn.cursor()
    cur.execute(sql.SQL("""
    INSERT INTO pacilflix.transaction (username, start_date_time, end_date_time, nama_paket, metode_pembayaran, timestamp_pembayaran)
    VALUES (%s, DATE(CURRENT_TIMESTAMP), DATE(CURRENT_TIMESTAMP)+ INTERVAL '1 year', 'premium', %s, NOW());
    """), [username, metode])
    
    conn.commit()
    cur.close()
    conn.close()

def buybasic(username,  metode):
    # result = []
    conn = initialize_connection()
    cur = conn.cursor()
    cur.execute(sql.SQL("""
    INSERT INTO pacilflix.transaction (username, start_date_time, end_date_time, nama_paket, metode_pembayaran, timestamp_pembayaran)
    VALUES (%s, DATE(CURRENT_TIMESTAMP), DATE(CURRENT_TIMESTAMP)+ INTERVAL '1 year', 'basic', %s, NOW());
    """), [username, metode])
    
    conn.commit()
    cur.close()
    conn.close()

def buystandard(username,  metode):
    # result = []
    conn = initialize_connection()
    cur = conn.cursor()
    cur.execute(sql.SQL("""
    INSERT INTO pacilflix.transaction (username, start_date_time, end_date_time, nama_paket, metode_pembayaran, timestamp_pembayaran)
    VALUES (%s, DATE(CURRENT_TIMESTAMP), DATE(CURRENT_TIMESTAMP)+ INTERVAL '1 year', 'standar' , %s, NOW());
    """), [username, metode])
    
    conn.commit()
    cur.close()
    conn.close()

