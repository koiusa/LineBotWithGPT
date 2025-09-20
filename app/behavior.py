from linebot.models import (TextSendMessage)
from conversation.text import textresponce
from conversation.image import imageresponce
from conversation.sticker import stickerresponce
from conversation.other import otherresponce
from common.context import eventcontext


class completion:
    def behavior(event_context: eventcontext):
        name = None
        if event_context.line_event.message.type in event_context.types:
            name = event_context.line_event.message.type
        else:
            name = "other"
        return globals()["{}{}".format(name, "behavior")]

    def reply(event_context: eventcontext):
        behavior = completion.behavior(event_context)
        behavior.conversation(event_context)


class textbehavior:
    def conversation(event_context: eventcontext):
        responce = textresponce(event_context)
        msg = responce.get_message()
        event_context.reply_message(TextSendMessage(text=msg))

class imagebehavior:
    def conversation(event_context: eventcontext):
        responce = imageresponce(event_context)
        msg = responce.get_message()
        event_context.reply_message(TextSendMessage(text=msg))


class stickerbehavior:
    def conversation(event_context: eventcontext):
        responce = stickerresponce(event_context)
        msg = responce.get_message()
        event_context.reply_message(TextSendMessage(text=msg))


class otherbehavior:
    def conversation(event_context: eventcontext):
        responce = otherresponce(event_context)
        msg = responce.get_message()
        event_context.reply_message(TextSendMessage(text=msg))
