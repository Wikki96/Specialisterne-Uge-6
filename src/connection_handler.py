import mysql.connector

class ConnectionHandler:
    """A wrapper for the mysql connector creating a cursor and 
    handling queries with one method.
    Public methods:
    execute
    """
    def __init__(self, connection_info: dict):
        self.con = mysql.connector.connect(
            host=connection_info["HOST"], user=connection_info["USER"], 
            password=connection_info["PW"], database=connection_info["DB"])
        self.cursor = self.con.cursor()

    def execute(self, query):
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        self.con.commit()
        return data