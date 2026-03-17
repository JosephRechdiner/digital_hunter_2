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
def get_quality_targets(cnx: mysql.connector.MySQLConnection):
    query = """
            SELECT entity_id, target_name, priority_level, movement_distance_km
            FROM targets
            WHERE (priority_level = 1 OR priority_level = 2) AND movement_distance_km > 5;
            """
    with cnx.cursor(dictionary=True) as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    return result

def get_new_targets(cnx:  mysql.connector.MySQLConnection):
    query = """
            SELECT entity_id, COUNT(*) AS count
            FROM intel_signals
            WHERE entity_id LIKE '%UNKNOWN%'
            GROUP BY entity_id
            ORDER BY count DESC
            LIMIT 3;
            """
    with cnx.cursor(dictionary=True) as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    return result

def get_target_route(entity_id: str, cnx: mysql.connector.MySQLConnection):
    query = """
    SELECT timestamp, reported_lat, reported_lon
    FROM intel_signals
    WHERE entity_id = %s
    ORDER BY timestamp desc;
            """
    with cnx.cursor(dictionary=True) as cursor:
        cursor.execute(query, (entity_id,))
        result = cursor.fetchall()
    return result

# print(get_target_route('TGT-003', cnx))

import matplotlib.pyplot as plt
import numpy as np

def extract_lat_and_lon(coords: dict):
    lat = [coord['reported_lat'] for coord in coords]
    lon = [coord['reported_lon'] for coord in coords]
    return lat, lon

coords = get_target_route('TGT-007', cnx)
# print(coords)
lat, lon = extract_lat_and_lon(coords)

xpoints = np.array(lon)
ypoints = np.array(lat)
plt.plot(xpoints, ypoints)
plt.scatter(lon[0], lat[0], color='g')
plt.scatter(lon[-1], lat[-1], color='r')

plt.show()

# print(lat)
# print(lon)
