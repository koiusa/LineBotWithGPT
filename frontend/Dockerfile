FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["sh", "-c", "HOST=0.0.0.0 DANGEROUSLY_DISABLE_HOST_CHECK=true npm start"]
