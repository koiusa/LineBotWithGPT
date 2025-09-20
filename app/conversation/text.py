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


class textresponce:
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
        if self.target and self.target.get("channelid"):
            self.channel.sync_ref(self.target.get("channelid"))

    def run_reset(self):
        if not self.is_userchannel():
            self.channel.reset()
        else:
            # 対象チャンネルが無い場合は安全にreset()へフォールバック
            if self.target and self.target.get("channelid"):
                self.channel.reset_ref(self.target.get("channelid"))
            else:
                self.channel.reset()

    def run_delete(self):
        text = self.event_context.line_event.message.text
        msg = None
        if text.lower() == "y":
            if not self.is_userchannel():
                self.histoly.delete_histoly()
            else:
                if self.target and self.target.get("channelid"):
                    self.histoly.delete_histoly_ref(self.target.get("channelid"))
                else:
                    return "対象チャンネルが設定されていません"
            msg = "削除完了しました"
        else:
            msg = "削除キャンセルしました"
        return msg

    def run_prompt(self):
        text = self.event_context.line_event.message.text
        if not self.is_userchannel():
            self.channel.add_prompt(text)
        else:
            if self.target and self.target.get("channelid"):
                self.channel.add_prompt_ref(self.target.get("channelid"), text)
            else:
                return "対象チャンネルが設定されていません"
        msg = "AIの役割を設定しました"
        return msg

    def run_deleteprompt(self):
        text = self.event_context.line_event.message.text
        msg = None
        if text.lower() == "y":
            if not self.is_userchannel():
                self.channel.add_prompt(None)
            else:
                if self.target and self.target.get("channelid"):
                    self.channel.add_prompt_ref(self.target.get("channelid"), None)
                else:
                    return "対象チャンネルが設定されていません"
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
                if self.target and self.target.get("channelid"):
                    self.channel.add_memory_ref(self.target.get("channelid"), num)
                else:
                    return "対象チャンネルが設定されていません"
            msg = "記憶数を[{}]に設定しました".format(num)
        else:
            msg = "設定キャンセルしました"
        return msg

    def run_ignorechannel(self):
        text = self.event_context.line_event.message.text
        if text.isdecimal():
            num = int(text)
            channels = self.channel.get_channels_by_user()
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
            channels = self.channel.get_channels_by_user()
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
