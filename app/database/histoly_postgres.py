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

    def add_histoly_variable(self, userid, message, type):
        with self.conn.cursor() as cur:
            cur.execute(f"""
                INSERT INTO {self.table_name} (id, channelid, userid, type, message, timestamp)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                str(uuid.uuid4()),
                self.primary.get_channelid(),
                userid,
                type,
                message,
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            ))
            self.conn.commit()
    
    def add_histoly_text(self, userid, message):
        self.add_histoly_variable(userid, message, "text")

    def delete_histoly(self):
        self.delete_histoly_ref(self.primary.get_channelid())

    def delete_histoly_ref(self, channelid):
        with self.conn.cursor() as cur:
            cur.execute(f"DELETE FROM {self.table_name} WHERE channelid = %s", (channelid,))
            self.conn.commit()

    def get_histoly(self, memory):
        channelid = self.primary.get_channelid()
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT userid, message, type, timestamp FROM {self.table_name} WHERE channelid = %s ORDER BY timestamp ASC", (channelid,))
            rows = cur.fetchall()
            memory = int(memory if memory is not None else 0)
            count = min(len(rows), memory+1)
            result = []
            for r in rows[-count:]:
                result.append({
                    "userid": r[0],
                    "message": r[1],
                    "type": r[2],
                    "timestamp": r[3]
                })
            return result

    def to_prompt(self, conversation, system):
        messages = []
        # system prompt（AIの役割）
        if system is not None:
            messages.append({
                "role": "system",
                "content": [
                    {"type": "text", "text": system}
                ]
            })
        for record in conversation:
            role = "assistant" if record.get("userid") == "bot" else "user"
            rtype = record.get("type", "text")
            message = record.get("message", "")
            if rtype == "image":
                messages.append({
                    "role": role,
                    "content": [
                        {"type": "image_url", "image_url": {"url": message}}
                    ]
                })
            else:
                messages.append({
                    "role": role,
                    "content": [
                        {"type": "text", "text": message}
                    ]
                })
        print(messages)
        return messages
