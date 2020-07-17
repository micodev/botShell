#!/bin/bash/
pkill -f main.py
mv config.json .config.json
git reset --hard
git pull
mv .config.json config.json
hn=$(hostname)
python3 -m install pip -r requirements.txt
python3 main.py