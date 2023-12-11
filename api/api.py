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


def datos_parcela_prueba(connection,parcela_id):
    if connection:
        try:
            cursor = connection.cursor()
            query = 'select suelos.nombre,suelos.descripcion,suelos.composicion,suelos.drenaje,suelos.pH,suelos.retencionAgua,suelos.texturaSuelo,suelos.capacidadAireacion,suelos.propiedadesViticultura from suelos inner join tipoDeSueloParcela on suelos.id = tipoDeSueloParcela.id_suelo where tipoDeSueloParcela.id_parcela = %s'
            cursor.execute(query, (parcela_id,))
            data = cursor.fetchall()
            cursor.close()
            return data
        except mysql.connector.Error as err:
            print(f"Error al consultar a la base de datos: {err}")
            return []
    else:
        return []


def datos_parcela(connection,parcela_id):
    if connection:
        try:
            cursor = connection.cursor()

            # Ejecutar la primera consulta
            cursor.execute('select suelos.nombre,suelos.descripcion,suelos.composicion,suelos.drenaje,suelos.pH,suelos.retencionAgua,suelos.texturaSuelo,suelos.capacidadAireacion,suelos.propiedadesViticultura from suelos inner join tipoDeSueloParcela on suelos.id = tipoDeSueloParcela.id_suelo where tipoDeSueloParcela.id_parcela = %s',(parcela_id,))
            suelos = cursor.fetchall()

            # Ejecutar la segunda consulta
            cursor.execute('SELECT tareas.nombre_tarea, tareas.descripcion, tareas.fecha_creacion, tareas.fecha_limite, tareas.estado FROM tareas')
            tareas = cursor.fetchall()

            cursor.close()

            # Retornar los resultados en un diccionario
            return {
                "suelos": suelos,
                "tareas": tareas
            }

        except mysql.connector.Error as err:
            print(f"Error al consultar a la base de datos: {err}")
            return []
    else:
        return []

#select suelos.nombre,suelos.descripcion,suelos.composicion,suelos.drenaje,suelos.pH,suelos.retencionAgua,suelos.texturaSuelo,suelos.capacidadAireacion,suelos.propiedadesViticultura from suelos inner join tipoDeSueloParcela on suelos.id = tipoDeSueloParcela.id_suelo where tipoDeSueloParcela.id_parcela = "53f1b371-1045-447a-ab8e-cdb4c93b6b04";

#nombre, descripcion, composicion, drenaje, pH, retencionAgua, texturaSuelo, capacidadAireacion, propiedadesViticultura

