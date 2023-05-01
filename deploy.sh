#!/bin/bash

# Install dependencies
pip install --upgrade pip
pip install telebot
pip install python-dotenv
pip install mysql-connector-python

# Create and activate a virtual environment
python3 -m venv myenv
source myenv/bin/activate

# Environment variables
export BOTTOKEN="6010256354:AAHChAnylibLfKnJuxvM6wy--nRxEGIq4bw"
export SUCCESS_MESSAGE="👍 Welcome To Mushee World"

# Run the bot
python bot.py
