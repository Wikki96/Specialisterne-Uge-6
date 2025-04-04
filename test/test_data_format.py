import mysql.connector

con = mysql.connector.connect(host="10.0.125.153", user="curseist", password="curseword", database="productdb")
cursor = con.cursor()
cursor.execute("SELECT * FROM products")
data = cursor.fetchmany(10)
print(data)

