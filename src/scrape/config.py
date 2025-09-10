from json import load

with open("res/config.json") as config_file:
    config = load(config_file)

BROWSER_LIST = config["BROWSER_LIST"]
BROWSER_PATH_DICT = config["BROWSER_PATH_DICT"]
DEFAULT_BROWSER = config["DEFAULT_BROWSER"]