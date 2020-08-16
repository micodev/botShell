import demjson
import redis
from os.path import dirname, join, realpath, isfile
import aiohttp
from requests.sessions import session
from aiohttp import connector


class utilities:
    red = redis.Redis(host="localhost", port=6379, db=1)
    WD = dirname(realpath(__file__))
    flood = {}
    client = None
    devs = []
    config = {}
    user_steps = {}
    plugins = []
    public_plugins = []
    crons = []

    @classmethod
    def check_sudo(cls, chat_id):
        if chat_id in utilities.config["sudo_members"]:
            return True
        if chat_id in utilities.devs:
            return True
        return False

    @classmethod
    def markdown_escape(cls, text):
        text = text.replace("_", "\\_")
        text = text.replace("[", "\\{")
        text = text.replace("*", "\\*")
        text = text.replace("`", "\\`")
        return text

    @classmethod
    def prRed(cls, skk):
        print("\033[91m{}\033[00m".format(skk))

    @classmethod
    def prGreen(cls, skk):
        print("\033[92m{}\033[00m".format(skk))

    @classmethod
    def prYellow(cls, skk):
        print("\033[93m{}\033[00m".format(skk))

    @classmethod
    def prLightPurple(cls, skk):
        print("\033[94m{}\033[00m".format(skk))

    @classmethod
    def prPurple(cls, skk):
        print("\033[33m{}\033[00m".format(skk))

    @classmethod
    def prCyan(cls, skk):
        print("\033[96m{}\033[00m".format(skk))

    @classmethod
    def prLightGray(cls, skk):
        print("\033[97m{}\033[00m".format(skk))

    @classmethod
    def prBlack(cls, skk):
        print("\033[98m{}\033[00m".format(skk))

    @classmethod
    def is_group(cls, message):
        if not message.sender_id == message.chat_id:
            return True
        return False

    @classmethod
    async def get(cls, url, params=None, headers=None):
        connector = aiohttp.TCPConnector(verify_ssl=False)
        session = aiohttp.ClientSession(connector=connector)
        resp = await session.get(url, params=params, headers=headers)
        await session.close()
        await connector.close()
        return await resp.text()

    @classmethod
    def save_config(cls):
        file = open(join(cls.WD, "config.json"), "w")
        file.write(demjson.encode(cls.config))
        file.close()

    @classmethod
    def get_config(cls):

        file = open(join(cls.WD, "config.json"), "r")
        cls.config = demjson.decode(file.read())
        file.close()
        return cls.config

    @classmethod
    def load_plugins(cls):

        cls.plugins = []
        cls.public_plugins = []
        error = []
        for pluginName in cls.config["plugins"]:
            plugin_dir = join(cls.WD, "plugins", pluginName + ".py")
            if isfile(plugin_dir):
                values = {}
                try:
                    with open(plugin_dir, encoding="utf-8") as f:
                        code = compile(f.read(), plugin_dir, "exec")
                        exec(code, values)
                        f.close()
                    print("plugin " + str(pluginName))
                    plugin = values["plugin"]
                    if not plugin["sudo"] and "usage" in plugin:
                        cls.public_plugins.append(plugin)
                    cls.plugins.append(plugin)
                except Exception as e:
                    utilities.prRed(
                        "There is error while install "
                        + pluginName
                        + " check developers for more info."
                        + "\n"
                        + str(e)
                    )
                    error.append(pluginName)
            else:
                cls.config["plugins"].remove(pluginName)
                cls.prRed(
                    pluginName + ".py : not found and will be removed from config.json"
                )
        for er in error:
            cls.config["plugins"].remove(er)
        cls.save_config()

    @classmethod
    def load_plugin(cls, name):
        plugin_dir = join(cls.WD, "plugins", name + ".py")
        print("plugin " + str(name))
        values = {}
        with open(plugin_dir, encoding="utf-8") as f:
            code = compile(f.read(), plugin_dir, "exec")
            exec(code, values)
            f.close()
        plugin = values["plugin"]
        return plugin
