import pandas as pd
from main import bd, session
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s:%(name)s:%(message)s")

file_handler = logging.FileHandler("script.log") 
file_handler.setFormatter(formatter) 

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter) 

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


cursor = session.bind.raw_connection().cursor()
def sql_query(sql,inf):
    cursor.execute(sql)
    for row in cursor:
        print(row)
    logger.info(inf)

sql = "SELECT * FROM tabla_1 WHERE domicilio IS NULL;"
inf = "chequenado que los valores 'NAN' de tabla_1 hayan sido cargados como NULL"
sql_query((sql),(inf))

sql = "SELECT * FROM tabla_2;"
inf = "cantidad de registros totales"
sql_query((sql),(inf))

sql = "SELECT * FROM tabla_3;"
inf = "información procesada de cines"
sql_query((sql),(inf))
logger.info("script finalizado.")