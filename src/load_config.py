
def load_config() -> list[str]:
    """Load and return the config"""
    try: f = open("config.txt", "r")
    except PermissionError as e:
        print(f"Could not access config.txt: {e}")
        raise
    except IOError as e:
        print(f"Could not read config.txt: {e}")
        raise
    finally:
        f.close()
    with open("config.txt", "r") as f:
        config = {}
        while True:
            line = f.readline()
            if line == "":
                break
            line = line.split(":")
            config[line[0]] = line[1].strip()
        return config
    return