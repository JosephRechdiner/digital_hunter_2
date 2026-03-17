import mysql.connector

config = {
  "host": "localhost",
  "port": 3306,
  "user": "root",
  "password": "root",
  "database": "digital_hunter"
}
cnx = mysql.connector.connect(
    host="localhost",
    port=3306,
    user='root',
    password='root',
    database="digital_hunter"
)

# with cnx.cursor(dictionary=True) as cursor:
#     query = 
