FROM python:3.12-slim

WORKDIR /app

COPY ./app /app

RUN apt-get update && apt-get install -y netcat-openbsd
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["sh", "/app/entrypoint.sh"]
