import os
import sys
import logging
import status
import behavior
import guard
from flask import Flask, request, abort
from guard import verify_line_signature
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, ImageMessage, StickerMessage
from linebot.exceptions import LineBotApiError, InvalidSignatureError

app = Flask(__name__)

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)

if channel_secret is None:
    logger.error('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    logger.error('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

@handler.add(MessageEvent, message=(TextMessage, StickerMessage, ImageMessage))
def message(line_event):
    eventcontext = behavior.eventcontext(
        event=line_event, linebot=line_bot_api)
    behavior.completion.reply(event_context=eventcontext)

@app.route("/callback", methods=['POST'])
def callback():
    # 署名検証
    if not verify_line_signature(request):
        abort(400)
    signature = request.headers.get('X-Line-Signature')
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except LineBotApiError as e:
        logger.error("Got exception from LINE Messaging API: %s\n" % e.message)
        for m in e.error.details:
            logger.error("  %s: %s" % (m.property, m.message))
        abort(400)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
