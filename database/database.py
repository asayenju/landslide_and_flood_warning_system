import pymysql
import pymysql.cursors

def get_db_connection():
    # Returns a database cursor connection
    return pymysql.connect(host='localhost',
                           user='root',
                           password='your_password',
                           db='landslide_flood_db',
                           cursorclass=pymysql.cursors.DictCursor)

def store_sensor_data(sensor_data):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = """
            INSERT INTO `sensordata` \
                (sensor_id, timestamp, measured_values) \
                VALUES (%s, %s, %s)
            """
            cursor.execute(sql, (sensor_data['sensor_id'], sensor_data['timestamp'], sensor_data['measured_values']))
        connection.commit()
    finally:
        connection.close()