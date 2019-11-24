import yaml

config = None


def get_config():
    global config

    if config is None:
        with open('config.yaml') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)

    return config
