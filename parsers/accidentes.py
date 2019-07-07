# encoding: utf-8

import gvsig

from org.gvsig.fmap.geom.aggregate import MultiPolygon
from org.gvsig.scripting.app.extension import ScriptingUtils
import xmltodic
from org.gvsig.fmap.geom import GeometryUtils

from util import sino2bool, null2empty, null2zero, get1, get2, Descriptor


class AccidentesParser(object):
  
  def __init__(self, fname, xml=None):
    self.fname = fname
    self.xml = xml
    self.informeCorriente = None
    self.accidenteCorriente = None
    self.columns = None

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
    if self.columns!=None:
      return self.columns
    self.columns = [
      Descriptor("LID_ACCIDENTE","String",20,hidden=True, pk=True),
      Descriptor("COD_INFORME","String",20,
        label="Id. informe")\
        .foreingkey("ARENA2_INFORMES","COD_INFORME","FORMAT('%s',COD_INFORME)"),
      Descriptor("ID_ACCIDENTE","String",20
        label="Cod. accidente")\
        .set("DAL.Search.Attribute.Priority",1),
      #Descriptor("TIPO_ACCIDENTE","Integer",
      #  label="Tipo accidente"),
      Descriptor("FECHA_ACCIDENTE","Date",
        label= "Fecha accidente")\
        .set("DAL.Search.Attribute.Priority",6),
      Descriptor("HORA_ACCIDENTE","Time", 
        Label="Hora accidente")\
        .set("DAL.Search.Attribute.Priority",7),
      Descriptor("COD_PROVINCIA","String",45, 
        Label="Provincia")\
        .set("DAL.Search.Attribute.Priority",2),
      Descriptor("COD_MUNICIPIO","String",100, 
        Label="Municipio"),
      Descriptor("COD_POBLACION","String",100, 
        Label="Poblacion"),
      Descriptor("ZONA","Integer", 
        Label="Zona")\
        .selectablefk("ARENA2_DIC_ZONA"),
      Descriptor("TIPO_VIA","Integer", 
        Label="Tipo de via")\
        .selectablefk("ARENA2_DIC_TIPO_VIA"),
      Descriptor("TIPO_VIA_DGT","Integer", 
        Label="Tipo de via original")\
        .selectablefk("ARENA2_DIC_TIPO_VIA"),
      Descriptor("CARRETERA","String", 
        Label="Carretera")\
        .set("DAL.Search.Attribute.Priority",3),
      Descriptor("CARRETERA_DGT","String", 
        Label="Carretera original")\
        .set("DAL.Search.Attribute.Priority",3),
      Descriptor("KM","Double",
        label="Punto kilometrico")\
        .set("DAL.Search.Attribute.Priority",4),
      Descriptor("TITULARIDAD_VIA","Integer", 
        Label="Titularidad de la via")\
        .selectablefk("ARENA2_DIC_TITULARIDAD_VIA",
      Descriptor("TITULARIDAD_VIA_DGT","Integer", 
        Label="Titularidad de la via original")\
        .selectablefk("ARENA2_DIC_TITULARIDAD_VIA",
      Descriptor("SENTIDO","Integer", 
        Label="Sentido")\
        .selectablefk("ARENA2_DIC_SENTIDO")\
        .set("DAL.Search.Attribute.Priority",5),
      Descriptor("CALLE_CODIGO","String",15
        label="Cod. calle"),
      Descriptor("CALLE_NOMBRE","String",150,
        label="Calle"),
      Descriptor("CALLE_NUMERO","String",10
        label="Calle numero"),
      Descriptor("MAPAY","Double"),
      Descriptor("MAPAX","Double"),
      Descriptor("MAPA", "Geometry", hidden=True, 
        geomtype="Point:2D", 
        SRS="EPSG:4326" #, 
        #expression="TRY ST_SetSRID(ST_Point(MAPAX,MAPAY),4326) EXCEPT NULL"
      ),

      Descriptor("NUDO","Integer",
        label="Nudo")\
        .selectablefk("ARENA2_DIC_NUDO"),
      Descriptor("NUDO_INFO","Integer",
        label="Nudo, informacion")\
        .selectablefk("ARENA2_DIC_NUDO_INFORMACION"),
      Descriptor("CRUCE_CALLE","String",150,
        label="Cruce"),
      Descriptor("CRUCE_INE_CALLE","String",10,
        label="Cruce INE"),
      Descriptor("TOTAL_VEHICULOS","Integer"
        label="Total vehiculos implicados")\
        .set("DAL.Search.Attribute.Priority",13),
      Descriptor("TOTAL_CONDUCTORES","Integer"
        label="Total conductores implicados"),
      Descriptor("TOTAL_PASAJEROS","Integer"
        label="Total pasajeros implicados"),
      Descriptor("TOTAL_PEATONES","Integer"
        label="Total peatones implicados"),
      Descriptor("NUM_TURISMOS","Integer"
        label="Num. turismos implicados"),
      Descriptor("NUM_FURGONETAS","Integer"
        label="Num. furgonetas implicados"),
      Descriptor("NUM_CAMIONES","Integer"
        label="Num. camiones implicados"),
      Descriptor("NUM_AUTOBUSES","Integer"
        label="Num. autobuses implicados"),
      Descriptor("NUM_CICLOMOTORES","Integer"
        label="Num. ciclomotores implicados"),
      Descriptor("NUM_MOTOCICLETAS","Integer"
        label="Num. motocicletas implicados"),
      Descriptor("NUM_BICICLETAS","Integer"
        label="Num. bicicletas implicados"),
      Descriptor("NUM_OTROS_VEHI","Integer"
        label="Num. otros vehiculos implicados"),

      Descriptor("TIPO_ACC_SALIDA","Integer",
        label="Tipo accidente (Salida)"),
        .selectablefk("ARENA2_DIC_TIPO_ACCICENTE_SALIDA"),
      Descriptor("TIPO_ACC_COLISION","Integer"
        label="Tipo accidente (Colision)"),
        .selectablefk("ARENA2_DIC_TIPO_ACCIDENTE_COLISION"),
      Descriptor("SENTIDO_CONTRARIO","Boolean"
        label="Circular sentido contrario"),
      Descriptor("CONDICION_NIVEL_CIRCULA","Integer"
        label="Nivel circulacion")\
        .selectablefk("ARENA2_DIC_NIVEL_CIRCULACION"),
      Descriptor("INFLU_NIVEL_CIRC","Boolean"),
      Descriptor("CONDICION_FIRME","Integer"),
      Descriptor("INFLU_SUP_FIRME","Boolean"),
      Descriptor("CONDICION_ILUMINACION","Integer"),
      Descriptor("INFLU_ILUMINACION","Boolean"),
      Descriptor("CONDICION_METEO","Integer"),
      Descriptor("INFLU_METEO","Boolean"),
      Descriptor("VISIB_RESTRINGIDA_POR","Integer"),
      Descriptor("INFLU_VISIBILIDAD","Boolean"),
      Descriptor("CARACT_FUNCIONAL_VIA","Integer"),
      Descriptor("VEL_GENERICA_SENYALIZADA","Integer"),

      Descriptor("VELOCIDAD","Double"),
      Descriptor("SENTIDOS_VIA","Integer"),
      Descriptor("NUMERO_CALZADAS","Integer"),
      Descriptor("CARRILES_APTOS_CIRC_ASC","Integer"),
      Descriptor("CARRILES_APTOS_CIRC_DESC","Integer"),
      Descriptor("ANCHURA_CARRIL","Integer"),
      Descriptor("ARCEN","Integer"),
      Descriptor("ACERA","Integer"),
      Descriptor("INFU_ACERA","Boolean"),
      Descriptor("ANCHURA_ACERA","Integer"),
      Descriptor("TRAZADO_PLANTA","Integer"),
      Descriptor("TRAZADO_ALZADO","Integer"),
      Descriptor("MARCAS_VIALES","Integer"),
      Descriptor("DESCRIPCION","String",5120,profile="Text"),

      Descriptor("INFLU_PRIORIDAD","Boolean",group="Regulacion prioridad"),
      Descriptor("PRIORI_NORMA","Boolean",group="Regulacion prioridad"),
      Descriptor("PRIORI_AGENTE","Boolean",group="Regulacion prioridad"),
      Descriptor("PRIORI_SEMAFORO","Boolean",group="Regulacion prioridad"),
      Descriptor("PRIORI_VERT_STOP","Boolean",group="Regulacion prioridad"),
      Descriptor("PRIORI_VERT_CEDA","Boolean",group="Regulacion prioridad"),
      Descriptor("PRIORI_HORIZ_STOP","Boolean",group="Regulacion prioridad"),
      Descriptor("PRIORI_HORIZ_CEDA","Boolean",group="Regulacion prioridad"),
      Descriptor("PRIORI_MARCAS","Boolean",group="Regulacion prioridad"),
      Descriptor("PRIORI_PEA_NO_ELEV","Boolean",group="Regulacion prioridad"),
      Descriptor("PRIORI_PEA_ELEV","Boolean",group="Regulacion prioridad"),
      Descriptor("PRIORI_MARCA_CICLOS","Boolean",group="Regulacion prioridad"),
      Descriptor("PRIORI_CIRCUNSTANCIAL","Boolean",group="Regulacion prioridad"),
      Descriptor("PRIORI_OTRA","Boolean",group="Regulacion prioridad"),

      Descriptor("TOTAL_VICTIMAS","Integer"),
      Descriptor("TOTAL_MUERTOS","Integer")\
        .set("DAL.Search.Attribute.Priority",10),
      Descriptor("TOTAL_GRAVES","Integer")\
        .set("DAL.Search.Attribute.Priority",11),
      Descriptor("TOTAL_LEVES","Integer")\
        .set("DAL.Search.Attribute.Priority",12),
      Descriptor("TOTAL_ILESOS","Integer"),

      Descriptor("PANELES_DIRECCIONALES","Boolean"),
      Descriptor("HITOS_ARISTA","Boolean"),
      Descriptor("CAPTAFAROS","Boolean"),

      Descriptor("SEPARA_LINEA_LONG_SEPARACION","Boolean"),
      Descriptor("SEPARA_CEBREADO","Boolean"),
      Descriptor("SEPARA_MEDIANA","Boolean"),
      Descriptor("SEPARA_BARRERA_SEGURIDAD","Boolean"),
      Descriptor("SEPARA_ZONA_PEATONAL","Boolean"),
      Descriptor("SEPARA_OTRA_SEPARACION","Boolean"),
      Descriptor("SEPARA_NINGUNA_SEPARACION","Boolean"),

      Descriptor("BARRERA_SEG_LAT_ASC","Integer",group="Barrera seguridad"),
      Descriptor("BARRERA_SEG_LAT_ASC_MOTO","Boolean",group="Barrera seguridad"),
      Descriptor("BARRERA_SEG_LAT_DESC","Integer",group="Barrera seguridad"),
      Descriptor("BARRERA_SEG_LAT_DESC_MOTO","Boolean",group="Barrera seguridad"),
      Descriptor("BARRERA_SEG_MEDIANA_ASC","Integer",group="Barrera seguridad"),
      Descriptor("BARRERA_SEG_MEDIANA_ASC_MOTO","Boolean",group="Barrera seguridad"),
      Descriptor("BARRERA_SEG_MEDIANA_DESC","Integer",group="Barrera seguridad"),
      Descriptor("BARRERA_SEG_MEDIANA_DESC_MOTO","Boolean",group="Barrera seguridad"),

      Descriptor("TRAMO_PUENTE","Boolean",group="Elementos tramo"),
      Descriptor("TRAMO_TUNEL","Boolean",group="Elementos tramo"),
      Descriptor("TRAMO_PASO","Boolean",group="Elementos tramo"),
      Descriptor("TRAMO_ESTRECHA","Boolean",group="Elementos tramo"),
      Descriptor("TRAMO_RESALTOS","Boolean",group="Elementos tramo"),
      Descriptor("TRAMO_BADEN","Boolean",group="Elementos tramo"),
      Descriptor("TRAMO_APARTADERO","Boolean",group="Elementos tramo"),
      Descriptor("TRAMO_NINGUNA","Boolean",group="Elementos tramo"),

      Descriptor("INFLU_MARGEN","Boolean",group="Caracteristicas margen"),
      Descriptor("MARGEN_DESPEJADO","Boolean",group="Caracteristicas margen"),
      Descriptor("MARGEN_ARBOLES","Boolean",group="Caracteristicas margen"),
      Descriptor("MARGEN_OTROS_NATURALES","Boolean",group="Caracteristicas margen"),
      Descriptor("MARGEN_EDIFICIOS","Boolean",group="Caracteristicas margen"),
      Descriptor("MARGEN_POSTES","Boolean",group="Caracteristicas margen"),
      Descriptor("MARGEN_PUBLICIDAD","Boolean",group="Caracteristicas margen"),
      Descriptor("MARGEN_OTROS_ARTIFICIALES","Boolean",group="Caracteristicas margen"),
      Descriptor("MARGEN_OTROS_OBSTACULOS","Boolean",group="Caracteristicas margen"),
      Descriptor("MARGEN_DESC","Boolean",group="Caracteristicas margen"),

      Descriptor("INFLU_CIRCUNS_ESP","Boolean",group="Circunstancias especiales"),
      Descriptor("CIRCUNS_ESP_NINGUNA","Boolean",group="Circunstancias especiales"),
      Descriptor("CIRCUNS_ESP_CONOS","Boolean",group="Circunstancias especiales"),
      Descriptor("CIRCUNS_ESP_ZANJA","Boolean",group="Circunstancias especiales"),
      Descriptor("CIRCUNS_ESP_TAPA","Boolean",group="Circunstancias especiales"),
      Descriptor("CIRCUNS_ESP_OBRAS","Boolean",group="Circunstancias especiales"),
      Descriptor("CIRCUNS_ESP_OBSTACULO","Boolean",group="Circunstancias especiales"),
      Descriptor("CIRCUNS_ESP_DESPREND","Boolean",group="Circunstancias especiales"),
      Descriptor("CIRCUNS_ESP_ESCALON","Boolean",group="Circunstancias especiales"),
      Descriptor("CIRCUNS_ESP_FBACHES","Boolean",group="Circunstancias especiales"),
      Descriptor("CIRCUNS_ESP_FDETERIORADO","Boolean",group="Circunstancias especiales"),
      Descriptor("CIRCUNS_ESP_OTRAS","Boolean",group="Circunstancias especiales"),
      Descriptor("CIRCUNS_ESP_DESC","Boolean",group="Circunstancias especiales"),

      Descriptor("INFLU_DELIM_CALZADA","Boolean",group="Delimitacion calzada"),
      Descriptor("DELIM_CALZADA_BORDILLO","Boolean",group="Delimitacion calzada"),
      Descriptor("DELIM_CALZADA_VALLAS","Boolean",group="Delimitacion calzada"),
      Descriptor("DELIM_CALZADA_SETOS","Boolean",group="Delimitacion calzada"),
      Descriptor("DELIM_CALZADA_MARCAS","Boolean",group="Delimitacion calzada"),
      Descriptor("DELIM_CALZADA_BARRERA","Boolean",group="Delimitacion calzada"),
      Descriptor("DELIM_CALZADA_ISLETA","Boolean",group="Delimitacion calzada"),
      Descriptor("DELIM_CALZADA_PEATONAL","Boolean",group="Delimitacion calzada"),
      Descriptor("DELIM_CALZADA_OTRA","Boolean",group="Delimitacion calzada"),
      Descriptor("DELIM_CALZADA_SIN_DELIM","Boolean",group="Delimitacion calzada"),

      Descriptor("FC_CON_DISTRAIDA","Boolean",group="Factores concurrentes"),
      Descriptor("FC_VEL_INADECUADA","Boolean",group="Factores concurrentes"),
      Descriptor("FC_PRIORIDAD","Boolean",group="Factores concurrentes"),
      Descriptor("FC_SEGURIDAD","Boolean",group="Factores concurrentes"),
      Descriptor("FC_ADELANTAMIENTO","Boolean",group="Factores concurrentes"),
      Descriptor("FC_GIRO","Boolean",group="Factores concurrentes"),
      Descriptor("FC_CON_NEGLIGENTE","Boolean",group="Factores concurrentes"),
      Descriptor("FC_CON_TEMERARIA","Boolean",group="Factores concurrentes"),
      Descriptor("FC_IRRUPCION_ANIMAL","Boolean",group="Factores concurrentes"),
      Descriptor("FC_IRRUPCION_PEATON","Boolean",group="Factores concurrentes"),
      Descriptor("FC_ALCOHOL","Boolean",group="Factores concurrentes"),
      Descriptor("FC_DROGAS","Boolean",group="Factores concurrentes"),
      Descriptor("FC_ESTADO_VIA","Boolean",group="Factores concurrentes"),
      Descriptor("FC_METEORO","Boolean",group="Factores concurrentes"),
      Descriptor("FC_CANSANCIO","Boolean",group="Factores concurrentes"),
      Descriptor("FC_INEXPERIENCIA","Boolean",group="Factores concurrentes"),
      Descriptor("FC_AVERIA","Boolean",group="Factores concurrentes"),
      Descriptor("FC_OBRAS","Boolean",group="Factores concurrentes"),
      Descriptor("FC_MAL_ESTADO_VEHI","Boolean",group="Factores concurrentes"),
      Descriptor("FC_ENFERMEDAD","Boolean",group="Factores concurrentes"),
      Descriptor("FC_SENYALIZACION","Boolean",group="Factores concurrentes"),
      Descriptor("FC_OBSTACULO","Boolean",group="Factores concurrentes"),
      Descriptor("FC_OTRO_FACTOR","Boolean",group="Factores concurrentes"),

      Descriptor("VEHICULOS","List",group="Vehiculos")\
        .relatedFeatures(
          "ARENA2_VEHICULOS",
          "LID_VEHICULO",
          ("ID_VEHICULO","NACIONALIDAD","TIPO_VEHICULO","MARCA_NOMBRE","MODELO"),
          "FEATURES('ARENA2_VEHICULOS',FORMAT('ID_ACCIDENTE = ''%s''',ID_ACCIDENTE))"
        )\
        .set("dynform.label.empty",True),
      Descriptor("PEATONES","List",group="Peatones")\
        .relatedFeatures(
          "ARENA2_PEATONES",
          "LID_PEATON",
          ("ID_PEATON","FECHA_NACIMIENTO","SEXO","PAIS_RESIDENCIA","PROVINCIA_RESIDENCIA","MUNICIPIO_RESIDENCIA"),
          "FEATURES('ARENA2_PEATONES',FORMAT('ID_ACCIDENTE = ''%s''',ID_ACCIDENTE))"
        )\
        .set("dynform.label.empty",True),

      Descriptor("CROQUIS","List",group="Croquis")\
        .relatedFeatures(
          "ARENA2_CROQUIS",
          "LID_CROQUIS",
          ("ID_CROQUIS","IMAGEN"),
          "FEATURES('ARENA2_CROQUIS',FORMAT('ID_ACCIDENTE = ''%s''',ID_ACCIDENTE))"
        )\
        .set("dynform.label.empty",True)

    ] 
    return self.columns

  def getRowCount(self):
    self.rewind()
    rowCount = 0
    while True:
      informe, accidente = self.next()
      if accidente == None:
        return rowCount
      rowCount+=1
      
   
  def read(self):
    informe, accidente = self.next()
    if accidente == None:
      return None

    
    x = accidente.get("MAPAX", None)
    y = accidente.get("MAPAY", None)
    if x != None and y != None:
      geom = GeometryUtils.createPoint(float(x), float(y))
    else:
      geom = None
    
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
      null2zero(accidente.get("TIPO_VIA", None)),
      null2empty(accidente.get("CARRETERA", None)),
      null2empty(accidente.get("CARRETERA", None)),
      null2zero(accidente.get("KM", None)),
      null2zero(accidente.get("TITULARIDAD_VIA", None)),
      null2zero(accidente.get("TITULARIDAD_VIA", None)),
      null2zero(accidente.get("SENTIDO", None)),

      null2empty(accidente.get("CALLE_CODIGO", None)),
      null2empty(accidente.get("CALLE_NOMBRE", None)),
      null2empty(accidente.get("CALLE_NUMERO", None)),

      null2zero(accidente.get("MAPAY", None)),
      null2zero(accidente.get("MAPAX", None)),
      geom, # Campo geometria calculado
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


def main(*args):
  print Descriptor("FECHA_ACCIDENTE","Date",label="Accidente")
  print Descriptor("LID_ACCIDENTE","String",20,hidden=True, pk=True)
  print Descriptor("COD_INFORME","String",20,label="Informe")\
          .foreingkey("ARENA2_INFORMES","COD_INFORME","FORMAT('%s',COD_INFORME)")\
          
  print Descriptor("TIPO_VIA","Integer", Label="Tipo de via")\
          .selectablefk("ARENA2_DIC_TIPO_VIA")\
          
  print Descriptor("MAPA", "Geometry", hidden=True, 
        geomtype="Point:2D", 
        SRS="EPSG:4326", 
        expression="TRY ST_SetSRID(ST_Point(MAPAX,MAPAY),4326) EXCEPT NULL"
      )
  
