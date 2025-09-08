from common.context import eventcontext


class primary:
    event_context = None

    def __init__(self, event_context: eventcontext):
        self.event_context = event_context

    def get_channelid(self):
        type = self.event_context.line_event.source.type
        channelid = None
        if type == "user":
            channelid = self.event_context.line_event.source.user_id
        elif type == "group":
            channelid = self.event_context.line_event.source.group_id
        elif type == "room":
            channelid = self.event_context.line_event.source.room_id
        else:
            pass
        return channelid

    def get_type(self):
        return self.event_context.line_event.source.type

    def get_message_type(self):
        return self.event_context.line_event.message.type

    def get_userid(self):
        return self.event_context.line_event.source.user_id
