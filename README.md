# alkemy-challenge
Challenge Data Analytics - Python

Este proyecto Consume datos desde 3 fuentes distintas para popular una base de datos SQL con información cultural
sobre bibliotecas, museos y salas de cines argentinos.

la configuracion necesaria se realiza desde un .env conteniendo los enlaces de las 3 fuentes y la configuración básica de la base de datos PostgreSQL.

los requerimientos necesarios para correr en un nuevo ambiente se pueden instalar haciendo "pip install r- requirements.txt" el documento requirements.txt esta incluido de la carpeta del proyecto.

el archivo "settings.py" contiene información para la configuración del proyecto como: los enlaces de los archivos fuente, la configuración de la base de datos, y algunas variables que facilitan la lectura/escritura del codigo.

el archivo "main.py" contiene todas las funciones que permiten: adquirir los archivos fuentes, procesar los datos, crear y actualizar las tablas dentro de la base de datos, segun los requerimientos.

el archivo "script.py" corre 3 querys de SQL usando un cursor.
