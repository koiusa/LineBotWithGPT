from flask import Flask, request, jsonify
import os
import json
import psycopg2
import uuid
from datetime import datetime

ADMIN_SETTINGS_FILE = os.environ.get("ADMIN_SETTINGS_FILE", "/app/admin_settings.json")

def load_settings():
    if os.path.exists(ADMIN_SETTINGS_FILE):
        with open(ADMIN_SETTINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    # デフォルト値
    return {
        "openaiModel": "gpt-4.1-turbo",
        "defaultMemory": 5,
        "maxMemory": 10,
        "systemPrompt": "あなたは親しみやすいアシスタントです。"
    }

def save_settings(data):
    with open(ADMIN_SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        host=os.getenv('POSTGRES_HOST'),
        port=os.getenv('POSTGRES_PORT')
    )

app = Flask(__name__)

@app.route("/api/settings", methods=["GET", "PUT"])
def api_settings():
    if request.method == "GET":
        return jsonify(load_settings())
    elif request.method == "PUT":
        data = request.json
        save_settings(data)
        return jsonify({"ok": True})

@app.route("/api/test-connection", methods=["POST"])
def api_test_connection():
    from openai import OpenAI
    api_key = os.getenv("OPENAI_API_KEY")
    model = load_settings().get("openaiModel", "gpt-4.1-turbo")
    try:
        client = OpenAI(api_key=api_key)
        # モデルリスト取得でAPIキーの有効性を確認
        client.models.list()
        return jsonify({"ok": True, "model": model})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400

# 統計API
@app.route("/api/stats", methods=['GET'])
def get_stats():
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            # 総チャンネル数
            cur.execute("SELECT COUNT(*) FROM linebot_chatgpt_channel")
            total_channels = cur.fetchone()[0]
            
            # 総メッセージ数
            cur.execute("SELECT COUNT(*) FROM linebot_chatgpt_history")
            total_messages = cur.fetchone()[0]
            
            # アクティブチャンネル数
            cur.execute("SELECT COUNT(*) FROM linebot_chatgpt_channel WHERE setting->>'active' = 'true' OR setting IS NULL")
            active_channels = cur.fetchone()[0]
        
        conn.close()
        
        return jsonify({
            'totalChannels': total_channels,
            'totalMessages': total_messages,
            'activeChannels': active_channels
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# チャンネル管理API
@app.route("/api/channels", methods=['GET'])
def get_channels():
    try:
        conn = get_db_connection()
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
                'setting': row[5] if row[5] else {'active': True},
                'timestamp': str(row[6])
            })
        
        return jsonify({'channels': channels})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/api/channels/<channel_id>", methods=['PUT', 'DELETE'])
def manage_channel(channel_id):
    try:
        conn = get_db_connection()
        
        if request.method == 'PUT':
            data = request.json
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE linebot_chatgpt_channel 
                    SET prompt = %s, memory = %s, setting = %s, timestamp = %s
                    WHERE channelid = %s
                """, (
                    data.get('prompt'),
                    data.get('memory'),
                    json.dumps(data.get('setting', {})),
                    datetime.now(),
                    channel_id
                ))
                conn.commit()
            
            conn.close()
            return jsonify({'ok': True})
            
        elif request.method == 'DELETE':
            with conn.cursor() as cur:
                # チャンネル削除（履歴も削除）
                cur.execute("DELETE FROM linebot_chatgpt_history WHERE channelid = %s", (channel_id,))
                cur.execute("DELETE FROM linebot_chatgpt_channel WHERE channelid = %s", (channel_id,))
                conn.commit()
            
            conn.close()
            return jsonify({'ok': True})
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 会話履歴API
@app.route("/api/history/<channel_id>", methods=['GET', 'DELETE'])
def manage_history(channel_id):
    try:
        conn = get_db_connection()
        
        if request.method == 'GET':
            with conn.cursor() as cur:
                cur.execute("SELECT id, userid, message, timestamp FROM linebot_chatgpt_history WHERE channelid = %s ORDER BY timestamp ASC", (channel_id,))
                rows = cur.fetchall()
            
            history = []
            for row in rows:
                history.append({
                    'id': str(row[0]),
                    'userId': row[1],
                    'message': row[2],
                    'timestamp': str(row[3])
                })
            
            conn.close()
            return jsonify({'history': history})
            
        elif request.method == 'DELETE':
            with conn.cursor() as cur:
                cur.execute("DELETE FROM linebot_chatgpt_history WHERE channelid = %s", (channel_id,))
                conn.commit()
            
            conn.close()
            return jsonify({'ok': True})
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ステッカーコマンドAPI
@app.route("/api/stickercommands", methods=["GET"])
def get_sticker_commands():
    try:
        with open("/app/stickercommand.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)
