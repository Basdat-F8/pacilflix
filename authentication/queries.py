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

def login(username, password):
    result = []
    conn = initialize_connection()
    cur = conn.cursor()
    cur.execute(sql.SQL("""
        SELECT * FROM pacilflix.pengguna
        WHERE username = %s AND password = %s
    """), [username, password])
    
    user_data = cur.fetchall()
    result.append(user_data)

    conn.close()
    return result

def register(username, password, negara_asal):
    conn = initialize_connection()
    cur = conn.cursor()
    
    try:
        cur.execute(sql.SQL("INSERT INTO pacilflix.pengguna VALUES (%s, %s, %s)"), [username, password, negara_asal])
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        conn.rollback()
        conn.close()
        raise e