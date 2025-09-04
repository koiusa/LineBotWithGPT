
[![GitHub commit activity](https://img.shields.io/github/commit-activity/m/koiusa/LineBotWithGPT)](https://github.com/koiusa/LineBotWithGPT/graphs/commit-activity)
[![GitHub issues](https://img.shields.io/github/issues/koiusa/LineBotWithGPT)](https://github.com/koiusa/LineBotWithGPT/issues)
[![GitHub license](https://img.shields.io/github/license/koiusa/LineBotWithGPT)](https://github.com/koiusa/LineBotWithGPT/blob/main/LICENSE)

# LineBotWithGPT

LINE公式BotとOpenAI GPTを連携し、会話履歴をPostgreSQLで管理するDocker対応チャットボットです。

---

## 主な機能
- LINE公式Botとして動作（Messaging API対応）
- OpenAI GPTと連携し自然な会話が可能
- 会話履歴をPostgreSQLで永続管理
- 複数チャンネル・複数ユーザー対応
- プロンプト（AIの役割）設定・削除
- 記憶数（履歴の深さ）変更
- チャンネルごとの履歴削除・管理
- Docker Composeによる簡単な起動・運用

## 使い方（LINE Bot操作例）
- 通常のトークでAIと会話
- 「AIの役割を設定」→ 任意のメッセージでプロンプト設定
- 「記憶数を設定」→ 数字を送信（最大10）
- 「履歴削除」→ 「y」と送信で履歴クリア
- 複数チャンネルの管理・切替も可能

## コマンド例（管理者向け）
```
docker compose build
docker compose up
```
LINE DevelopersのWebhook URLに `http://<サーバーIP>:8000/callback` を設定

## データベース構造（PostgreSQL）
- linebot_chatgpt_channel: チャンネル情報・プロンプト・記憶数など
- linebot_chatgpt_history: 会話履歴（userId, message, timestamp...）

## カスタマイズ例
- OpenAIのモデルを変更したい場合：lambda_function.pyの `model="gpt-3.5-turbo"` を編集
- 履歴の保存件数や内容を拡張したい場合：histoly_postgres.pyを編集
- Webhookエンドポイントやポート番号はdocker-compose.yml/entrypoint.shで調整可能

## 開発・デバッグTips
- `docker compose logs -f` でリアルタイムログ確認
- DBの中身確認は `docker exec -it linebot-gpt-db psql -U <user> <db>`
- .envの値を変更したら再ビルド推奨

