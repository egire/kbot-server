#!/bin/bash

cd ~
echo "Updating web-ui..."
cd kbot/kbot-web/
git pull

cd ~
echo "Updating server..."
cd kbot/kbot-server/
git pull
