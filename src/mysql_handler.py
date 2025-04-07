import mysql.connector

class MySQLHandler:
    """A wrapper for the mysql connector. 
    
    Creates a cursor and handles queries with one method. 
    If the given database doesn't exist, 
    it will connect with no database selected.

    Public methods:
        execute

    Instance variables:
        con - a mysql-connector connection object.
        cursor - a mysql-connector cursor on the connection.
    """
    
    def __init__(self, connection_info: dict):
        """Connect using connection_info.
        
        connection_info should contain the keys:
            HOST
            USER
            PW - password for USER
            DB - a database name
            PORT
        """
        try: 
            self.con = mysql.connector.connect(
                host=connection_info["HOST"], 
                user=connection_info["USER"], 
                password=connection_info["PW"], 
                database=connection_info["DB"], 
                port=connection_info["PORT"])
        # If the database can't be found 
        # a ProgrammingError will be raised by mysql.connector
        except mysql.connector.ProgrammingError as e:
            self.con = mysql.connector.connect(
                host=connection_info["HOST"], 
                user=connection_info["USER"], 
                password=connection_info["PW"], 
                database="", 
                port=connection_info["PORT"])
        self.cursor = self.con.cursor()

    def execute(self, query):
        """Execute query on the database and fetch data if any"""
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        self.con.commit()
        return data