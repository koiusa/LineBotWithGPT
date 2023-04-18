import boto3
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError
import logging
import datetime
import uuid
import threading
from database.primary import primary
from common.context import eventcontext

logger = logging.getLogger()
logger.setLevel(logging.ERROR)


class histoly:
    tableName = "linebot-chatgpt-history"
    table = None
    event_context = None
    primary = None

    dynamodb = boto3.resource('dynamodb')

    def __init__(self, event_context: eventcontext):
        self.table = self.dynamodb.Table(self.tableName)
        self.event_context = event_context
        self.primary = primary(self.event_context)

    def add_histoly(self, userid, message):
        try:
            self.table.put_item(
                Item={
                    'Id': str(uuid.uuid4()),
                    'channelId': self.primary.get_channelid(),
                    'userId': userid,
                    'type': self.primary.get_type(),
                    'message': message,
                    'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
                })
        except ClientError as err:
            logger.error(
                "Couldn't add history to table %s. Here's why: %s: %s",
                self.table.name,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise

    def delete_histoly(self):
        self.delete_histoly_ref(self.primary.get_channelid())

    def delete_histoly_ref(self, channelId):
        try:
            res = self.table.scan(
                FilterExpression=Attr('channelId').eq(channelId))
            print(res)
            for item in res["Items"]:
                self.table.delete_item(
                    Key={
                        'Id': item["Id"],
                        'channelId': item["channelId"],
                    })
        except ClientError as err:
            logger.error(
                "Couldn't delete history to table %s. Here's why: %s: %s",
                self.table.name,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise

    def get_histoly(self, memory):
        try:
            res = self.table.scan(FilterExpression=Attr(
                'channelId').eq(self.primary.get_channelid()))
            print(res["Items"])

            clean_thread = threading.Thread(target=self.clean_histoly(res))
            clean_thread.start()

            # 最新のメッセージも履歴に含んでいるため
            memory = int(memory if memory is not None else 0)
            count = min(len(res["Items"]), memory+1)
            print(-count)
            res = sorted(
                res["Items"], key=lambda x: x['timestamp'], reverse=False)[-count:]
            print(res)
            return res
        except ClientError as err:
            logger.error(
                "Couldn't delete history to table %s. Here's why: %s: %s",
                self.table.name,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise

    # 履歴が増えすぎないように掃除
    def clean_histoly(self, histoly):
        try:
            limmit = 30
            count = int(len(histoly["Items"])/2)
            if count > limmit:
                target = sorted(
                    histoly["Items"], key=lambda x: x['timestamp'], reverse=False)[0:count]
                for item in target:
                    self.table.delete_item(
                        Key={
                            'Id': item["Id"],
                            'channelId': item["channelId"],
                        })
                print("[{}] Items clean histoly".format(count))
            print("clean dane")
        except ClientError as err:
            logger.error(
                "Couldn't clean history to table %s. Here's why: %s: %s",
                self.table.name,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise

    def to_prompt(self, conversation, system):
        messages = []
        if system != None:
            messages.append({"role": "system", "content": system})
        for record in conversation:
            if record["userId"] == "bot":
                messages.append(
                    {"role": "assistant", "content": record["message"]})
            else:
                messages.append({"role": "user", "content": record["message"]})
        print(messages)
        return messages
