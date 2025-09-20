import openai
import const
import os
import imghdr
import hashlib
from flask import url_for
from database.channel import channel
from database.histoly_postgres import HistolyPostgres
from linebot.models import (TextSendMessage)
from common.context import eventcontext


class imageresponce:
    event_context = None
    channel = None
    histoly = None
    current = None
    target = None

    def __init__(self, event_context: eventcontext):
        self.event_context = event_context
        self.channel = channel(self.event_context)
        self.histoly = HistolyPostgres(self.event_context)

    def get_message(self):
        # get_target_channel() は配列を返すため、1件目をターゲットとして扱う
        items = self.channel.get_target_channel()
        self.target = items[0] if items and len(items) > 0 else None
        # self.run_sync()
        self.current = self.channel.get_record()

        msg = self.run_conversation()

        self.run_reset()
        return msg

    def is_userchannel(self):
        return self.current.get("type") == "user"
        
    def run_reset(self):
        if not self.is_userchannel():
            self.channel.reset()
        else:
            # 対象チャンネルが無い場合は安全にreset()へフォールバック
            if self.target and self.target.get("channelid"):
                self.channel.reset_ref(self.target.get("channelid"))
            else:
                self.channel.reset()

    def run_conversation(self):
        userid = self.event_context.line_event.source.user_id

        line_bot_api = self.event_context.line_bot_api
        message_id = self.event_context.line_event.message.id
        response = line_bot_api.get_message_content(message_id)
        img_bytes = response.content
        ext = imghdr.what(None, img_bytes)
        if ext is None:
            ext = 'jpeg'  # 判定できない場合はjpeg
        import base64
        img_base64 = base64.b64encode(img_bytes).decode("utf-8")
        message = f"data:image/{ext};base64,{img_base64}"

        self.histoly.add_histoly_variable(userid, message, self.event_context.line_event.message.type)

        conversation = self.histoly.get_histoly(self.current.get("memory"))
        prompt = self.histoly.to_prompt(
            conversation, self.current.get("prompt"))
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        completion = client.chat.completions.create(
            model=const.OPENAI_MODEL,
            messages=prompt,
            max_tokens=300
        )
        # 受信したテキストをCloudWatchLogsに出力する
        print(completion.choices[0].message.content)
        msg = completion.choices[0].message.content.lstrip()

        self.histoly.add_histoly_text("bot", msg)
        return msg
