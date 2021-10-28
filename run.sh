#!/bin/bash

GIT_SSH_COMMAND='ssh -i ~/NewsFeed_Telegram_Bot/ssh/id_rsa'
screen -dmS TelegramBot  ./env/bin/python3 main.py
