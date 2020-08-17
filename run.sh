#!/bin/bash/
pkill -f main.py
mv config.json .config.json
git reset --hard
git pull
mv .config.json config.json
py=python3.8
$py -m pip install --upgrade pip
$py -m pip install --upgrade setuptools
$py -m pip install -r requirements.txt
bash lib.sh
$py -m pip install tensorflow
$py main.py