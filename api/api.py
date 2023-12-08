import mysql.connector

def get_viniedos (connection):
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT id, nombre, superficie, provincia, localidad, pais FROM viniedos")
            data = cursor.fetchall()
            cursor.close()
            return data
        except mysql.connector.Error as err:
            print(f"Error al consultar a la base de datos: {err}")
            return []
    else:
        return []


def get_tareas_home(connection):
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM tareas WHERE estado = "Pendiente" ORDER BY fecha_limite ASC')
            data = cursor.fetchall()
            cursor.close()
            return data
        except mysql.connector.Error as err:
            print(f"Error al consultar a la base de datos: {err}")
            return []
    else:
        return []



def get_parcelas_by_viniedo(connection, viniedo_id):
    if connection:
        try:
            cursor = connection.cursor()
            query = 'SELECT id,id_viniedo,nombre,superficie,latitud,longitud,ST_AsText(coordenadas) AS coordenadas_polygon FROM parcelas WHERE id_viniedo = %s LIMIT 0, 1000'
            cursor.execute(query, (viniedo_id,))
            data = cursor.fetchall()
            cursor.close()
            return data
        except mysql.connector.Error as err:
            print(f"Error al consultar a la base de datos: {err}")
            return []
    else:
        return []


def datos_viniedos(connection,viniedo_id):
    if connection:
        try:
            cursor = connection.cursor()
            query = 'SELECT id, nombre, superficie, provincia, localidad, pais, ST_AsText(coordenadas) AS coordenadas_polygon FROM viniedos WHERE id = %s LIMIT 0, 1000'
            cursor.execute(query, (viniedo_id,))
            data = cursor.fetchall()
            cursor.close()
            return data
        except mysql.connector.Error as err:
            print(f"Error al consultar a la base de datos: {err}")
            return []
    else:
        return []