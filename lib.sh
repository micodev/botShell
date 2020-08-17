
hn=$(hostname)
if [ $hn == "localhost" ]
then
    pkg upgrade
    pkg update
    pkg install python
    py=python
    pkg install redis
    pi=$py" -m pip"
    $pi install --upgrade pip
    pkg install -y libxml2 libxslt
    pkg install -y libjpeg-turbo
    pkg install -y ffmpeg
    pkg install -y clang
    pkg install -y qpdf
    pkg install -y zlib
    redis-server --daemonize yes
    $pi install -r requirements.txt

else
    sudo apt update -y
    sudo apt install -y software-properties-common
    echo -ne '\n' | sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt install python3.8 -y
    sudo apt install python3-pip -y
    python3.8 -m pip install --upgrade pip
    sudo apt install ffmpeg -y
    sudo apt install redis-server -y
    sudo apt install clang -y
    sudo service redis-server restart
    py=python3.8
    pi=$py" -m pip"
    $pi install --upgrade pip
    $pi install setuptools
    $pi install -r requirements.txt
    $pi install tensorflow
fi