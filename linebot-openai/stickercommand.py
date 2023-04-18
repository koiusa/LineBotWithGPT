import json
import pandas as pd


class command:
    list = None
    df = None

    def __init__(self):
        with open("stickercommand.json") as f:
            self.list = json.load(f)
        self.df = pd.DataFrame(self.list["command"])
        print(self.list)
        print(self.df)

    def get_actionid(self, package_id: int, sticker_id: int):
        print("{}:{}".format(package_id, sticker_id))
        query = "package_id == {} & sticker_id == {}".format(
            package_id, sticker_id)
        records = self.df.query(query)
        print(records)
        action = None
        if not records.empty:
            dic_record = records.to_dict(orient="records")
            action = dic_record[0]["action_id"]
        print(action)
        return action
