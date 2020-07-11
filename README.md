# BotShell

[![N|Solid](https://raw.githubusercontent.com/micodev/botShell/master/images/cover.png?token=AEF6B4UU3ONGVXAPOKR2VDS7CMQMW)](https://t.me/soProTeam)

> 👏 Thanks in advance for any support you make for this project

BotShell is a pluggable telegram bot based on [telethon](https://github.com/LonamiWebs/Telethon).

- speed & fast.
- pluggable plugins (no need to restart).
- asynchronous bot.

## Installation

BotShell requires [Python3.6+](https://www.python.org/about/gettingstarted/) to run.

First thing first install the dependencies.

```sh
$ sudo apt install software-properties-common
$ sudo add-apt-repository ppa:deadsnakes/ppa
$ sudo apt update
$ sudo apt install python3.6
$ sudo apt install libcurl4-gnutls-dev
$ git clone https://github.com/micodev/botShell.git
$ cd botShell
$ pip3 install -r requirements.txt  # or use  pip depends on your vm.
```

Second thing to do is edit ```Config.json``` file.

```json
    {
        "api_hash": "Your_api_hash_here",
        "api_id":  Your_api_id,
        "bot_id": 0,
        "sudo_members": [
            your_id_or_any_sudo 
        ]
    }
```

After that use this command to make magic happened...

```sh
$ python3 main.py
```

At this point the terminal will ask you for phonenumber or [api token](https://t.me/botfather) to sign in.

## Plugins

BotShell is currently extended with the following plugins,feel free to make some and pull request it or send to developers of this source to insert it in.

| Plugin | README |
| ------ | ------ |
| cronJob | Simple implementation of cron job.|
| getBook | Get book from [libgen](http://libgen.li/).|
| help | By sending `/help` you can get a message with all command available or its usage.|
| img2pdf | You can convert **20** of images to pdf.|
| marquee | Text that send by bot (if using cli) or from user to bot will be marquee.|
| ocr | Get text from image (arabic supported the english going to be `rtl`).|
| plugins | Show, enable,disable plugins exist in [plugins](https://github.com/micodev/botShell/tree/master/plugins) folder.|
| squareSnake | using this plugin bot can make square message using emoji with black white square emoji.|
|tagAll| Tag all users exist in group.|
|typing| Make message like someone typing it at realtime.|
|weather| Get weather from [OpenWeather](https://openweathermap.org)|



## Development

Want to contribute? Great!
Contract with us from here : [Ibrahim Ayad](https://t.me/anime19).

**Note:** this bot is still being under development so keep up with updates.

License
----

MIT (Personal use only).


**Totally free software..**
