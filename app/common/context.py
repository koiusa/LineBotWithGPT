from linebot import (LineBotApi, WebhookHandler)


class eventcontext:
    types = ["text", "sticker"]
    line_event = None
    line_bot_api = None

    def __init__(self, event: WebhookHandler, linebot: LineBotApi):
        self.line_event = event
        self.line_bot_api = linebot
        print(self.line_event)

    def reply_message(self, message):
        self.line_bot_api.reply_message(
            self.line_event.reply_token, message)
