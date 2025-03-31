import mysql.connector
import load_config

class MySQLConnector:
    """A wrapper for the mysql connector creating a cursor and 
    handling queries with one method.
    Public methods:
    execute
    """
    def __init__(self, database=""):
        config = load_config()
        self.con = mysql.connector.connect(
            host=config["host"], user=config["user"], 
            password=config["pw"], database=database)
        self.cursor = self.con.cursor()

    def execute(self, query):
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        self.con.commit()
        return data