import os
import pandas as pd
from decouple import Config, RepositoryEnv
from cx_Oracle import Connection, connect, init_oracle_client
from sqlalchemy import create_engine,text
from .conexionbddian import (conectarSOLEM, consultarSOLEMpd, consultarSOLEMcursor, 
                             ejecutarQuery, consultarSOLEMsa, crear_engine)

config = Config(RepositoryEnv(os.path.join(os.environ.get("HOMEPATH"), ".env")))
user = config('USER')
pwd = config('PASSWORD')
server = config('SERVER')
port = config('PORT')
service = config('SERVICE_NAME')

