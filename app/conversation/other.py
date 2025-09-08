from common.context import eventcontext


class otherresponce:
    event_context = None

    def __init__(self, event_context: eventcontext):
        self.event_context = event_context

    def get_message(self):
        # message_id = self.event_context.line_event.message.id
        # message_content = self.event_context.line_bot_api.get_message_content(
        #     message_id)
        return "未対応っす"
