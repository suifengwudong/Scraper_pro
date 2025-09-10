from json import load, dump

class Config():
    '''Class to manage configuration settings for the scraper.'''
    config_path = "res/config.json"
    configs = {
        "BROWSER_LIST": [],
        "BROWSER_PATH_DICT": {},
        "DEFAULT_BROWSER": ""
    }

    @classmethod
    def load(cls):
        '''Load configuration settings from a JSON file.'''
        with open(cls.config_path) as f:
            cls.configs = load(f)

    @classmethod
    def save(cls):
        '''Save the current configuration settings to a JSON file.'''
        with open(cls.config_path, "w") as f:
            dump(cls.configs, f, indent=4)

Config.load()

if __name__ == "__main__":
    Config.save()