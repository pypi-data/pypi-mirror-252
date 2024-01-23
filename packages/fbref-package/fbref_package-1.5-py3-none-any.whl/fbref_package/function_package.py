import pandas as pd
from sqlalchemy import create_engine
import sqlalchemy
import mysql.connector

var_host='dbmbds.cfngygfor8bi.us-east-1.rds.amazonaws.com' 
var_port='3306'
var_database='db_fbref'
var_user='admin'
var_password='mbdsf*2022'
# var_host='localhost' 
# var_port='8889'
# var_database='db_fbref'
# var_user='root'
# var_password='root'

# Parámetros de conexión a tu base de datos
connection_params = {
    'user': var_user,
    'password': var_password,
    'host': var_host,
    'port': var_port,
    'database': var_database
}

# def query_to_dataframe(competition_id, season, query, connection_params):
def query_to_dataframe(query, connection_params):
    """
    Ejecuta una consulta SQL y devuelve los resultados en un DataFrame de pandas.
    Si hay un error, devuelve un mensaje indicando que los parámetros son incorrectos.

    :param competition_id: ID de la competición
    :param season: Temporada
    :param query: Consulta SQL con placeholders para competition_id y season
    :param connection_params: Parámetros de conexión a la base de datos
    :return: DataFrame de pandas con el resultado de la consulta o un mensaje de error
    """
    # Crear conexión a la base de datos
    # conn = mysql.connector.connect(**connection_params)

    connection_string = f"mysql+mysqlconnector://{connection_params['user']}:{connection_params['password']}@{connection_params['host']}:{connection_params['port']}/{connection_params['database']}"
    # Crear un motor de conexión con SQLAlchemy
    engine = create_engine(connection_string)

    try:
        # Formatear la consulta con los parámetros
        # formatted_query = query.format(competition_id=competition_id, season=season, table=table)

        # Ejecutar la consulta y cargar en DataFrame
        # df = pd.read_sql_query(formatted_query, conn)
        df = pd.read_sql_query(query, engine)
        return df

    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        return pd.DataFrame()  # Devuelve un DataFrame vacío

    finally:
        # Cerrar la conexión, independientemente de si hubo un error o no
        engine.dispose()

def getData(competition_id, season, tabla):

    consulta_sql = "SELECT * FROM "+tabla+" WHERE competition_id = '"+competition_id+"' AND season = '"+season+"'"
    result = query_to_dataframe(consulta_sql, connection_params)

    return result

def getCompetitions():
    
    consulta_sql = "SELECT * FROM competitions "
    result = query_to_dataframe(consulta_sql, connection_params)

    return result

def getTables():
    """
    Devuelve una lista de las tablas en una base de datos MySQL específica.

    :param host: Host de la base de datos
    :param usuario: Usuario de la base de datos
    :param password: Contraseña del usuario
    :param nombre_base_datos: Nombre de la base de datos
    :param puerto: Puerto de la base de datos (por defecto 3306)
    :return: Lista de nombres de tablas
    """
    try:
        # Crear la conexión a la base de datos
        conexion = mysql.connector.connect(
            host=connection_params['host'],
            user=connection_params['user'],
            passwd=connection_params['password'],
            database=connection_params['database'],
            port=connection_params['port']
        )

        # Crear un cursor
        cursor = conexion.cursor()

        # Ejecutar la consulta para obtener los nombres de las tablas
        cursor.execute("SHOW TABLES")

        # Recuperar todos los resultados
        tablas = cursor.fetchall()

        # Convertir la lista de bytearray en una lista de cadenas
        nombres_tablas = [tabla[0].decode("utf-8") for tabla in tablas]

        # Cerrar la conexión
        cursor.close()
        conexion.close()

        return nombres_tablas

    except mysql.connector.Error as error:
        print(f"Error al conectarse a MySQL: {error}")
        return []