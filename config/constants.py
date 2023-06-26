import codecs
import configparser


class Settings:
    def __init__(self, config_path="config.ini"):
        self.config_path = config_path
        self.config = configparser.ConfigParser()
        self._load_constants()

    def _load_constants(self):
        self.config = self.load_config()
        self.DEFAULT = self.config["DEFAULT"]
        self.DEBUG = self.config.getboolean("DEFAULT", "debug")
        self.STATIC_PATH = self.DEFAULT.get("static_path")
        self.CLIENT = self.DEFAULT.get("client")

    def build_config(self) -> None:
        self.config["DEFAULT"] = {
            "debug": True,
        }
        with open(self.config_path, "w", encoding="utf-8") as f:
            print("- Creating new config")
            self.config.write(f)

    def load_config(self):
        try:
            self.config.read_file(codecs.open(self.config_path, "r", "utf-8"))
        except FileNotFoundError:
            print("- Config not found")
            self.build_config()
            self.config.read_file(codecs.open(self.config_path, "r", "utf-8"))
        return self.config

    def reload(self):
        self._load_constants()
