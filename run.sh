#!/bin/bash/
pkill -f main.py
hn=$(hostname)
pip3 install requests-futures
if [ $hn == "localhost" ]
then
    python3 main.py
else
    screen python3 main.py
fi