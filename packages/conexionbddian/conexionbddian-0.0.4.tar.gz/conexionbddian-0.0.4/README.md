# Utilidad para la Base de Datos SOLEM

Este módulo de Python proporciona un conjunto de utilidades para interactuar con la base de datos Oracle SOLEM utilizando `cx_Oracle` y `SQLAlchemy`. Las utilidades incluyen funciones para conectarse a la base de datos, ejecutar consultas SQL y devolver resultados como DataFrames de Pandas.

## Características

- **Conexión a la Base de Datos:** Establece una conexión con la base de datos Oracle SOLEM utilizando credenciales almacenadas en un archivo de entorno.
- **Ejecución de Consultas:** Ejecuta consultas SQL utilizando `cx_Oracle` o `SQLAlchemy`.
- **Recuperación de Datos:** Recupera los resultados de las consultas como DataFrames de Pandas para una fácil manipulación y análisis.
- **Creación de Engine:** Crea un motor de SQLAlchemy para operaciones avanzadas con la base de datos.

## Requisitos Previos

Antes de usar este módulo, asegúrate de que los siguientes paquetes estén instalados:

- `pandas`
- `python-decouple`
- `cx_Oracle`
- `SQLAlchemy`

Puedes instalarlos usando `pip`:

```bash
pip install pandas python-decouple cx_Oracle SQLAlchemy
```

## Configuración

Debes crear un archivo .env y colocarlo en $HOMEPATH. El archivo debe tener la siguiente información:

-USER=tu_usuario 
-PASSWORD=tu_contraseña
-SERVER=tu_servidor
-PORT=tu_puerto
-SERVICE_NAME=tu_nombre_de_servicio

De igual forma asegúrate de tener instalado el oracle instant client.
