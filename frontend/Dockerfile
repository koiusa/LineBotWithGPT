FROM node:24-alpine

WORKDIR /app

COPY . .

RUN npm install
RUN npm install keycloak-js@latest

EXPOSE 3000

# HTTPS環境変数を設定
# HTTPS有効化：以下のコメントアウトを外す
# ENV HTTPS=true
# ENV SSL_CRT_FILE=/app/certs/cert.pem
# ENV SSL_KEY_FILE=/app/certs/key.pem
# ENV PORT=3000

# HOST_CHECK無効化でDocker環境での接続問題を回避
# DANGEROUSLY_DISABLE_HOST_CHECK=trueは開発環境でのみ使用
CMD ["sh", "-c", "HOST=0.0.0.0 DANGEROUSLY_DISABLE_HOST_CHECK=true npm start"]
