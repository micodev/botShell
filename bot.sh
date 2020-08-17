#!/bin/bash
sysname=$(uname)
cat sopro.txt
if [ $sysname == "Linux" ]
then
  bash lib.sh
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
  echo '{"db":"sqlite:///database.db","api_hash": "'$api_hash'","api_id": '$api_id',"bot_id": 0,"flood":true,"isbot": true,"plugins":['$plugins'],"sudo_members": ['$id']}' > $file
  py=python3.8
  $py main.py
fi