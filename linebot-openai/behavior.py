import openai
from linebot import (LineBotApi, WebhookHandler)
from linebot.models import (
    TextMessage, ImageMessage, StickerMessage, TextSendMessage)
from linebot.exceptions import (LineBotApiError, InvalidSignatureError)
from stickercommand import command


class eventcontext:
    types = ["text", "sticker"]
    line_event = None
    line_bot_api = None

    def __init__(self, event, linebot):
        self.line_event = event
        self.line_bot_api = linebot
        print(self.line_event)

    def reply_message(self, message):
        self.line_bot_api.reply_message(
            self.line_event.reply_token, message)

    def behavior(self):
        name = None
        if self.line_event.message.type in self.types:
            name = self.line_event.message.type
        else:
            name = "other"
        return globals()["{}{}".format(name, "behavior")]


class completion:
    def reply(event_context: eventcontext):
        behavior = event_context.behavior()
        behavior.conversation(event_context)


class textbehavior:
    def conversation(event_context: eventcontext):
        text = event_context.line_event.message.text

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": text}
            ]
        )
        # 受信したテキストをCloudWatchLogsに出力する
        print(completion.choices[0].message.content)
        msg = completion.choices[0].message.content.lstrip()
        event_context.reply_message(TextSendMessage(text=msg))


class stickerbehavior:
    def conversation(event_context: eventcontext):
        cmd = command()
        action_id = cmd.get_actionid(event_context.line_event.message.package_id,
                                     event_context.line_event.message.sticker_id)
        msg = None
        if action_id is None:
            msg = stickerbehavior.default(event_context)
        else:
            msg = stickerbehavior.action(event_context, action_id)
        event_context.reply_message(TextSendMessage(text=msg))

    def default(event_context: eventcontext):
        message_id = event_context.line_event.message.id
        message_packageid = event_context.line_event.message.package_id
        message_stickerid = event_context.line_event.message.sticker_id
        msg = "package_id:{0} \n" \
            "sticker_id:{1} \n" \
            "{2}".format(message_packageid, message_stickerid, "未対応のスタンプっす")
        return msg

    def action(event_context: eventcontext, action_id):
        message_id = event_context.line_event.message.id
        message_packageid = event_context.line_event.message.package_id
        message_stickerid = event_context.line_event.message.sticker_id
        msg = "package_id:{0} \n" \
            "sticker_id:{1} \n" \
            "action_id:{2}".format(
                message_packageid, message_stickerid, action_id)
        return msg


class otherbehavior:
    def conversation(event_context: eventcontext):
        message_id = event_context.line_event.message.id
        message_content = event_context.line_bot_api.get_message_content(
            message_id)
        msg = "その他未対応っす"
        event_context.reply_message(TextSendMessage(text=msg))
