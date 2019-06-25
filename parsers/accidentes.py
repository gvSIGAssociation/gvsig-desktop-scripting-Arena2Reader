# encoding: utf-8

import gvsig

from org.gvsig.fmap.geom.aggregate import MultiPolygon
from org.gvsig.scripting.app.extension import ScriptingUtils
import xmltodic
from org.gvsig.fmap.geom import GeometryUtils

from util import sino2bool, null2empty, null2zero, get1, get2

class AccidentesParser(object):
  
  def __init__(self, fname, xml=None):
    self.fname = fname
    self.xml = xml
    self.informeCorriente = None
    self.accidenteCorriente = None

  def getXML(self):
    return self.xml
    
  def open(self):
    if self.xml == None:
      fileXml = open(self.fname,"r")
      data = fileXml.read()
      fileXml.close()
      self.xml = xmltodic.parse(data)
      #print self.xml
    
    self.informeCorriente = 0
    self.accidenteCorriente = 0
    self.rewind()

  def rewind(self):
    self.informeCorriente = 0
    self.accideneteCorriente = 0
  
  def getInformes(self):
    informes = self.xml["INFORME"]
    if not isinstance(informes,list):
      informes = [ informes ]
    return informes

  def getAccidentes(self, informe):
    accidentes = informe["ACCIDENTES"]['ACCIDENTE']
    if not isinstance(accidentes,list):
      accidentes = [ accidentes ]
    return accidentes
  
  def getColumns(self):
    columns = [
      "LID_ACCIDENTE:String:size:20:set:hidden=true:set:pk=true",
      "COD_INFORME:String:size:20:set:label=Informe:set:foreingkey=true:set:foreingkey.table=ARENA2_INFORMES:set:foreingkey.code=COD_INFORME:set:foreingKey.Label=FORMAT('%s',COD_INFORME)",
      "ID_ACCIDENTE:String:size:20",
      "FECHA_ACCIDENTE:Date:set:label=Accidente",
      "HORA_ACCIDENTE:Time:set:label=Hora accidente",
      "COD_PROVINCIA:String:size:45:set:Label=Provincia",
      "COD_MUNICIPIO:String:size:100:set:Label=Municipio",
      "COD_POBLACION:String:size:100:set:Label=Poblacion",
      "ZONA:Integer:set:Label=Zona:set:foreingkey=true:set:foreingkey.selectable=true:set:foreingkey.Table=ARENA2_ZONA:set:foreingkey.Code=ID:set:foreingkey.Label=FORMAT('%02d - %s',ID,DESCRIPCION)",
      "TIPO_VIA:Integer:set:Label=Tipo de via:set:foreingkey=true:set:foreingkey.selectable=true:set:foreingkey.Table=ARENA2_TIPO_VIA:set:foreingkey.Code=ID:set:foreingkey.Label=FORMAT('%02d - %s',ID,DESCRIPCION)",
      "CARRETERA:String:size:20:set:Label=Carretera",
      "KM:Double",
      "TITULARIDAD_VIA:Integer:set:Label=Titularidad de la via:set:foreingkey=true:set:foreingkey.selectable=true:set:foreingkey.Table=ARENA2_TITULARIDAD_VIA:set:foreingkey.Code=ID:set:foreingkey.Label=FORMAT('%02d - %s',ID,DESCRIPCION)",
      "SENTIDO:Integer:set:Label=Sentido:set:foreingkey=true:set:foreingkey.selectable=true:set:foreingkey.Table=ARENA2_SENTIDO:set:foreingkey.Code=ID:set:foreingkey.Label=FORMAT('%02d - %s - %s',ID,TRADUCCION,DESCRIPCION)",
      "CALLE_CODIGO:String:size:15",
      "CALLE_NOMBRE:String:size:150",
      "CALLE_NUMERO:String:size:10",
      "MAPAY:Double",
      "MAPAX:Double",
      "MAPA/Geometry/set/geomtype=Point:2D/set/SRS=EPSG:4326/set/hidden=true/set/expression=TRY ST_SetSRID(ST_Point(MAPAX,MAPAY),4326) EXCEPT NULL",
      "NUDO:Integer:set:foreingkey=true:set:foreingkey.selectable=true:set:foreingkey.Table=ARENA2_NUDO:set:foreingkey.Code=ID:set:foreingkey.Label=FORMAT('%02d - %s',ID,DESCRIPCION)",
      "NUDO_INFO:Integer:set:foreingkey=true:set:foreingkey.selectable=true:set:foreingkey.Table=ARENA2_NUDO_INFORMACION:set:foreingkey.Code=ID:set:foreingkey.Label=FORMAT('%02d - %s',ID,DESCRIPCION)",
      "CRUCE_CALLE:String:size:150",
      "CRUCE_INE_CALLE:String:size:10",
      "TOTAL_VEHICULOS:Integer",
      "TOTAL_CONDUCTORES:Integer",
      "TOTAL_PASAJEROS:Integer",
      "TOTAL_PEATONES:Integer",
      "NUM_TURISMOS:Integer",
      "NUM_FURGONETAS:Integer",
      "NUM_CAMIONES:Integer",
      "NUM_AUTOBUSES:Integer",
      "NUM_CICLOMOTORES:Integer",
      "NUM_MOTOCICLETAS:Integer",
      "NUM_BICICLETAS:Integer",
      "NUM_OTROS_VEHI:Integer",
      "TIPO_ACC_SALIDA:Integer",
      "TIPO_ACC_COLISION:Integer",
      "SENTIDO_CONTRARIO:Boolean",
      "CONDICION_NIVEL_CIRCULA:Integer",
      "INFLU_NIVEL_CIRC:Boolean",
      "CONDICION_FIRME:Integer",
      "INFLU_SUP_FIRME:Boolean",
      "CONDICION_ILUMINACION:Integer",
      "INFLU_ILUMINACION:Boolean",
      "CONDICION_METEO:Integer",
      "INFLU_METEO:Boolean",
      "VISIB_RESTRINGIDA_POR:Integer",
      "INFLU_VISIBILIDAD:Boolean",
      "CARACT_FUNCIONAL_VIA:Integer",
      "VEL_GENERICA_SENYALIZADA:Integer",
      "VELOCIDAD:Double",
      "SENTIDOS_VIA:Integer",
      "NUMERO_CALZADAS:Integer",
      "CARRILES_APTOS_CIRC_ASC:Integer",
      "CARRILES_APTOS_CIRC_DESC:Integer",
      "ANCHURA_CARRIL:Integer",
      "ARCEN:Integer",
      "ACERA:Integer",
      "INFU_ACERA:Boolean",
      "ANCHURA_ACERA:Integer",
      "TRAZADO_PLANTA:Integer",
      "TRAZADO_ALZADO:Integer",
      "MARCAS_VIALES:Integer",
      "DESCRIPCION:String:size:1024:set:profile=Text",

      "INFLU_PRIORIDAD:Boolean:set:group=Regulacion prioridad",
      "PRIORI_NORMA:Boolean:set:group=Regulacion prioridad",
      "PRIORI_AGENTE:Boolean:set:group=Regulacion prioridad",
      "PRIORI_SEMAFORO:Boolean:set:group=Regulacion prioridad",
      "PRIORI_VERT_STOP:Boolean:set:group=Regulacion prioridad",
      "PRIORI_VERT_CEDA:Boolean:set:group=Regulacion prioridad",
      "PRIORI_HORIZ_STOP:Boolean:set:group=Regulacion prioridad",
      "PRIORI_HORIZ_CEDA:Boolean:set:group=Regulacion prioridad",
      "PRIORI_MARCAS:Boolean:set:group=Regulacion prioridad",
      "PRIORI_PEA_NO_ELEV:Boolean:set:group=Regulacion prioridad",
      "PRIORI_PEA_ELEV:Boolean:set:group=Regulacion prioridad",
      "PRIORI_MARCA_CICLOS:Boolean:set:group=Regulacion prioridad",
      "PRIORI_CIRCUNSTANCIAL:Boolean:set:group=Regulacion prioridad",
      "PRIORI_OTRA:Boolean:set:group=Regulacion prioridad",

      "TOTAL_VICTIMAS:Integer",
      "TOTAL_MUERTOS:Integer",
      "TOTAL_GRAVES:Integer",
      "TOTAL_LEVES:Integer",
      "TOTAL_ILESOS:Integer",

      "PANELES_DIRECCIONALES:Boolean",
      "HITOS_ARISTA:Boolean",
      "CAPTAFAROS:Boolean",

      "SEPARA_LINEA_LONG_SEPARACION:Boolean",
      "SEPARA_CEBREADO:Boolean",
      "SEPARA_MEDIANA:Boolean",
      "SEPARA_BARRERA_SEGURIDAD:Boolean",
      "SEPARA_ZONA_PEATONAL:Boolean",
      "SEPARA_OTRA_SEPARACION:Boolean",
      "SEPARA_NINGUNA_SEPARACION:Boolean",

      "BARRERA_SEG_LAT_ASC:Integer:set:group=Barrera seguridad",
      "BARRERA_SEG_LAT_ASC_MOTO:Boolean:set:group=Barrera seguridad",
      "BARRERA_SEG_LAT_DESC:Integer:set:group=Barrera seguridad",
      "BARRERA_SEG_LAT_DESC_MOTO:Boolean:set:group=Barrera seguridad",
      "BARRERA_SEG_MEDIANA_ASC:Integer:set:group=Barrera seguridad",
      "BARRERA_SEG_MEDIANA_ASC_MOTO:Boolean:set:group=Barrera seguridad",
      "BARRERA_SEG_MEDIANA_DESC:Integer:set:group=Barrera seguridad",
      "BARRERA_SEG_MEDIANA_DESC_MOTO:Boolean:set:group=Barrera seguridad",

      "TRAMO_PUENTE:Boolean:set:group=Elementos tramo",
      "TRAMO_TUNEL:Boolean:set:group=Elementos tramo",
      "TRAMO_PASO:Boolean:set:group=Elementos tramo",
      "TRAMO_ESTRECHA:Boolean:set:group=Elementos tramo",
      "TRAMO_RESALTOS:Boolean:set:group=Elementos tramo",
      "TRAMO_BADEN:Boolean:set:group=Elementos tramo",
      "TRAMO_APARTADERO:Boolean:set:group=Elementos tramo",
      "TRAMO_NINGUNA:Boolean:set:group=Elementos tramo",

      "INFLU_MARGEN:Boolean:set:group=Caracteristicas margen",
      "MARGEN_DESPEJADO:Boolean:set:group=Caracteristicas margen",
      "MARGEN_ARBOLES:Boolean:set:group=Caracteristicas margen",
      "MARGEN_OTROS_NATURALES:Boolean:set:group=Caracteristicas margen",
      "MARGEN_EDIFICIOS:Boolean:set:group=Caracteristicas margen",
      "MARGEN_POSTES:Boolean:set:group=Caracteristicas margen",
      "MARGEN_PUBLICIDAD:Boolean:set:group=Caracteristicas margen",
      "MARGEN_OTROS_ARTIFICIALES:Boolean:set:group=Caracteristicas margen",
      "MARGEN_OTROS_OBSTACULOS:Boolean:set:group=Caracteristicas margen",
      "MARGEN_DESC:Boolean:set:group=Caracteristicas margen",

      "INFLU_CIRCUNS_ESP:Boolean:set:group=Circunstancias especiales",
      "CIRCUNS_ESP_NINGUNA:Boolean:set:group=Circunstancias especiales",
      "CIRCUNS_ESP_CONOS:Boolean:set:group=Circunstancias especiales",
      "CIRCUNS_ESP_ZANJA:Boolean:set:group=Circunstancias especiales",
      "CIRCUNS_ESP_TAPA:Boolean:set:group=Circunstancias especiales",
      "CIRCUNS_ESP_OBRAS:Boolean:set:group=Circunstancias especiales",
      "CIRCUNS_ESP_OBSTACULO:Boolean:set:group=Circunstancias especiales",
      "CIRCUNS_ESP_DESPREND:Boolean:set:group=Circunstancias especiales",
      "CIRCUNS_ESP_ESCALON:Boolean:set:group=Circunstancias especiales",
      "CIRCUNS_ESP_FBACHES:Boolean:set:group=Circunstancias especiales",
      "CIRCUNS_ESP_FDETERIORADO:Boolean:set:group=Circunstancias especiales",
      "CIRCUNS_ESP_OTRAS:Boolean:set:group=Circunstancias especiales",
      "CIRCUNS_ESP_DESC:Boolean:set:group=Circunstancias especiales",

      "INFLU_DELIM_CALZADA:Boolean:set:group=Delimitacion calzada",
      "DELIM_CALZADA_BORDILLO:Boolean:set:group=Delimitacion calzada",
      "DELIM_CALZADA_VALLAS:Boolean:set:group=Delimitacion calzada",
      "DELIM_CALZADA_SETOS:Boolean:set:group=Delimitacion calzada",
      "DELIM_CALZADA_MARCAS:Boolean:set:group=Delimitacion calzada",
      "DELIM_CALZADA_BARRERA:Boolean:set:group=Delimitacion calzada",
      "DELIM_CALZADA_ISLETA:Boolean:set:group=Delimitacion calzada",
      "DELIM_CALZADA_PEATONAL:Boolean:set:group=Delimitacion calzada",
      "DELIM_CALZADA_OTRA:Boolean:set:group=Delimitacion calzada",
      "DELIM_CALZADA_SIN_DELIM:Boolean:set:group=Delimitacion calzada",

      "FC_CON_DISTRAIDA:Boolean:set:group=Factores concurrentes",
      "FC_VEL_INADECUADA:Boolean:set:group=Factores concurrentes",
      "FC_PRIORIDAD:Boolean:set:group=Factores concurrentes",
      "FC_SEGURIDAD:Boolean:set:group=Factores concurrentes",
      "FC_ADELANTAMIENTO:Boolean:set:group=Factores concurrentes",
      "FC_GIRO:Boolean:set:group=Factores concurrentes",
      "FC_CON_NEGLIGENTE:Boolean:set:group=Factores concurrentes",
      "FC_CON_TEMERARIA:Boolean:set:group=Factores concurrentes",
      "FC_IRRUPCION_ANIMAL:Boolean:set:group=Factores concurrentes",
      "FC_IRRUPCION_PEATON:Boolean:set:group=Factores concurrentes",
      "FC_ALCOHOL:Boolean:set:group=Factores concurrentes",
      "FC_DROGAS:Boolean:set:group=Factores concurrentes",
      "FC_ESTADO_VIA:Boolean:set:group=Factores concurrentes",
      "FC_METEORO:Boolean:set:group=Factores concurrentes",
      "FC_CANSANCIO:Boolean:set:group=Factores concurrentes",
      "FC_INEXPERIENCIA:Boolean:set:group=Factores concurrentes",
      "FC_AVERIA:Boolean:set:group=Factores concurrentes",
      "FC_OBRAS:Boolean:set:group=Factores concurrentes",
      "FC_MAL_ESTADO_VEHI:Boolean:set:group=Factores concurrentes",
      "FC_ENFERMEDAD:Boolean:set:group=Factores concurrentes",
      "FC_SENYALIZACION:Boolean:set:group=Factores concurrentes",
      "FC_OBSTACULO:Boolean:set:group=Factores concurrentes",
      "FC_OTRO_FACTOR:Boolean:set:group=Factores concurrentes",
      "VEHICULOS:List:set:group=Vehiculos:set:expression=FEATURES('ARENA2_VEHICULOS',FORMAT('ID_ACCIDENTE = ''%s''',ID_ACCIDENTE)):tag:dynform.label.empty=true:tag:DAL.RelatedFeatures.Columns=ID_VEHICULO/NACIONALIDAD/TIPO_VEHICULO/MARCA_NOMBRE/MODELO:tag:DAL.RelatedFeatures.table=ARENA2_VEHICULOS:tag:DAL.RelatedFeatures.Unique.Field.Name=LID_VEHICULO",
      "PEATONES:List:set:group=Peatones:set:expression=FEATURES('ARENA2_PEATONES',FORMAT('ID_ACCIDENTE = ''%s''',ID_ACCIDENTE)):tag:dynform.label.empty=true:tag:DAL.RelatedFeatures.Columns=ID_PEATON/FECHA_NACIMIENTO/SEXO/PAIS_RESIDENCIA/PROVINCIA_RESIDENCIA/MUNICIPIO_RESIDENCIA:tag:DAL.RelatedFeatures.table=ARENA2_PEATONES:tag:DAL.RelatedFeatures.Unique.Field.Name=LID_PEATON",
      "CROQUIS:List:set:group=Croquis:set:expression=FEATURES('ARENA2_CROQUIS',FORMAT('ID_ACCIDENTE = ''%s''',ID_ACCIDENTE)):tag:dynform.label.empty=true:tag:DAL.RelatedFeatures.Columns=ID_CROQUIS/IMAGEN:tag:DAL.RelatedFeatures.table=ARENA2_CROQUIS:tag:DAL.RelatedFeatures.Unique.Field.Name=LID_CROQUIS"
    ] 
    return columns

  def getRowCount(self):
    self.rewind()
    rowCount = 0
    while True:
      informe, accidente = self.next()
      if accidente == None:
        return rowCount;
      rowCount+=1
      
   
  def read(self):
    informe, accidente = self.next()
    if accidente == None:
      return None

    """
    x = accidente.get("MAPAX", None)
    y = accidente.get("MAPAY", None)
    if x != None and y != None:
      geom = GeometryUtils.createPoint(float(x), float(y))
    else:
      geom = None
    """
    
    values = [
      null2empty(accidente.get("@ID_ACCIDENTE", None)),
      null2empty(informe.get("@COD_INFORME", None)),

      null2empty(accidente.get("@ID_ACCIDENTE", None)),
      null2empty(accidente.get("FECHA_ACCIDENTE", None)),
      null2empty(accidente.get("HORA_ACCIDENTE", None)),
      null2empty(accidente.get("COD_PROVINCIA", None)),
      null2empty(accidente.get("COD_MUNICIPIO", None)),
      null2empty(accidente.get("COD_POBLACION", None)),
      null2zero(accidente.get("ZONA", None)),
      null2zero(accidente.get("TIPO_VIA", None)),
      null2empty(accidente.get("CARRETERA", None)),
      null2zero(accidente.get("KM", None)),
      null2zero(accidente.get("TITULARIDAD_VIA", None)),
      null2zero(accidente.get("SENTIDO", None)),

      null2empty(accidente.get("CALLE_CODIGO", None)),
      null2empty(accidente.get("CALLE_NOMBRE", None)),
      null2empty(accidente.get("CALLE_NUMERO", None)),

      null2zero(accidente.get("MAPAY", None)),
      null2zero(accidente.get("MAPAX", None)),
      None, # Campo geometria calculado
      null2zero(accidente.get("NUDO", None)),
      null2zero(accidente.get("NUDO_INFO", None)),
      
      null2empty(accidente.get("CRUCE_CALLE", None)),
      null2empty(accidente.get("CRUCE_INE_CALLE", None)),
      
      null2zero(accidente.get("TOTAL_VEHICULOS", None)),
      null2zero(accidente.get("TOTAL_CONDUCTORES", None)),
      null2zero(accidente.get("TOTAL_PASAJEROS", None)),
      null2zero(accidente.get("TOTAL_PEATONES", None)),
      null2zero(accidente.get("NUM_TURISMOS", None)),
      null2zero(accidente.get("NUM_FURGONETAS", None)),
      null2zero(accidente.get("NUM_CAMIONES", None)),
      null2zero(accidente.get("NUM_AUTOBUSES", None)),
      null2zero(accidente.get("NUM_CICLOMOTORES", None)),
      null2zero(accidente.get("NUM_MOTOCICLETAS", None)),
      null2zero(accidente.get("NUM_BICICLETAS", None)),
      null2zero(accidente.get("NUM_OTROS_VEHI", None)),
      
      null2zero(get2(accidente,"TIPO_ACCIDENTE","TIPO_ACC_SALIDA")),
      null2zero(get2(accidente,"TIPO_ACCIDENTE","TIPO_ACC_COLISION")),
      
      sino2bool(accidente.get("SENTIDO_CONTRARIO", None)),

      null2zero(get2(accidente,"CONDICION_NIVEL_CIRCULA","#text")),
      sino2bool(get2(accidente,"CONDICION_NIVEL_CIRCULA","@INFLU_NIVEL_CIRC")),
      null2zero(get2(accidente,"CONDICION_FIRME","#text")),
      sino2bool(get2(accidente,"CONDICION_FIRME","@INFLU_SUP_FIRME")),
      null2zero(get2(accidente,"CONDICION_ILUMINACION","#text")),
      sino2bool(get2(accidente,"CONDICION_ILUMINACION","@INFLU_ILUMINACION")),
      null2zero(get2(accidente,"CONDICION_METEO","#text")),
      sino2bool(get2(accidente,"CONDICION_METEO","@INFLU_METEO")),
      null2zero(get2(accidente,"VISIB_RESTRINGIDA_POR","#text")),
      sino2bool(get2(accidente,"VISIB_RESTRINGIDA_POR","@INFLU_VISIBILIDAD")),

      null2zero(accidente.get("CARACT_FUNCIONAL_VIA", None)),
      null2zero(accidente.get("VEL_GENERICA_SENYALIZADA", None)),

      null2zero(accidente.get("VELOCIDAD", None)),
      null2zero(accidente.get("SENTIDOS_VIA", None)),
      null2zero(accidente.get("NUMERO_CALZADAS", None)),

      null2zero(get2(accidente,"NUM_CARRILES","@CARRILES_APTOS_CIRC_ASC")),
      null2zero(get2(accidente,"NUM_CARRILES","@CARRILES_APTOS_CIRC_DESC")),
      null2zero(accidente.get("ANCHURA_CARRIL", None)),
      null2zero(accidente.get("ARCEN", None)),

      null2zero(get2(accidente,"ACERA","#text")),
      sino2bool(get2(accidente,"ACERA","@INFU_ACERA")),
      null2zero(accidente.get("ANCHURA_ACERA", None)),
      
      null2zero(accidente.get("TRAZADO_PLANTA", None)),
      null2zero(accidente.get("TRAZADO_ALZADO", None)),
      null2zero(accidente.get("MARCAS_VIALES", None)),
      null2empty(accidente.get("DESCRIPCION", None)),

      sino2bool(get2(accidente,"REGULACION_PRIORIDAD","@INFLU_PRIORIDAD")),
      sino2bool(get2(accidente,"REGULACION_PRIORIDAD","PRIORI_NORMA")),
      sino2bool(get2(accidente,"REGULACION_PRIORIDAD","PRIORI_AGENTE")),
      sino2bool(get2(accidente,"REGULACION_PRIORIDAD","PRIORI_SEMAFORO")),
      sino2bool(get2(accidente,"REGULACION_PRIORIDAD","PRIORI_VERT_STOP")),
      sino2bool(get2(accidente,"REGULACION_PRIORIDAD","PRIORI_VERT_CEDA")),
      sino2bool(get2(accidente,"REGULACION_PRIORIDAD","PRIORI_HORIZ_STOP")),
      sino2bool(get2(accidente,"REGULACION_PRIORIDAD","PRIORI_HORIZ_CEDA")),
      sino2bool(get2(accidente,"REGULACION_PRIORIDAD","PRIORI_MARCAS")),
      sino2bool(get2(accidente,"REGULACION_PRIORIDAD","PRIORI_PEA_NO_ELEV")),
      sino2bool(get2(accidente,"REGULACION_PRIORIDAD","PRIORI_PEA_ELEV")),
      sino2bool(get2(accidente,"REGULACION_PRIORIDAD","PRIORI_MARCA_CICLOS")),
      sino2bool(get2(accidente,"REGULACION_PRIORIDAD","PRIORI_CIRCUNSTANCIAL")),
      sino2bool(get2(accidente,"REGULACION_PRIORIDAD","PRIORI_OTRA")),

      null2zero(get2(accidente,"VICTIMAS","@TOTAL_VICTIMAS")),
      null2zero(get2(accidente,"VICTIMAS","TOTAL_MUERTOS")),
      null2zero(get2(accidente,"VICTIMAS","TOTAL_GRAVES")),
      null2zero(get2(accidente,"VICTIMAS","TOTAL_LEVES")),
      null2zero(get2(accidente,"VICTIMAS","TOTAL_ILESOS")),

      sino2bool(get2(accidente,"ELEMENTOS_BALIZAMIENTO","PANELES_DIRECCIONALES")),
      sino2bool(get2(accidente,"ELEMENTOS_BALIZAMIENTO","HITOS_ARISTA")),
      sino2bool(get2(accidente,"ELEMENTOS_BALIZAMIENTO","CAPTAFAROS")),

      sino2bool(get2(accidente,"ELEMENTOS_SEPARACION_SENTIDO","SEPARA_LINEA_LONG_SEPARACION")),
      sino2bool(get2(accidente,"ELEMENTOS_SEPARACION_SENTIDO","SEPARA_CEBREADO")),
      sino2bool(get2(accidente,"ELEMENTOS_SEPARACION_SENTIDO","SEPARA_MEDIANA")),
      sino2bool(get2(accidente,"ELEMENTOS_SEPARACION_SENTIDO","SEPARA_BARRERA_SEGURIDAD")),
      sino2bool(get2(accidente,"ELEMENTOS_SEPARACION_SENTIDO","SEPARA_ZONA_PEATONAL")),
      sino2bool(get2(accidente,"ELEMENTOS_SEPARACION_SENTIDO","SEPARA_OTRA_SEPARACION")),
      sino2bool(get2(accidente,"ELEMENTOS_SEPARACION_SENTIDO","SEPARA_NINGUNA_SEPARACION")),

      null2zero(get2(accidente,"BARRERA_SEGURIDAD","BARRERA_SEG_LAT_ASC")),
      sino2bool(get2(accidente,"BARRERA_SEGURIDAD","BARRERA_SEG_LAT_ASC_MOTO")),
      null2zero(get2(accidente,"BARRERA_SEGURIDAD","BARRERA_SEG_LAT_DESC")),
      sino2bool(get2(accidente,"BARRERA_SEGURIDAD","BARRERA_SEG_LAT_DESC_MOTO")),
      null2zero(get2(accidente,"BARRERA_SEGURIDAD","BARRERA_SEG_MEDIANA_ASC")),
      sino2bool(get2(accidente,"BARRERA_SEGURIDAD","BARRERA_SEG_MEDIANA_ASC_MOTO")),
      null2zero(get2(accidente,"BARRERA_SEGURIDAD","BARRERA_SEG_MEDIANA_DESC")),
      sino2bool(get2(accidente,"BARRERA_SEGURIDAD","BARRERA_SEG_MEDIANA_DESC_MOTO")),

      sino2bool(get2(accidente,"ELEMENTOS_TRAMO","TRAMO_PUENTE")),
      sino2bool(get2(accidente,"ELEMENTOS_TRAMO","TRAMO_TUNEL")),
      sino2bool(get2(accidente,"ELEMENTOS_TRAMO","TRAMO_PASO")),
      sino2bool(get2(accidente,"ELEMENTOS_TRAMO","TRAMO_ESTRECHA")),
      sino2bool(get2(accidente,"ELEMENTOS_TRAMO","TRAMO_RESALTOS")),
      sino2bool(get2(accidente,"ELEMENTOS_TRAMO","TRAMO_BADEN")),
      sino2bool(get2(accidente,"ELEMENTOS_TRAMO","TRAMO_APARTADERO")),
      sino2bool(get2(accidente,"ELEMENTOS_TRAMO","TRAMO_NINGUNA")),
      
      sino2bool(get2(accidente,"CARACTERISTICAS_MARGEN","@INFLU_MARGEN")),
      sino2bool(get2(accidente,"CARACTERISTICAS_MARGEN","MARGEN_DESPEJADO")),
      sino2bool(get2(accidente,"CARACTERISTICAS_MARGEN","MARGEN_ARBOLES")),
      sino2bool(get2(accidente,"CARACTERISTICAS_MARGEN","MARGEN_OTROS_NATURALES")),
      sino2bool(get2(accidente,"CARACTERISTICAS_MARGEN","MARGEN_EDIFICIOS")),
      sino2bool(get2(accidente,"CARACTERISTICAS_MARGEN","MARGEN_POSTES")),
      sino2bool(get2(accidente,"CARACTERISTICAS_MARGEN","MARGEN_PUBLICIDAD")),
      sino2bool(get2(accidente,"CARACTERISTICAS_MARGEN","MARGEN_OTROS_ARTIFICIALES")),
      sino2bool(get2(accidente,"CARACTERISTICAS_MARGEN","MARGEN_OTROS_OBSTACULOS")),
      sino2bool(get2(accidente,"CARACTERISTICAS_MARGEN","MARGEN_DESC")),

      sino2bool(get2(accidente,"CIRCUNSTANCIAS_ESPECIALES_VIA","@INFLU_CIRCUNS_ESP")),
      sino2bool(get2(accidente,"CIRCUNSTANCIAS_ESPECIALES_VIA","CIRCUNS_ESP_NINGUNA")),
      sino2bool(get2(accidente,"CIRCUNSTANCIAS_ESPECIALES_VIA","CIRCUNS_ESP_CONOS")),
      sino2bool(get2(accidente,"CIRCUNSTANCIAS_ESPECIALES_VIA","CIRCUNS_ESP_ZANJA")),
      sino2bool(get2(accidente,"CIRCUNSTANCIAS_ESPECIALES_VIA","CIRCUNS_ESP_TAPA")),
      sino2bool(get2(accidente,"CIRCUNSTANCIAS_ESPECIALES_VIA","CIRCUNS_ESP_OBRAS")),
      sino2bool(get2(accidente,"CIRCUNSTANCIAS_ESPECIALES_VIA","CIRCUNS_ESP_OBSTACULO")),
      sino2bool(get2(accidente,"CIRCUNSTANCIAS_ESPECIALES_VIA","CIRCUNS_ESP_DESPREND")),
      sino2bool(get2(accidente,"CIRCUNSTANCIAS_ESPECIALES_VIA","CIRCUNS_ESP_ESCALON")),
      sino2bool(get2(accidente,"CIRCUNSTANCIAS_ESPECIALES_VIA","CIRCUNS_ESP_FBACHES")),
      sino2bool(get2(accidente,"CIRCUNSTANCIAS_ESPECIALES_VIA","CIRCUNS_ESP_FDETERIORADO")),
      sino2bool(get2(accidente,"CIRCUNSTANCIAS_ESPECIALES_VIA","CIRCUNS_ESP_OTRAS")),
      sino2bool(get2(accidente,"CIRCUNSTANCIAS_ESPECIALES_VIA","CIRCUNS_ESP_DESC")),

      sino2bool(get2(accidente,"DELIMITACION_CALZADA","@INFLU_DELIM_CALZADA")),
      sino2bool(get2(accidente,"DELIMITACION_CALZADA","DELIM_CALZADA_BORDILLO")),
      sino2bool(get2(accidente,"DELIMITACION_CALZADA","DELIM_CALZADA_VALLAS")),
      sino2bool(get2(accidente,"DELIMITACION_CALZADA","DELIM_CALZADA_SETOS")),
      sino2bool(get2(accidente,"DELIMITACION_CALZADA","DELIM_CALZADA_MARCAS")),
      sino2bool(get2(accidente,"DELIMITACION_CALZADA","DELIM_CALZADA_BARRERA")),
      sino2bool(get2(accidente,"DELIMITACION_CALZADA","DELIM_CALZADA_ISLETA")),
      sino2bool(get2(accidente,"DELIMITACION_CALZADA","DELIM_CALZADA_PEATONAL")),
      sino2bool(get2(accidente,"DELIMITACION_CALZADA","DELIM_CALZADA_OTRA")),
      sino2bool(get2(accidente,"DELIMITACION_CALZADA","DELIM_CALZADA_SIN_DELIM")),

      sino2bool(get2(accidente,"FACTORES_CONCURRENTES","FC_CON_DISTRAIDA")),
      sino2bool(get2(accidente,"FACTORES_CONCURRENTES","FC_VEL_INADECUADA")),
      sino2bool(get2(accidente,"FACTORES_CONCURRENTES","FC_PRIORIDAD")),
      sino2bool(get2(accidente,"FACTORES_CONCURRENTES","FC_SEGURIDAD")),
      sino2bool(get2(accidente,"FACTORES_CONCURRENTES","FC_ADELANTAMIENTO")),
      sino2bool(get2(accidente,"FACTORES_CONCURRENTES","FC_GIRO")),
      sino2bool(get2(accidente,"FACTORES_CONCURRENTES","FC_CON_NEGLIGENTE")),
      sino2bool(get2(accidente,"FACTORES_CONCURRENTES","FC_CON_TEMERARIA")),
      sino2bool(get2(accidente,"FACTORES_CONCURRENTES","FC_IRRUPCION_ANIMAL")),
      sino2bool(get2(accidente,"FACTORES_CONCURRENTES","FC_IRRUPCION_PEATON")),
      sino2bool(get2(accidente,"FACTORES_CONCURRENTES","FC_ALCOHOL")),
      sino2bool(get2(accidente,"FACTORES_CONCURRENTES","FC_DROGAS")),
      sino2bool(get2(accidente,"FACTORES_CONCURRENTES","FC_ESTADO_VIA")),
      sino2bool(get2(accidente,"FACTORES_CONCURRENTES","FC_METEORO")),
      sino2bool(get2(accidente,"FACTORES_CONCURRENTES","FC_CANSANCIO")),
      sino2bool(get2(accidente,"FACTORES_CONCURRENTES","FC_INEXPERIENCIA")),
      sino2bool(get2(accidente,"FACTORES_CONCURRENTES","FC_AVERIA")),
      sino2bool(get2(accidente,"FACTORES_CONCURRENTES","FC_OBRAS")),
      sino2bool(get2(accidente,"FACTORES_CONCURRENTES","FC_MAL_ESTADO_VEHI")),
      sino2bool(get2(accidente,"FACTORES_CONCURRENTES","FC_ENFERMEDAD")),
      sino2bool(get2(accidente,"FACTORES_CONCURRENTES","FC_SENYALIZACION")),
      sino2bool(get2(accidente,"FACTORES_CONCURRENTES","FC_OBSTACULO")),
      sino2bool(get2(accidente,"FACTORES_CONCURRENTES","FC_OTRO_FACTOR")),
      None, # VEHICULOS
      None, # Peatones
      None # Croquis
    ]
    return values

  def next(self):
    if self.informeCorriente == None:
      return None, None
    
    informes = self.getInformes()
    while self.informeCorriente < len(informes):
      informe = informes[self.informeCorriente]
      #print "Informe: ", get1(informe,"@COD_INFORME"), self.informeCorriente
      accidentes = self.getAccidentes(informe)
      if self.accidenteCorriente < len(accidentes):
        accidente = accidentes[self.accidenteCorriente]
        #print "Accidente: ", get1(accidente,"@ID_ACCIDENTE"), self.accidenteCorriente
        self.accidenteCorriente += 1
        return informe, accidente

      self.informeCorriente += 1
      self.accidenteCorriente = 0

    self.informeCorriente = None
    return None, None
