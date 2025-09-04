#!/bin/sh
chmod +x ./wait-for-it.sh
./wait-for-it.sh linebot-gpt-db 5432 python create_channel_table_postgres.py && python create_history_table_postgres.py
gunicorn --bind 0.0.0.0:8000 main:app
