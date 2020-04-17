#!/bin/bash

#echo "Updating web..."
#/home/pi/update-kbot.sh

echo "Running web..."
killall python3

cd /home/pi/kbot/kbot-server/
python3 kbotserv.py 8000
