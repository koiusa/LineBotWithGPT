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

def create_table():
    sql = '''
    CREATE TABLE IF NOT EXISTS linebot_chatgpt_history (
        id UUID PRIMARY KEY,
        channelid VARCHAR(128),
        userid VARCHAR(128),
        type VARCHAR(32),
        message TEXT,
        timestamp TIMESTAMP
    );
    '''
    conn = get_pg_connection()
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
    print('History table created.')

if __name__ == '__main__':
    create_table()
