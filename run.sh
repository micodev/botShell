#!/bin/bash/
pkill -f main.py
hn=$(hostname)
git pull
python3 -m install -r requirements.txt
python3 main.py