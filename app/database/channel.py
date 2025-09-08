import psycopg2
import os

def get_pg_connection():
    return psycopg2.connect(
        dbname=os.getenv('POSTGRES_DB', 'linebot'),
        user=os.getenv('POSTGRES_USER', 'postgres'),
        password=os.getenv('POSTGRES_PASSWORD', 'password'),
        host=os.getenv('POSTGRES_HOST', 'localhost'),
        port=os.getenv('POSTGRES_PORT', '5432')
    )
import logging
import datetime
import uuid
from database.primary import primary
from common.context import eventcontext

logger = logging.getLogger()
logger.setLevel(logging.ERROR)


class channel:
    # レコードを辞書形式に変換
    tableName = "linebot_chatgpt_channel"
    event_context = None
    primary = None

    def __init__(self, event_context: eventcontext):
        self.event_context = event_context
        self.primary = primary(self.event_context)

    def to_item(self, record):
        return {
            'channelid': record.get('channelid'),
            'userid': record.get('userid'),
            'type': record.get('type'),
            'actionid': record.get('actionid'),
            'memory': record.get('memory'),
            'prompt': record.get('prompt'),
            'setting': record.get('setting'),
            'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            'create_datetime': record.get('create_datetime'),
        }

    # 現在のチャンネルIDのレコードを取得
    def get_record(self):
        return self.get_record_ref(self.primary.get_channelid())

    # 指定チャンネルID・ユーザーIDのレコードを取得。なければ新規作成
    def get_record_ref(self, channelid):
        conn = get_pg_connection()
        cur = conn.cursor()
        cur.execute(f"""
            SELECT * FROM {self.tableName}
            WHERE channelid = %s AND userid = %s
        """, (channelid, self.primary.get_userid()))
        row = cur.fetchone()
        if row:
            columns = [desc[0] for desc in cur.description]
            item = dict(zip(columns, row))
        else:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            new_id = str(uuid.uuid4())
            item = {
                'id': new_id,
                'channelid': channelid,
                'userid': self.primary.get_userid(),
                'type': self.primary.get_type(),
                'actionid': 0,
                'memory': 0,
                'prompt': None,
                'setting': True,
                'timestamp': timestamp,
                'create_datetime': timestamp,
            }
            cur.execute(f"""
                INSERT INTO {self.tableName} (id, channelid, userid, type, actionid, memory, prompt, setting, timestamp, create_datetime)
                VALUES (%(id)s, %(channelid)s, %(userid)s, %(type)s, %(actionid)s, %(memory)s, %(prompt)s, %(setting)s, %(timestamp)s, %(create_datetime)s)
            """, (item))
            conn.commit()
        cur.close()
        conn.close()
        return item

    # 現在のチャンネルIDのactionidを更新
    def add_action(self, actionid):
        self.add_action_ref(self.primary.get_channelid(), actionid)

    # 指定チャンネルID・ユーザーIDのactionidを更新
    def add_action_ref(self, channelid, actionid):
        conn = get_pg_connection()
        cur = conn.cursor()
        cur.execute(f"""
            UPDATE {self.tableName} SET actionid = %s, timestamp = %s
            WHERE channelid = %s AND userid = %s
        """, (actionid, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"), channelid, self.primary.get_userid()))
        conn.commit()
        cur.close()
        conn.close()

    # 現在のチャンネルIDのmemoryを更新
    def add_memory(self, memory: int):
        self.add_memory_ref(self.primary.get_channelid(), memory)

    # 指定チャンネルID・ユーザーIDのmemoryを更新
    def add_memory_ref(self, channelid, memory: int):
        conn = get_pg_connection()
        cur = conn.cursor()
        cur.execute(f"""
            UPDATE {self.tableName} SET memory = %s, timestamp = %s
            WHERE channelid = %s AND userid = %s
        """, (memory, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"), channelid, self.primary.get_userid()))
        conn.commit()
        cur.close()
        conn.close()

    # 現在のチャンネルIDのpromptを更新
    def add_prompt(self, prompt):
        self.add_prompt_ref(self.primary.get_channelid(), prompt)

    # 指定チャンネルID・ユーザーIDのpromptを更新
    def add_prompt_ref(self, channelid, prompt):
        conn = get_pg_connection()
        cur = conn.cursor()
        cur.execute(f"""
            UPDATE {self.tableName} SET prompt = %s, timestamp = %s
            WHERE channelid = %s AND userid = %s
        """, (prompt, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"), channelid, self.primary.get_userid()))
        conn.commit()
        cur.close()
        conn.close()

    # 指定チャンネルID・ユーザーIDのsettingを更新
    def add_setting(self, channelid, setting):
        conn = get_pg_connection()
        cur = conn.cursor()
        cur.execute(f"""
            UPDATE {self.tableName} SET setting = %s, timestamp = %s
            WHERE channelid = %s AND userid = %s
        """, (setting, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"), channelid, self.primary.get_userid()))
        conn.commit()
        cur.close()
        conn.close()

    # 現在のチャンネルIDのactionidを0にリセット
    def reset(self):
        self.reset_ref(self.primary.get_channelid())

    # 指定チャンネルID・ユーザーIDのactionidを0にリセット
    def reset_ref(self, channelid):
        conn = get_pg_connection()
        cur = conn.cursor()
        cur.execute(f"""
            UPDATE {self.tableName} SET actionid = 0, timestamp = %s
            WHERE channelid = %s AND userid = %s
        """, (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"), channelid, self.primary.get_userid()))
        conn.commit()
        cur.close()
        conn.close()

    # 現在のチャンネルIDの全レコードを同期
    def sync(self):
        self.sync_ref(self.primary.get_channelid())

    # 指定チャンネルIDの全レコードを最新値で同期
    def sync_ref(self, channelid):
        print("sync start")
        conn = get_pg_connection()
        cur = conn.cursor()
        # 指定channelidの全レコード取得
        cur.execute(f"SELECT * FROM {self.tableName} WHERE channelid = %s", (channelid,))
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        items = [dict(zip(columns, row)) for row in rows]
        if items:
            # timestamp昇順で最新を取得
            items_sorted = sorted(items, key=lambda x: x['timestamp'])
            source = items_sorted[-1]
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            for item in items:
                cur.execute(f"""
                    UPDATE {self.tableName}
                    SET type = %s, actionid = %s, memory = %s, prompt = %s, timestamp = %s
                    WHERE channelid = %s AND userid = %s
                """,
                (source['type'], source['actionid'], source['memory'], source['prompt'], timestamp, item['channelid'], item['userid']))
            conn.commit()
        cur.close()
        conn.close()
        print("sync done")

    # 全チャンネルレコードを取得
    def get_channels(self):
        conn = get_pg_connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {self.tableName}")
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        items = [dict(zip(columns, row)) for row in rows]
        cur.close()
        conn.close()
        return items

    # setting=True のチャンネルレコードのみ取得
    def get_target_channels(self):
        conn = get_pg_connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {self.tableName} WHERE setting = TRUE")
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        items = [dict(zip(columns, row)) for row in rows]
        cur.close()
        conn.close()
        return items
