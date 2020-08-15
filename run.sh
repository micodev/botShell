#!/bin/bash/
pkill -f main.py
pkill -f run.sh
mv config.json .config.json
git reset --hard
git pull
mv .config.json config.json
sudo update-alternatives  --set python /usr/bin/python3.6
sudo update-alternatives --config python
python -m pip install --upgrade pip
python -m pip install --upgrade setuptools
python -m pip install -r requirements.txt
bash lib.sh
python -m pip install tensorflow
python main.py