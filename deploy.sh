#!/bin/bash

# Create and activate a virtual environment
python3 -m venv myenv
source myenv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install telebot
pip install python-dotenv
pip install mysql-connector-python

# Run the bot
python bot.py
