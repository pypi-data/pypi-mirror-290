import os
import pandas as pd
from decouple import Config, RepositoryEnv
from cx_Oracle import Connection, connect, init_oracle_client
from sqlalchemy import create_engine,text

config = Config(RepositoryEnv(os.path.join(os.environ.get("HOMEPATH"), ".env")))
user = config('USER')
pwd = config('PASSWORD')
server = config('SERVER')
port = config('PORT')
service = config('SERVICE_NAME')

def conectarSOLEM(user,pwd,server,port,service):
    '''
    Parameters
    ----------
    Returns
    -------
    Connection
        Conexión a base de datos SOLEM.

    '''
    conexion = connect(user=user
                        ,password=pwd
                        ,dsn=f"{server}:{port}/{service}")
    return conexion

def consultarSOLEMpd(query:str)->pd.DataFrame:
    '''
    Parameters
    ----------

    query : str
        Sentencia SQL.

    Returns
    -------
    DataFrame
        Resultado de la consulta.

    '''
    conexion = conectarSOLEM(user,pwd,server,port,service)
    consulta = pd.read_sql(query,conexion)
    conexion.close()
    return consulta

def consultarSOLEMcursor(query:str)->pd.DataFrame:
    '''
    Parameters
    ----------

    query : str
        Sentencia SQL.

    Returns
    -------
    DataFrame
        Resultado de la consulta.

    '''
    conexion = conectarSOLEM(user,pwd,server,port,service)
    cursor = conexion.cursor()
    cursor.execute(query)

    valores = [i for i in cursor]
    llaves = [i[0] for i in cursor.description]

    consulta = pd.DataFrame(valores, columns = llaves)
    cursor.close()
    conexion.close()
    return consulta


def ejecutarQuery(query:str):
    
    cadena_conexion = f'oracle+cx_oracle://{user}:{pwd}@{server}:{port}/?service_name={service}'
    conn_sqlalchemy = create_engine(cadena_conexion).connect()
    conn_sqlalchemy.execute(text(query))
    conn_sqlalchemy.close()

def consultarSOLEMsa(query:str)->pd.DataFrame:
    '''
    Parameters
    ----------

    query : str
        Sentencia SQL.

    Returns
    -------
    DataFrame
        Resultado de la consulta.

    '''
    
    cadena_conexion = f'oracle+cx_oracle://{user}:{pwd}@{server}:{port}/?service_name={service}'
    conn_sqlalchemy = create_engine(cadena_conexion).connect()
    consulta = pd.read_sql(query,conn_sqlalchemy)
    conn_sqlalchemy.close()
    return consulta


def crear_engine():
    cadena_conexion = f'oracle+cx_oracle://{user}:{pwd}@{server}:{port}/?service_name={service}'
    conn_sqlalchemy = create_engine(cadena_conexion).connect()
    return conn_sqlalchemy