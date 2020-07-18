#!/bin/bash/
pkill -f main.py
mv config.json .config.json
git reset --hard
git pull
mv .config.json config.json
sudo update-alternatives  --set python /usr/bin/python3.6
sudo update-alternatives --config python
python -m pip install -r requirements.txt
python main.py