from flask import Flask, request, jsonify
import os
import json

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)
