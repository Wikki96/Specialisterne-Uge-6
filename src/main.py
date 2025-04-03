import requests
from mysql_handler import MySQLHandler
import json
import polars as pl
from load_config import load_config

if __name__ == "__main__":
    #config = load_config()
    #remote_sql = config["REMOTE"]["SQL"]
    #ip = config["REMOTE"]["IP"]
    #port = config["REMOTE"]["API"]["PORT"]
    #remote_sql["HOST"] = ip
    #
    #orders = requests.get(f"http://{ip}:{port}/orders")
    #order_items = requests.get(f"http://{ip}:{port}/order_items")
    #customers = requests.get(f"http://{ip}:{port}/customers")
    #df = pl.DataFrame(json.loads(orders.json()))
    #con = ConnectionHandler(remote_sql)
    #brands = con.execute("SELECT * FROM brands")
    
    