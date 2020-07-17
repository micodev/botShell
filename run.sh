#!/bin/bash/
pkill -f main.py
hn=$(hostname)
python3 -m install -r requirements.txt
python3 main.py