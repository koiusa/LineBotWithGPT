FROM node:24-alpine

WORKDIR /app

COPY . .

RUN npm install
RUN npm install keycloak-js@latest

EXPOSE 3000

# HTTPS環境変数を設定
# ENV HTTPS=true
# ENV SSL_CRT_FILE=/app/certs/cert.pem
# ENV SSL_KEY_FILE=/app/certs/key.pem

CMD ["sh", "-c", "HOST=0.0.0.0 DANGEROUSLY_DISABLE_HOST_CHECK=true npm start"]
