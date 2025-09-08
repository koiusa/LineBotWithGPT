
[![GitHub commit activity](https://img.shields.io/github/commit-activity/m/koiusa/LineBotWithGPT)](https://github.com/koiusa/LineBotWithGPT/graphs/commit-activity)
[![GitHub issues](https://img.shields.io/github/issues/koiusa/LineBotWithGPT)](https://github.com/koiusa/LineBotWithGPT/issues)
[![GitHub license](https://img.shields.io/github/license/koiusa/LineBotWithGPT)](https://github.com/koiusa/LineBotWithGPT/blob/main/LICENSE)

# LineBotWithGPT

LINE公式BotとOpenAI GPTを連携し、会話履歴をPostgreSQLで管理するDocker対応チャットボットです。  
**React製Web管理画面付き**で、ブラウザから簡単に設定・履歴管理が可能です。

---

## 主な機能
- LINE公式Botとして動作（Messaging API対応）
- OpenAI GPTと連携し自然な会話が可能
- 会話履歴をPostgreSQLで永続管理
- 複数チャンネル・複数ユーザー対応
- プロンプト（AIの役割）設定・削除
- 記憶数（履歴の深さ）変更
- チャンネルごとの履歴削除・管理
- **React製Web管理画面** 📊
  - ダッシュボード（統計表示）
  - チャンネル管理（設定変更・削除）
  - 会話履歴表示・エクスポート
  - システム設定（OpenAIモデル変更など）
- Docker Composeによる簡単な起動・運用

## 使い方（LINE Bot操作例）
- 通常のトークでAIと会話
- 「AIの役割を設定」→ 任意のメッセージでプロンプト設定
- 「記憶数を設定」→ 数字を送信（最大10）
- 「履歴削除」→ 「y」と送信で履歴クリア
- 複数チャンネルの管理・切替も可能

## セットアップ・起動方法

### 1. 環境変数設定
```bash
cp .env.example .env
# .envファイルを編集してAPIキーなどを設定
```

### 2. Docker Compose起動
```bash
docker compose build
docker compose up -d
```

### 3. アクセス
- **LINE Bot Webhook**: `http://<サーバーIP>:18000/callback`
- **Web管理画面**: `http://<サーバーIP>:13000`
- **PostgreSQL**: `localhost:65432`

## 構成・ポート番号
| サービス | ポート | 説明 |
|---------|--------|------|
| linebot-gpt | 18000 | Flask API サーバー (LINE Webhook) |
| linebot-gpt-frontend | 13000 | React Web管理画面 |
| linebot-gpt-db | 65432 | PostgreSQL データベース |

## データベース構造（PostgreSQL）
- **linebot_chatgpt_channel**: チャンネル情報・プロンプト・記憶数など
- **linebot_chatgpt_history**: 会話履歴（userId, message, timestamp...）

## カスタマイズ例
- OpenAIのモデルを変更したい場合：`app/const.py`の`OPENAI_MODEL`を編集
- 履歴の保存件数や内容を拡張したい場合：`app/database/histoly_postgres.py`を編集
- Webhookエンドポイントやポート番号は`docker-compose.yml`で調整可能
- React管理画面のデザインやAPIは`frontend/`ディレクトリ内で変更

## 開発・デバッグTips
- `docker compose logs -f linebot-gpt` でバックエンドログ確認
- `docker compose logs -f linebot-gpt-frontend` でフロントエンドログ確認  
- DBの中身確認: `docker exec -it linebot-gpt-db psql -U postgres linebot`
- .envの値を変更したら再ビルド推奨
- React開発時は`frontend/`ディレクトリで`npm start`での開発も可能

## アーキテクチャ
```
[LINE Messaging API] 
    ↓ Webhook
[Flask API Server] ←→ [PostgreSQL]
    ↓ REST API
[React Web Dashboard]
```

