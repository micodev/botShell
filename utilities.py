import demjson
from os.path import dirname, join, realpath
import aiohttp
from requests.sessions import session
from aiohttp import connector


class utilities:
    WD = dirname(realpath(__file__))
    client = None
    config = {}
    user_steps = {}
    plugins = []
    public_plugins = []
    crons = []

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
        try:
            cls.plugins = []
            cls.public_plugins = []
            for pluginName in cls.config["plugins"]:
                plugin_dir = join(cls.WD, "plugins", pluginName + ".py")
                print("plugin " + str(pluginName))
                values = {}
                with open(plugin_dir, encoding="utf-8") as f:
                    code = compile(f.read(), plugin_dir, "exec")
                    exec(code, values)
                    f.close()
                plugin = values["plugin"]
                if not plugin["sudo"] and "usage" in plugin:
                    cls.public_plugins.append(plugin)
                cls.plugins.append(plugin)
        except Exception as e:
            print("Error : " + str(e))

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
