import json
import pandas as pd
from database.channel import channel
from common.context import eventcontext


class stickercommand:
    def __init__(self, name, caption, type, action_id):
        self.name = name
        self.caption = caption
        self.type = type
        self.action_id = action_id


class stickerresponce:
    list = None
    df = None
    event_context = None
    channel = None

    def __init__(self, event_context: eventcontext):
        with open("stickercommand.json") as f:
            self.list = json.load(f)
        self.df = pd.DataFrame(self.list["command"])
        self.event_context = event_context
        self.channel = channel(self.event_context)
        print(self.list)
        print(self.df)

    def get_message(self):
        # self.channel.sync()
        message_packageid = self.event_context.line_event.message.package_id
        message_stickerid = self.event_context.line_event.message.sticker_id
        action = self.get_action(message_packageid, message_stickerid)
        msg = None
        caption = "None"
        if action != None:
            caption = self.get_caption(action)
        msg = "package_id:{0} \n" \
            "sticker_id:{1} \n" \
            "{2}".format(
                message_packageid, message_stickerid, caption)
        return msg

    def get_action(self, package_id: int, sticker_id: int):
        print("{}:{}".format(package_id, sticker_id))
        query = "package_id == {} & sticker_id == {}".format(
            package_id, sticker_id)
        records = self.df.query(query)
        print(records)
        action = None
        if not records.empty:
            record = records.to_dict(orient="records")[0]
            action = stickercommand(
                record["name"], record["caption"], record["type"], record["action_id"])
        print(action)
        return action

    def get_caption(self, action):
        caption = action.caption
        self.channel.add_action(action.action_id)
        if action.type == "receive":
            if action.action_id == 6 or action.action_id == 7:
                record = self.channel.get_target_channels()
                channels = []
                for idx, val in enumerate(record):
                    channels.append("{} : {} | {} {}".format(
                        idx, val["setting"], val["type"], val["channelId"]))
                caption = "{}\n{}".format(caption, "\n".join(channels))
        else:
            if action.action_id == 2:
                record = self.channel.get_record()
                caption = f"{caption}\n'memory':{record.get('memory')}\n'prompt':{record.get('prompt')}"
        return caption
