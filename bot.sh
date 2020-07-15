#!/bin/bash
sysname=$(uname)
cat sopro.txt
if [ $sysname == "Linux" ]
then
  hn=$(hostname)
  if [ $hn == "localhost" ]
  then
    pkg update
    pkg install python
    pip3 install --upgrade pip
    pkg install libxml2 libxslt
    pkg install libjpeg-turbo
    pkg update
    pip3 install telethon
    pip3 install beautifulsoup4
    pip3 install SQLAlchemy
    pip3 install -r requirements.txt
  else
    sudo apt install software-properties-common -y
    sudo add-apt-repository ppa:deadsnakes/ppa -y
    sudo apt update -y
    sudo apt install python3.6 -y
    sudo apt install python3.6-dev -y
    sudo apt install python3-pip -y
    sudo pip3 install telethon
    sudo pip3 install beautifulsoup4
    pip3 install SQLAlchemy
    sudo python3.6 -m pip install -r requirements.txt
  fi
  echo -n "Insert api hash (https://my.telegram.org) : "
  read api_hash
  echo -n "Insert api id : "
  read api_id
  echo -n "Insert the id of main user (you id) : "
  read id

  search_dir=$(cd $(dirname $0); pwd)
  array=("item 1" "item 2" "item 3")
  for file in $search_dir/plugins/*; do
    f=$(echo "${file##*/}");
    filename=$(echo $f| cut  -d'.' -f 1); #file has extension, it return only filename
    plugins+="\""$filename"\","
  done
  plugins=${plugins[@]}

  file=config.json
  echo '{"db":"sqlite:///database.db","api_hash": "'$api_hash'","api_id": '$api_id',"bot_id": 0,"isbot": true,"plugins":['$plugins'],"sudo_members": ['$id']}' > $file
  if [ $hn == "localhost" ]
  then
    python3 main.py
  else
    python3.6 main.py
  fi
fi