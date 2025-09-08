import openai
import const
import os
import imghdr
import hashlib
from flask import url_for
from werkzeug.utils import secure_filename
from database.channel import channel
from database.histoly_postgres import HistolyPostgres
from linebot.models import (TextSendMessage)
from common.context import eventcontext


class textresponce:
    event_context = None
    channel = None
    histoly = None
    current = None
    targets = None

    def __init__(self, event_context: eventcontext):
        self.event_context = event_context
        self.channel = channel(self.event_context)
        self.histoly = HistolyPostgres(self.event_context)

    def get_message(self):
        self.targets = self.channel.get_target_channels()
        # self.run_sync()
        msg = None

        self.current = self.channel.get_record()
        actionid = self.current.get("actionid")
        if actionid == 1:
            msg = self.run_prompt()
        elif actionid == 3:
            msg = self.run_delete()
        elif actionid == 4:
            msg = self.run_memory()
        elif actionid == 5:
            msg = self.run_deleteprompt()
        elif actionid == 6:
            msg = self.run_ignorechannel()
        elif actionid == 7:
            msg = self.run_aimchannel()
        else:
            msg = self.run_conversation()

        self.run_reset()
        return msg

    def is_userchannel(self):
        return self.current.get("type") == "user"

    def run_sync(self):
        self.channel.sync()
        for target in self.targets:
            self.channel.sync_ref(target.get("channelid"))

    def run_reset(self):
        if not self.is_userchannel():
            self.channel.reset()
        else:
            for target in self.targets:
                self.channel.reset_ref(target.get("channelid"))

    def run_delete(self):
        text = self.event_context.line_event.message.text
        msg = None
        if text.lower() == "y":
            if not self.is_userchannel():
                self.histoly.delete_histoly()
            else:
                for target in self.targets:
                    self.histoly.delete_histoly_ref(target.get("channelid"))
            msg = "削除完了しました"
        else:
            msg = "削除キャンセルしました"
        return msg

    def run_prompt(self):
        text = self.event_context.line_event.message.text
        if not self.is_userchannel():
            self.channel.add_prompt(text)
        else:
            for target in self.targets:
                self.channel.add_prompt_ref(target.get("channelid"), text)
        msg = "AIの役割を設定しました"
        return msg

    def run_deleteprompt(self):
        text = self.event_context.line_event.message.text
        msg = None
        if text.lower() == "y":
            if not self.is_userchannel():
                self.channel.add_prompt(None)
            else:
                for target in self.targets:
                    self.channel.add_prompt_ref(target.get("channelid"), None)
            msg = "AIの役割を削除しました"
        else:
            msg = "削除キャンセルしました"
        return msg

    def run_memory(self):
        text = self.event_context.line_event.message.text

        if text.isdecimal():
            num = int(text)
            if num > 10:
                num = 10
            if not self.is_userchannel():
                self.channel.add_memory(num)
            else:
                for target in self.targets:
                    self.channel.add_memory_ref(target.get("channelid"), num)
            msg = "記憶数を[{}]に設定しました".format(num)
        else:
            msg = "設定キャンセルしました"
        return msg

    def run_ignorechannel(self):
        text = self.event_context.line_event.message.text
        if text.isdecimal():
            num = int(text)
            channels = self.channel.get_channels()
            if len(channels) > num:
                self.channel.add_setting(channels[num].get('channelid'), False)
                # self.event_context.line_bot_api.push_message(
                #     channels[num].get('channelid'), TextSendMessage(text="[ユーザー：{}]の操作対象から削除されました。".format(
                #         channels[num].get('userid'))))
                msg = "[{}]を操作対象から削除しました。".format(num)
            else:
                msg = "削除キャンセルしました"
        else:
            msg = "削除キャンセルしました"
        return msg

    def run_aimchannel(self):
        text = self.event_context.line_event.message.text
        if text.isdecimal():
            num = int(text)
            channels = self.channel.get_channels()
            if len(channels) > num:
                self.channel.add_setting(channels[num].get('channelid'), True)
                # self.event_context.line_bot_api.push_message(
                #     channels[num].get('channelid'), TextSendMessage(text="[ユーザー：{}]の操作対象に設定されました。".format(
                #         channels[num].get('userid'))))
                msg = "[{}]を操作対象に設定しました。".format(num)
            else:
                msg = "設定キャンセルしました"
        else:
            msg = "設定キャンセルしました"
        return msg

    def run_conversation(self):
        userid = self.event_context.line_event.source.user_id

        message = None
        if self.event_context.line_event.message.type == "image":
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
        else:
            message = self.event_context.line_event.message.text

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
