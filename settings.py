from decouple import config
meses = ["none", "enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

content = {
  "museos" : config("museos"), 
  "cine" : config("cine"),
  "biblioteca_popular" : config("biblioteca_popular")
}

nombres_columnas=["cod_localidad","id_provincia","id_departamento","categoría","provincia","localidad","nombre","domicilio","código postal","número de teléfono","web","mail", "fuente"]

museos_drop = ["observaciones", "codigo_indicativo_telefono", "latitud", "longitud", "juridisccion", "anio_de_creacion", "descripcion_de_patrimonio", "anio_de_inauguracion"]

museos_rename = {"espacio_cultural_id": "cod_localidad", "provincia_id": "id_provincia", "localidad_id": "id_departamento", "categoria": "categoría", "direccion":"domicilio", "codigo_postal":"código postal", "telefono":"número de teléfono", "Mail":"mail", "Web":"web"}

cine_drop = ["Observaciones","Departamento","Piso","cod_area", "Información adicional", "Latitud", "Longitud", "TipoLatitudLongitud","tipo_gestion", "Pantallas", "Butacas", "espacio_INCAA", "año_actualizacion"]

cine_rename = {"Cod_Loc": "cod_localidad", "IdProvincia": "id_provincia", "IdDepartamento": "id_departamento", "Categoría": "categoría", "Provincia":"provincia", "Localidad":"localidad", "Nombre" : "nombre", "Dirección":"domicilio", "CP":"código postal", "Teléfono":"número de teléfono", "Mail":"mail", "Web":"web",  "Fuente":"fuente"}

biblioteca_rename = {"Cod_Loc": "cod_localidad", "IdProvincia": "id_provincia", "IdDepartamento": "id_departamento", "Categoría": "categoría", "Provincia":"provincia", "Localidad":"localidad", "Nombre" : "nombre", "Domicilio":"domicilio", "CP":"código postal", "Teléfono":"número de teléfono", "Mail":"mail", "Web":"web", "Fuente":"fuente"}

biblioteca_drop = ["Observacion","Departamento","Subcategoria","Piso","Cod_tel", "Información adicional", "Latitud", "Longitud", "TipoLatitudLongitud", "Tipo_gestion", "año_inicio", "Año_actualizacion"]

settings = {'pguser':config('pguser'),
              'pgpasswd':config('pgpasswd'),
              'pghost':config('pghost'),
              'pgport':config('pgport'),
              'pgdb':config('pgdb')
             }