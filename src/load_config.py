import json

def load_config() -> list[str]:
    """Load and return the config"""
    try: f = open("config.json", "r")
    except PermissionError as e:
        print(f"Could not access config.json: {e}")
        raise
    except IOError as e:
        print(f"Could not read config.json: {e}")
        raise
    else:
        f.close()
    with open("config.json", "r") as f:
        try: config = json.load(f)
        except json.decoder.JSONDecodeError as e:
            print(f"Make sure that config.json has correct json: {e}")
            raise
        return config
    return