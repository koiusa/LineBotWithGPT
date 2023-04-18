#!/usr/bin/env bash

SCRIPT_DIR=$(cd $(dirname $0); pwd)
TARGET_DIR=python

sudo rm -r ${TARGET_DIR}
mkdir ${TARGET_DIR}
pip install openai -t ${TARGET_DIR}
pip install line-bot-sdk -t ${TARGET_DIR}
pip install logging -t ${TARGET_DIR}
pip install langchain -t ${TARGET_DIR}
zip -r linebot-openai.zip ${TARGET_DIR}

sudo rm -r ${TARGET_DIR}
mkdir ${TARGET_DIR}
pip install pandas -t ${TARGET_DIR}
zip -r linebot-database.zip ${TARGET_DIR}