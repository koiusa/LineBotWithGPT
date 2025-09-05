def lambda_handler(event, context):
    authorizer = guard.authorizer()
    if not authorizer.request(event):
        return status.const.forbidden_json

    @handler.add(MessageEvent, message=(TextMessage, StickerMessage, ImageMessage))
    def message(line_event):
        eventcontext = behavior.eventcontext(
            event=line_event, linebot=line_bot_api)
        behavior.completion.reply(event_context=eventcontext)

# 例外処理としての動作
    try:
        handler.handle(authorizer.body, authorizer.signature)
    except LineBotApiError as e:
        logger.error("Got exception from LINE Messaging API: %s\n" % e.message)
        for m in e.error.details:
            logger.error("  %s: %s" % (m.property, m.message))
        return status.const.error_json
    except InvalidSignatureError:
        return status.const.error_json

    return status.const.ok_json

# --- Flaskサーバー型に変更 ---
import os
import sys
import logging
import openai
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
openai.api_key = os.getenv("OPENAI_API_KEY")

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

# 管理画面用API
@app.route("/api/stats", methods=['GET'])
def get_stats():
    try:
        import psycopg2
        conn = psycopg2.connect(
            dbname=os.getenv('POSTGRES_DB'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            host=os.getenv('POSTGRES_HOST'),
            port=os.getenv('POSTGRES_PORT')
        )
        
        with conn.cursor() as cur:
            # 総チャンネル数
            cur.execute("SELECT COUNT(*) FROM linebot_chatgpt_channel")
            total_channels = cur.fetchone()[0]
            
            # 総メッセージ数
            cur.execute("SELECT COUNT(*) FROM linebot_chatgpt_history")
            total_messages = cur.fetchone()[0]
            
            # アクティブチャンネル数
            cur.execute("SELECT COUNT(*) FROM linebot_chatgpt_channel WHERE setting->>'active' = 'true'")
            active_channels = cur.fetchone()[0]
        
        conn.close()
        
        return {
            'totalChannels': total_channels,
            'totalMessages': total_messages,
            'activeChannels': active_channels
        }
    except Exception as e:
        logger.error(f"Stats API error: {e}")
        return {'error': 'データの取得に失敗しました'}, 500

@app.route("/api/channels", methods=['GET'])
def get_channels():
    try:
        import psycopg2
        conn = psycopg2.connect(
            dbname=os.getenv('POSTGRES_DB'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            host=os.getenv('POSTGRES_HOST'),
            port=os.getenv('POSTGRES_PORT')
        )
        
        with conn.cursor() as cur:
            cur.execute("SELECT id, channelid, type, prompt, memory, setting, timestamp FROM linebot_chatgpt_channel ORDER BY timestamp DESC")
            rows = cur.fetchall()
        
        conn.close()
        
        channels = []
        for row in rows:
            channels.append({
                'id': str(row[0]),
                'channelId': row[1],
                'type': row[2],
                'prompt': row[3],
                'memory': row[4],
                'setting': row[5] or {},
                'timestamp': str(row[6])
            })
        
        return {'channels': channels}
    except Exception as e:
        logger.error(f"Channels API error: {e}")
        return {'error': 'データの取得に失敗しました'}, 500

@app.route("/api/history/<channel_id>", methods=['GET'])
def get_history(channel_id):
    try:
        import psycopg2
        conn = psycopg2.connect(
            dbname=os.getenv('POSTGRES_DB'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            host=os.getenv('POSTGRES_HOST'),
            port=os.getenv('POSTGRES_PORT')
        )
        
        with conn.cursor() as cur:
            cur.execute("SELECT id, userid, message, timestamp FROM linebot_chatgpt_history WHERE channelid = %s ORDER BY timestamp ASC", (channel_id,))
            rows = cur.fetchall()
        
        conn.close()
        
        history = []
        for row in rows:
            history.append({
                'id': str(row[0]),
                'userId': row[1],
                'message': row[2],
                'timestamp': str(row[3])
            })
        
        return {'history': history}
    except Exception as e:
        logger.error(f"History API error: {e}")
        return {'error': 'データの取得に失敗しました'}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
