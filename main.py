import requests 
import os 
import datetime
from bs4 import BeautifulSoup 
import pandas as pd
from settings import  *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s:%(name)s: %(message)s")

file_handler = logging.FileHandler("main.log") 
file_handler.setFormatter(formatter) 

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter) 

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# Adquisición de archivos fuente 

hoy = "{:%d-%m-%Y}".format(datetime.date.today())
mes = meses[int(datetime.date.today().month)]
agnio = hoy[-4:]
home = os.getcwd()

def download_file():
  """
  Obtiene los archivos fuente de forma local y los organiza en ruta siguiendo la siguiente estructura:
  “categoría\año-mes\categoria-dia-mes-año.csv”
  Si, el archivo del mismo día existe, este es reemplazado al momentp de corre de nuevo el script.
  """
  for cat, url in content.items():
    r = requests.get(url)
    s = BeautifulSoup(r.content, "html.parser")
    try:
      link = s.find('a', class_="btn btn-green btn-block").get('href')
    except AttributeError as e:
      logger.Error(e)
    except Exception as e:
      logger.Error(e)
    else:
      with requests.get(link, stream=True) as rq:
        if os.path.exists(f"{cat}/{agnio}-{mes}") == True:
          os.chdir(f"{cat}/{agnio}-{mes}")
        else:
          os.makedirs(f"{cat}/{agnio}-{mes}")
          logger.info(f" Directorio {cat}/{agnio}-{mes} creado exitosamente")
          os.chdir(f"{cat}/{agnio}-{mes}")
        with open(f"{cat}-{hoy}.csv", "wb") as file:
          file.write(rq.content)
          logger.info(f"archivo {cat}-{hoy}.csv adquirido, encoding {rq.apparent_encoding}" )
    os.chdir(home)

cat=list(content.keys())

# Procesamiento de Datos

def process_data():
    """
    Transforma los datos de los archivos fuente en la información que va a nutrir la base de datos.

    Retorna:
      df1, df2, df3 
    """
    download_file()
    museos_df= pd.read_csv(f"{cat[0]}/{agnio}-{mes}/{cat[0]}-{hoy}.csv", encoding = "ISO-8859-1", engine='python')
    #categoria = ["Museos"]*len(museos_df)
    #museos_df["categoria"]=categoria
    museos_df.rename(columns = museos_rename ,inplace = True)
    museos_df.reindex(columns=nombres_columnas)
    museos =museos_df.drop(columns=museos_drop ,inplace=False)
    
    cine_df=pd.read_csv(f"{cat[1]}/{agnio}-{mes}/{cat[1]}-{hoy}.csv", encoding = "utf-8", engine='python')
    cine_df.rename(columns = cine_rename ,inplace = True)
    cine_df.reindex(columns=nombres_columnas)
    cine = cine_df.drop(columns= cine_drop ,inplace=False)

    biblioteca_df=pd.read_csv(f"{cat[2]}/{agnio}-{mes}/{cat[2]}-{hoy}.csv", encoding = "utf-8", engine='python')
    biblioteca_df.rename(columns = biblioteca_rename ,inplace = True)
    biblioteca_df.reindex(columns=nombres_columnas)
    biblioteca = biblioteca_df.drop(columns=biblioteca_drop,inplace=False)
    df= pd.concat([museos, cine, biblioteca], ignore_index=True)
    df1=df.drop(columns=["fuente"])
    a = pd.DataFrame(df.groupby(["categoría"]).count().sum())
    b = pd.DataFrame(df.groupby(["fuente"]).count().sum())
    c = pd.DataFrame(df.groupby(["provincia","categoría"]).count().sum())
    df2 = pd.concat([a, b, c], axis=1, keys=["registros totales por categoría", "registros totales por fuente", "registros por categoría y provincia"])
    tabla_cine = cine_df[["provincia","Pantallas","Butacas","espacio_INCAA"]]
    df3 = tabla_cine.groupby(["provincia"]).count()
   
    return (df1, df2, df3)

try:
  df1, df2, df3 = process_data()
  logger.info("Datos Procesados")
except Exception as e:
  logger.error(e)


# Conexión a la base de datos.

def get_database():
    """
    Conecta la base de datos.
    Retorna:
        engine
    """
    try:
        engine = get_engine(settings['pguser'],
                      settings['pgpasswd'],
                      settings['pghost'],
                      settings['pgport'],
                      settings['pgdb'])
        logger.info("Conectado a la base de datos PostgreSQL!")
    except IOError:
        logger.exception("Error al tratar de conectarse a la base de datos!")
        return None, 'fail'
    return engine

def get_engine(user, passwd, host, port, db):
    """
    Obtiene el Engine de la base de datos PostgreSQL.
    Input:
        db: Nombre de la base de datos
        user: Usuario
        host: Hostname del servidor de la base de datos
        port: Numero de puerto ()
        passwd: Contraseña de la base de datos
    Retorna:
        engine de la base de datos
    """
    url = 'postgresql://{user}:{passwd}@{host}:{port}/{db}'.format(
        user=user, passwd=passwd, host=host, port=port, db=db)

    engine = create_engine(url)
    return engine

def get_session():
    """
    Return an SQLAlchemy session
    Input:
        engine: an SQLAlchemy engine
    """
    engine = get_database()
    session = sessionmaker(bind=engine)()
    #session = Session()
    return engine, session

bd, session = get_session()
Base = declarative_base()

# Actualización de la base de Datos 

def delete_table(session, tabla):
  sql = "DROP TABLE %s" %tabla
  crsr = session.bind.raw_connection().cursor()
  crsr.execute(sql)
  session.commit()

#delete_table(session, "tabla_1")
#delete_table(session, "tabla_2")
#delete_table(session, "tabla_3")

def db_update():
    """
    Actualiza la información de las tablas en la base de datos. 
    """
    try:
        timestamp = [f"{hoy}"]*len(df1)
        df1["fecha"] = timestamp
        df1.to_sql("tabla_1", bd, if_exists = "replace")
        timestamp = [f"{hoy}"]*len(df2)
        df2["fecha"] = timestamp
        df2.to_sql("tabla_2", bd, if_exists = "replace")
        timestamp = [f"{hoy}"]*len(df3)
        df3["fecha"] = timestamp
        df3.to_sql("tabla_3", bd, if_exists = "replace")
        logger.info("La base de datos ha sido actualizada")
    except Exception as e:
        logger.error(e)

db_update()
if __name__ == "__main__":
  Base.metadata.drop_all(bd)
  Base.metadata.create_all(bd)
