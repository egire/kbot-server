#!/bin/bash

cd /home/pi/

./update-kbot.sh

echo "Running server..."
cd ./kbot/kbot-server
python3 kbotserv.py 8000 > /dev/null 2> /dev/null &
