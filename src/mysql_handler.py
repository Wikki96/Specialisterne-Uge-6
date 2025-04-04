import mysql.connector

class MySQLHandler:
    """A wrapper for the mysql connector creating a cursor and 
    handling queries with one method. If the given database doesn't 
    exist, it will connect with no database selected.
    Public methods:
    execute
    """
    
    def __init__(self, connection_info: dict):
        try: 
            self.con = mysql.connector.connect(
                host=connection_info["HOST"], 
                user=connection_info["USER"], 
                password=connection_info["PW"], 
                database=connection_info["DB"], 
                port=connection_info["PORT"])
        # If the database can't be found 
        # a ProgrammingError will be raised
        except mysql.connector.ProgrammingError as e:
            self.con = mysql.connector.connect(
                host=connection_info["HOST"], 
                user=connection_info["USER"], 
                password=connection_info["PW"], 
                database="", 
                port=connection_info["PORT"])
        self.cursor = self.con.cursor()

    def execute(self, query):
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        self.con.commit()
        return data