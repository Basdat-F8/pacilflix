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

def hapus_unduhan(username):
    conn = initialize_connection()
    cur = conn.cursor()

    try:
        cur.execute(sql.SQL("""
            DELETE FROM pacilflix.tayangan_terunduh
            WHERE timestamp <= NOW() - INTERVAL '1 day'
            AND username = %s
        """), [username])
        conn.commit()

    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def fetch_unduhan(username):
    conn = initialize_connection()
    cur = conn.cursor()

    try:
        query = """
            SELECT t.judul, tt.timestamp
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

# # Test the fetch_unduhan function
# if __name__ == "__main__":
#     try:
#         username = 'test_username'  # Replace with an actual username for testing
#         unduhan_list = fetch_unduhan(username)
#         for unduhan in unduhan_list:
#             print(unduhan)
#     except Exception as e:
#         print(f"An error occurred: {e}")
