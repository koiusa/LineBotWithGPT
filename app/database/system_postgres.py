import json
import logging
import psycopg2
from database.primary import primary
from common.context import eventcontext
import os

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

def get_pg_connection():
    return psycopg2.connect(
        dbname=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        host=os.getenv('POSTGRES_HOST'),
        port=os.getenv('POSTGRES_PORT')
    )
    
class SystemPostgres:
    def __init__(self):
        self.table_name = "linebot_system" 
    
    def get_system_prompt_json(self):
        """
        system_tableからprompt(json)を取得し、dictとして返す
        """
        conn = get_pg_connection()
        with conn.cursor() as cur:
            cur.execute(f"SELECT prompt FROM {self.table_name} ORDER BY timestamp DESC LIMIT 1")
            row = cur.fetchone()
            print(row)  # 取得した行を確認するためのデバッグ出力
            if row and row[0]:
                import json
                try:
                    return json.loads(row[0])
                except Exception as e:
                    print(f"JSON decode error: {e}")
                    return None
            return None
        conn.close()


    def get_system_prompt_value(self, key):
        """
        prompt(json)からkeyで値を取得
        """
        prompt_json = self.get_system_prompt_json()
        if prompt_json and key in prompt_json:
            return prompt_json[key]
        return None
    
    def add_system_prompt(self, prompt_dict):
        """
        prompt_dict（json/dict）をDBに新規作成or既存UPDATE（最新1件のみ管理）
        """
        conn = get_pg_connection()
        prompt_json = json.dumps(prompt_dict, ensure_ascii=False)
        with conn.cursor() as cur:
            # 既存レコードがあればUPDATE、なければINSERT
            cur.execute(f"SELECT id FROM {self.table_name} ORDER BY timestamp DESC LIMIT 1")
            row = cur.fetchone()
            if row:
                cur.execute(f"UPDATE {self.table_name} SET prompt = %s, timestamp = CURRENT_TIMESTAMP WHERE id = %s", (prompt_json, row[0]))
            else:
                cur.execute(f"INSERT INTO {self.table_name} (prompt) VALUES (%s)", (prompt_json,))
            conn.commit()
        conn.close()
