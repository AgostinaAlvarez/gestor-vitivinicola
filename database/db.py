import mysql.connector

def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='root',
            password='1234pin56',
            database='bd'
        )

        return connection
    except mysql.connector.Error as err:
        print(f"Error al connectar a la base de datos: {err}")
        return None


def fetch_data_from_table(connection):
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM usuarios")
            data = cursor.fetchall()
            cursor.close()
            return data
        except mysql.connector.Error as err:
            print(f"Error al consultar a la base de datos: {err}")
            return []
    else:
        return []