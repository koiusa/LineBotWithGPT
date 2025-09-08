import psycopg2
import os

def get_pg_connection():
    return psycopg2.connect(
        dbname=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        host=os.getenv('POSTGRES_HOST'),
        port=os.getenv('POSTGRES_PORT')
    )

def create_system_table():
    conn = get_pg_connection()
    with conn.cursor() as cur:
        cur.execute('''
            CREATE TABLE IF NOT EXISTS linebot_system (
                id SERIAL PRIMARY KEY,
                prompt TEXT NOT NULL,
                timestamp TIMESTAMP,
                create_datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        conn.commit()
    conn.close()
    print("linebot_system テーブル作成完了")

if __name__ == "__main__":
    create_system_table()
