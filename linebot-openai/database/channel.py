import boto3
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError
import logging
import datetime
from database.primary import primary
from common.context import eventcontext

logger = logging.getLogger()
logger.setLevel(logging.ERROR)


class channel:
    tableName = "linebot-chatgpt-channel"
    table = None
    event_context = None
    primary = None

    dynamodb = boto3.resource('dynamodb')

    def __init__(self, event_context: eventcontext):
        self.table = self.dynamodb.Table(self.tableName)
        self.event_context = event_context
        self.primary = primary(self.event_context)

    def to_item(self, record):
        return {
            'channelId': record.get('channelId'),
            'userId': record.get('userId'),
            'type': record.get('type'),
            'actionid': record.get('actionid'),
            'memory': record.get('memory'),
            'prompt': record.get('prompt'),
            'setting': record.get('setting'),
            'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            'create_datetime': record.get('create_datetime'),
        }

    def get_record(self):
        return self.get_record_ref(self.primary.get_channelid())

    def get_record_ref(self, channelid):
        try:
            response = self.table.get_item(
                Key={
                    'channelId': channelid,
                    'userId': self.primary.get_userid(),
                })
            print(response)
            if response.get("Item") is None:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                response = {'Item': {
                    'channelId': channelid,
                    'userId': self.primary.get_userid(),
                    'type': self.primary.get_type(),
                    'actionid': 0,
                    'memory': 0,
                    'prompt': None,
                    'setting': True,
                    'timestamp': timestamp,
                    'create_datetime': timestamp,
                }}
            return response.get("Item")
        except ClientError as err:
            logger.error(
                "Couldn't get record to table %s. Here's why: %s: %s",
                self.table.name,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise

    def add_action(self, actionid):
        self.add_action_ref(self.primary.get_channelid(), actionid)

    def add_action_ref(self, channelId, actionid):
        try:
            record = self.get_record_ref(channelId)
            item = self.to_item(record)
            item["channelId"] = channelId
            item["actionid"] = actionid
            self.table.put_item(Item=item)
        except ClientError as err:
            logger.error(
                "Couldn't add action to table %s. Here's why: %s: %s",
                self.table.name,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise

    def add_memory(self, memory: int):
        self.add_memory_ref(self.primary.get_channelid(), memory)

    def add_memory_ref(self, channelId, memory: int):
        try:
            record = self.get_record_ref(channelId)
            item = self.to_item(record)
            item["channelId"] = channelId
            item["memory"] = memory
            self.table.put_item(Item=item)
        except ClientError as err:
            logger.error(
                "Couldn't add memory to table %s. Here's why: %s: %s",
                self.table.name,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise

    def add_prompt(self, prompt):
        self.add_prompt_ref(self.primary.get_channelid(), prompt)

    def add_prompt_ref(self, channelId, prompt):
        try:
            record = self.get_record_ref(channelId)
            item = self.to_item(record)
            item["channelId"] = channelId
            item["prompt"] = prompt
            self.table.put_item(Item=item)
        except ClientError as err:
            logger.error(
                "Couldn't add prompt to table %s. Here's why: %s: %s",
                self.table.name,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise

    def add_setting(self, channelId, setting):
        try:
            record = self.get_record_ref(channelId)
            item = self.to_item(record)
            item["channelId"] = channelId
            item["setting"] = setting
            self.table.put_item(Item=item)
        except ClientError as err:
            logger.error(
                "Couldn't add setting to table %s. Here's why: %s: %s",
                self.table.name,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise

    def reset(self):
        self.reset_ref(self.primary.get_channelid())

    def reset_ref(self, channelid):
        try:
            record = self.get_record_ref(channelid)
            item = self.to_item(record)
            item["actionid"] = 0
            self.table.put_item(Item=item)
        except ClientError as err:
            logger.error(
                "Couldn't reset to table %s. Here's why: %s: %s",
                self.table.name,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise

    def sync(self):
        self.sync_ref(self.primary.get_channelid())

    def sync_ref(self, channelId):
        try:
            print("sync start")
            res = self.table.scan(
                FilterExpression=Attr('channelId').eq(channelId))
            print(res)
            if len(res.get("Items")) > 0:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                source = sorted(
                    res["Items"], key=lambda x: x['timestamp'], reverse=False)[-1]
                for item in res["Items"]:
                    option = {
                        'Key': {'channelId': item["channelId"], 'userId': item["userId"]},
                        'ConditionExpression': '#type = :type',
                        'UpdateExpression': 'set #actionid = :actionid, #memory = :memory, #prompt = :prompt, #timestamp = :timestamp',
                        'ExpressionAttributeNames': {
                            '#type': 'type',
                            '#actionid': 'actionid',
                            '#memory': 'memory',
                            '#prompt': 'prompt',
                            '#timestamp': 'timestamp',
                        },
                        'ExpressionAttributeValues': {
                            ':type': source["type"],
                            ':actionid': source["actionid"],
                            ':memory': source["memory"],
                            ':prompt': source["prompt"],
                            ':timestamp': timestamp}
                    }
                    self.table.update_item(**option)
            print("sync done")
        except ClientError as err:
            logger.error(
                "Couldn't sync channel to table %s. Here's why: %s: %s",
                self.table.name,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise

    def get_channels(self):
        try:
            res = self.table.scan(FilterExpression=Attr('userId').eq(
                self.primary.get_userid()) and Attr('type').ne('user'))
            print(res)
            if len(res.get("Items")) > 0:
                res = {"Items": sorted(
                    res["Items"], key=lambda x: x['create_datetime'], reverse=True)}
            return res.get("Items")
        except ClientError as err:
            logger.error(
                "Couldn't get channel to table %s. Here's why: %s: %s",
                self.table.name,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise

    def get_target_channels(self):
        try:
            res = self.table.scan(FilterExpression=Attr('userId').eq(
                self.primary.get_userid()) and Attr('type').ne('user') and Attr('setting').eq(True))
            print(res)
            if len(res.get("Items")) > 0:
                res = {"Items": sorted(
                    res["Items"], key=lambda x: x['create_datetime'], reverse=True)}
            return res.get("Items")
        except ClientError as err:
            logger.error(
                "Couldn't get channel to table %s. Here's why: %s: %s",
                self.table.name,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
