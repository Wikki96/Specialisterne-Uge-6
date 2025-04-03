from mysql_handler import MySQLHandler
from load_config import load_config
import os
import sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

if __name__ == "__main__":
    config = load_config()
    con = MySQLHandler(config["LOCAL"])
    with open(os.path.join("MySQL", "bike_store.sql")) as f:
        queries = f.read()
    queries = queries.split(";")
    for query in queries:
        if query.strip() != "":
            query = query.replace("bike_store", config["LOCAL"]["DB"])
            con.execute(query)