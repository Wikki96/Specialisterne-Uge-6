import mysql.connector
import requests
from load_config import load_config
from mysql_handler import MySQLHandler
import json
import polars as pl

class ConnectionHandler:
    """Handles the connections to the local and remote servers.

    Opens a connection to the remote sql servers as specified 
    in config.json and handles all interactions with it and the local
    sql server as well as interactions through the api.

    Methods:
    -
    get_orders : Returns the table orders.
    get_order_items : Returns the table order_items.
    get_customers : Returns the table customers.
    get_products : Returns the table products.
    get_brands : Returns the table brands.
    get_categories : Returns the table categories.
    get_stocks : Returns the table stocks.
    write_to_local_database : Writes the given polars dataframe to 
        the local sql table with the name given.

    Instance variables:
    -
    ip : the ip of the remote server.
    apiport : the port used for the api
    remote_uri : uri for the remote sql server
    local_uri : uri for the local sql server
    remote_sql : a MySQLHandler for the remote server
    """

    def __init__(self):
        """Handles queries to the local and remote servers
        
        Loads the configuration file config.json to make the 
        connections. The file should contain a section "LOCAL"
        that comforms to the specifications in MySQLHandler.
        Furthermore it should have a section "REMOTE" containing
        "IP", "API", and "SQL", with "API" containing "PORT" and
        "SQL" fulfilling the specifications for MySQLHandler except
        "HOST". 

        An example structure:
        -------
        "LOCAL": 
            "HOST": "localhost",
            "USER": "root",
            "PW": "pw",
            "DB": "test",
            "PORT": 3306
        "REMOTE": 
            "IP": "0.0.0.0",
            "API": {
                "PORT": 8000
            },
            "SQL": {
                "PORT": 3306,
                "USER": "user",
                "PW": "pw",
                "DB": "test"
            }
        }
        """
        config = load_config()
        remote_sql = config["REMOTE"]["SQL"]
        local_sql = config["LOCAL"]
        self.ip = config["REMOTE"]["IP"]
        remote_sql["HOST"] = self.ip
        self.apiport = config["REMOTE"]["API"]["PORT"]
        self.remote_uri = (f"mysql://{remote_sql["USER"]}:"
            f"{remote_sql["PW"]}@{self.ip}:{remote_sql["PORT"]}"
            f"/{remote_sql["DB"]}")
        self.local_uri = (f"mysql://{local_sql["USER"]}:"
            f"{local_sql["PW"]}@{local_sql["HOST"]}:"
            f"{local_sql["PORT"]}/{local_sql["DB"]}")
        #try:
        #    self.remote_sql = MySQLHandler(remote_sql)
        #except mysql.connector.InterfaceError as e:
        #    print("Could not connect to remote SQL server: " + e)
        #    raise

    def get_orders(self):
        return self.__dataframe_from_api("orders")
    
    def get_order_items(self):
        return self.__dataframe_from_api("order_items")
    
    def get_customers(self):
        return self.__dataframe_from_api("customers")

    def get_products(self):
        query = "SELECT * FROM products"
        data = self.remote_sql.execute(query)
        schema = {"product_id": pl.Int64, 
                  "product_name": str, 
                  "brand_id": pl.Int64,
                  "category_id": pl.Int64,
                  "model_year": pl.Int64,
                  "list_price": str}
        products = pl.DataFrame(data, orient="row", schema=schema)
        return products

    def get_brands(self):
        return self.__dataframe_from_sql_remote("brands")
    
    def get_categories(self):
        return self.__dataframe_from_sql_remote("categories")
    
    def get_stocks(self):
        return self.__dataframe_from_sql_remote("stocks")

    def write_to_local_database(self, 
                                table: pl.DataFrame, 
                                destination: str):
        """Load the table into the local database.
        
        Args:
        table - a polars dataframe containing the data
        destination - a string containing the name of the sql table
        """
        table.write_database(destination, 
                             self.local_uri, 
                             if_table_exists="append")
        return

    def __dataframe_from_api(self, table):
        table = requests.get(f"http://{self.ip}:{self.apiport}/{table}")
        table = pl.DataFrame(json.loads(table.json()))
        return table
    
    def __dataframe_from_sql_remote(self, table):
        query = f"SELECT * FROM {table}"
        dataframe = pl.read_database_uri(query=query, 
                                         uri=self.remote_uri)
        return dataframe
