sudo apt install software-properties-common
udo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.6
sudo apt install libcurl4-gnutls-dev
pip3 install -r requirements.txt
echo -n "Insert api hash (https://my.telegram.org) : "
read api_hash
echo -n "Insert api id : "
read api_id
echo -n "Insert the id of main user (you id) : "
read id


file=config.json
echo 
echo '{\n"api_hash": "'$api_hash'",\n"api_id": '$api_id',"bot_id": 0,"isbot": true,"plugins": ["plugins","help"],"sudo_members": ['$id']}' > $file
python3 main.py
