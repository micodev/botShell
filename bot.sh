#!/bin/bash
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update -y
sudo apt install python3.6 -y
sudo apt install python3.6-dev -y
sudo apt install python3-pip -y
sudo pip3 install telethon
sudo python3.6 -m pip install -r requirements.txt
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
plugins=${plugins[@]%?}

file=config.json
echo '{"api_hash": "'$api_hash'","api_id": '$api_id',"bot_id": 0,"isbot": true,"plugins":['$plugins'],"sudo_members": ['$id']}' > $file
python3.6 main.py
