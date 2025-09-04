import logging
import datetime
import uuid
import psycopg2
from database.primary import primary
from common.context import eventcontext
import os

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

class HistolyPostgres:
    def __init__(self, event_context: eventcontext):
        self.event_context = event_context
        self.primary = primary(self.event_context)
        self.conn = psycopg2.connect(
            dbname=os.getenv('POSTGRES_DB'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            host=os.getenv('POSTGRES_HOST'),
            port=os.getenv('POSTGRES_PORT')
        )
        self.table_name = "linebot_chatgpt_history"

    def add_histoly(self, userid, message):
        with self.conn.cursor() as cur:
            cur.execute(f"""
                INSERT INTO {self.table_name} (id, channelid, userid, type, message, timestamp)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                str(uuid.uuid4()),
                self.primary.get_channelid(),
                userid,
                self.primary.get_type(),
                message,
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            ))
            self.conn.commit()

    def delete_histoly(self):
        self.delete_histoly_ref(self.primary.get_channelid())

    def delete_histoly_ref(self, channelid):
        with self.conn.cursor() as cur:
            cur.execute(f"DELETE FROM {self.table_name} WHERE channelid = %s", (channelid,))
            self.conn.commit()

    def get_histoly(self, memory):
        channelid = self.primary.get_channelid()
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT userid, message, timestamp FROM {self.table_name} WHERE channelid = %s ORDER BY timestamp ASC", (channelid,))
            rows = cur.fetchall()
            memory = int(memory if memory is not None else 0)
            count = min(len(rows), memory+1)
            result = []
            for r in rows[-count:]:
                result.append({
                    "userId": r[0],
                    "message": r[1],
                    "timestamp": r[2]
                })
            return result

    def to_prompt(self, conversation, system):
        messages = []
        if system is not None:
            messages.append({"role": "system", "content": system})
        for record in conversation:
            if record[0] == "bot":
                messages.append({"role": "assistant", "content": record[1]})
            else:
                messages.append({"role": "user", "content": record[1]})
        print(messages)
        return messages
