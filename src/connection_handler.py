import mysql.connector
import requests
from load_config import load_config
from mysql_handler import MySQLHandler
import json
import polars as pl

class ConnectionHandler:
    """Connect to the remote server, it's MySQL server and your 
    local MySQL server.
    """

    def __init__(self):
        config = load_config()
        remote_sql = config["REMOTE"]["SQL"]
        local_sql = config["LOCAL"]
        self.ip = config["REMOTE"]["IP"]
        self.apiport = config["REMOTE"]["API"]["PORT"]
        self.remote_uri = f"""mysql://{remote_sql["USER"]}:{remote_sql["PW"]}
            @{self.ip}:{remote_sql["PORT"]}/{remote_sql["DB"]}"""
        self.local_uri = f"""mysql://{local_sql["USER"]}:{local_sql["PW"]}
            @{local_sql["HOST"]}:{local_sql["PORT"]}/{local_sql["DB"]}"""
        try:
            self.remote_sql = MySQLHandler(remote_sql)
        except mysql.connector.InterfaceError as e:
            print("Could not connect to remote SQL server: " + e)
            raise
        try:
            self.local_sql = MySQLHandler(config["LOCAL"])
        except mysql.connector.InterfaceError as e:
            print("Could not connect to local SQL server: " + e)
            raise

    def execute(self, query):
        """Execute the query on the local sql server"""
        data = self.local_sql.execute(query)
        return data

    def get_orders(self):
        return self.__dataframe_from_api("orders")
    
    def get_order_items(self):
        return self.__dataframe_from_api("order_items")
    
    def get_customers(self):
        return self.__dataframe_from_api("customers")

    def get_products(self):
        return self.__dataframe_from_sql_remote("products")
    
    def get_brands(self):
        return self.__dataframe_from_sql_remote("brands")
    
    def get_categories(self):
        return self.__dataframe_from_sql_remote("categories")
    
    def get_stocks(self):
        return self.__dataframe_from_sql_remote("stocks")
    
    def __dataframe_from_api(self, table):
        table = requests.get(f"http://{self.ip}:{self.port}/{table}")
        table = pl.DataFrame(json.loads(table.json))
        return table
    
    def __dataframe_from_sql_remote(self, table):
        query = f"SELECT * FROM {table}"
        return pl.read_database_uri(query=query, uri=self.remote_uri)