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
    self.accidenteCorriente = 0
  
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
      Descriptor("LID_ACCIDENTE","String",20,hidden=True, pk=True, readOnly=True),
      Descriptor("COD_INFORME","String",20, readOnly=True,
        label="_Codigo_informe",
        shortLabel="_Cod_informe")\
        .foreingkey("ARENA2_INFORMES","COD_INFORME","FORMAT('%s',COD_INFORME)"),
      Descriptor("ID_ACCIDENTE","String",20, readOnly=True,
        label="_Codigo_accidente",
        shortLabel="_Cod_accidente")\
        .set("DAL.Search.Attribute.Priority",1),
      Descriptor("FECHA_ACCIDENTE","Date", readOnly=True,
        label= "_Fecha_accidente")\
        .set("DAL.Search.Attribute.Priority",6),
      Descriptor("HORA_ACCIDENTE","Time", readOnly=True, 
        label="_Hora_accidente")\
        .set("DAL.Search.Attribute.Priority",7),

      Descriptor("COD_PROVINCIA","String",45, readOnly=True, 
        label="_Provincia")\
        .set("DAL.Search.Attribute.Priority",2),
      Descriptor("COD_MUNICIPIO","String",100, readOnly=True, 
        label="_Municipio"),
      Descriptor("COD_POBLACION","String",100, readOnly=True, 
        label="_Poblacion"),
      Descriptor("ZONA","Integer", readOnly=True, 
        label="_Zona")\
        .selectablefk("ARENA2_DIC_ZONA"),
      Descriptor("TIPO_VIA","Integer", readOnly=False, 
        label="_Tipo_de_via",
        shortLabel="_Tipo_via")\
        .selectablefk("ARENA2_DIC_TIPO_VIA"),
      Descriptor("TIPO_VIA_DGT","Integer", readOnly=True, 
        label="_Tipo_de_via_original",
        shortLabel="_Tipo_via_orig")\
        .selectablefk("ARENA2_DIC_TIPO_VIA"),

      Descriptor("CARRETERA","String", readOnly=False, 
        label="_Carretera")\
        .set("DAL.Search.Attribute.Priority",3),
      Descriptor("CARRETERA_DGT","String", readOnly=True, 
        label="_Carretera_original",
        shortLabel="_Carretera_orig")\
        .set("DAL.Search.Attribute.Priority",3),
      Descriptor("KM","Double", readOnly=True,
        label="_Punto_kilometrico",
        shortLabel="_Pk")\
        .set("DAL.Search.Attribute.Priority",4),
      Descriptor("TITULARIDAD_VIA","Integer", readOnly=False, 
        label="_Titularidad_de_la_via",
        shortLabel="_Titularidad_via")\
        .selectablefk("ARENA2_DIC_TITULARIDAD_VIA"),

      Descriptor("TITULARIDAD_VIA_DGT","Integer", readOnly=True, 
        label="_Titularidad_de_la_via_original",
        shortlabel="_Titularidad_via_orig")\
        .selectablefk("ARENA2_DIC_TITULARIDAD_VIA"),
      Descriptor("SENTIDO","Integer", readOnly=True, 
        label="_Sentido")\
        .selectablefk("ARENA2_DIC_SENTIDO")\
        .set("DAL.Search.Attribute.Priority",5),
      Descriptor("CALLE_CODIGO","String",15, readOnly=True,
        label="_Codigo_calle",
        shortLabel="_Cod_calle"),
      Descriptor("CALLE_NOMBRE","String",150, readOnly=True,
        label="_Calle"),
      Descriptor("CALLE_NUMERO","String",10, readOnly=True,
        label="_Numero_de_calle",
        shortLabel="_Num_calle"),
      Descriptor("MAPAY","Double", readOnly=True),
      Descriptor("MAPAX","Double", readOnly=True),
      Descriptor("MAPA", "Geometry", hidden=True, 
        geomtype="Point:2D", 
        SRS="EPSG:4326" #, 
        #expression="TRY ST_SetSRID(ST_Point(MAPAX,MAPAY),4326) EXCEPT NULL"
      ),

      Descriptor("NUDO","Integer", readOnly=True,
        label="_Nudo")\
        .selectablefk("ARENA2_DIC_NUDO"),
      Descriptor("NUDO_INFO","Integer", readOnly=True,
        label="_Informacion_nudo",
        shortLabel="_Inf_nudo")\
        .selectablefk("ARENA2_DIC_NUDO_INFORMACION"),
      Descriptor("CRUCE_CALLE","String",150, readOnly=True,
        label="_Cruce"),
      Descriptor("CRUCE_INE_CALLE","String",10, readOnly=True,
        label="_Cruce_INE"),
      Descriptor("TOTAL_VEHICULOS","Integer", readOnly=True,
        label="_Total_vehiculos_implicados",
        shortlabel="_Tot_vehiculos")\
        .set("DAL.Search.Attribute.Priority",13),
      Descriptor("TOTAL_CONDUCTORES","Integer", readOnly=True,
        label="_Total_conductores_implicados",
        shortlabel="_Tot_conductores"),
      Descriptor("TOTAL_PASAJEROS","Integer", readOnly=True,
        label="_Total_pasajeros_implicados",
        shortlabel="_Tot_pasajeros"),
      Descriptor("TOTAL_PEATONES","Integer", readOnly=True,
        label="_Total_peatones_implicados",
        shortlabel="_Tot_peatones"),
      Descriptor("NUM_TURISMOS","Integer", readOnly=True,
        label="_Num_turismos_implicados",
        shortlabel="_Num_turismos"),
      Descriptor("NUM_FURGONETAS","Integer", readOnly=True,
        label="_Num_furgonetas_implicadas",
        shortlabel="_Num_furgonetas"),
      Descriptor("NUM_CAMIONES","Integer", readOnly=True,
        label="_Num_camiones_implicados",
        shortlabel="_Num_camiones"),
      Descriptor("NUM_AUTOBUSES","Integer", readOnly=True,
        label="_Num_autobuses_implicados",
        shortlabel="_Num_autobuses"),
      Descriptor("NUM_CICLOMOTORES","Integer", readOnly=True,
        label="_Num_ciclomotores_implicados",
        shortlabel="_Num_ciclomotores"),
      Descriptor("NUM_MOTOCICLETAS","Integer", readOnly=True,
        label="_Num_motocicletas_implicadas",
        shortlabel="_Num_motocicletas"),
      Descriptor("NUM_BICICLETAS","Integer", readOnly=True,
        label="_Num_bicicletas_implicadas",
        shortlabel="_Num_bicicletas"),
      Descriptor("NUM_OTROS_VEHI","Integer", readOnly=True,
        label="_Num_otros_vehiculos_implicados",
        shortlabel="_Num_otros_vehiculos"),

      Descriptor("TIPO_ACC_SALIDA","Integer", readOnly=True,
        label="_Tipo_accidente_Salida")\
        .selectablefk("ARENA2_DIC_TIPO_ACCICENTE_SALIDA"),
      Descriptor("TIPO_ACC_COLISION","Integer", readOnly=True,
        label="_Tipo_accidente_Colision")\
        .selectablefk("ARENA2_DIC_TIPO_ACCIDENTE_COLISION"),
      Descriptor("SENTIDO_CONTRARIO","Boolean", readOnly=True,
        label="_Circular_sentido_contrario"),
      Descriptor("CONDICION_NIVEL_CIRCULA","Integer", readOnly=True,
        label="_Nivel_circulacion")\
        .selectablefk("ARENA2_DIC_NIVEL_CIRCULACION"),

      ##-----------------
        
      Descriptor("INFLU_NIVEL_CIRC","Boolean", readOnly=True, 
        label="_Influye_nivel_circulacion"),
      Descriptor("CONDICION_FIRME","Integer", readOnly=True, 
        label="_Condicion_del_firme")\
        .selectablefk("ARENA2_DIC_CONDICION_FIRME"),
      Descriptor("INFLU_SUP_FIRME","Boolean", readOnly=True, 
        label="_Influye_firme"),
      Descriptor("CONDICION_ILUMINACION","Integer", readOnly=True, 
        label="_Iluminacion")\
        .selectablefk("ARENA2_DIC_ILUMINACION"),
      Descriptor("INFLU_ILUMINACION","Boolean", readOnly=True, 
        label="_Influye_iluminacion"),
      Descriptor("CONDICION_METEO","Integer", readOnly=True, 
        label="_Meteorologia")\
        .selectablefk("ARENA2_DIC_METEO"),
      Descriptor("INFLU_METEO","Boolean", readOnly=True, 
        label="_Influye_meteorologia"),
      Descriptor("VISIB_RESTRINGIDA_POR","Integer", readOnly=True, 
        label="_Visibilidad")\
        .selectablefk("ARENA2_DIC_VISIBILIDAD_RESTRINGIDA_POR"),
      Descriptor("INFLU_VISIBILIDAD","Boolean", readOnly=True, 
        label="_Influye visibilidad"),
      Descriptor("CARACT_FUNCIONAL_VIA","Integer", readOnly=True,
        label="_Caracteristicas_funcionales_de_la_via",
        shortLabel="_Caracteisticas_via")\
        .selectablefk("ARENA2_DIC_CARACT_FUNCIONAL_VIA"),
      Descriptor("VEL_GENERICA_SENYALIZADA","Integer", readOnly=True,
        label="_Velocidad_generica")\
        .selectablefk("ARENA2_DIC_VEL_GENERICA"),

      Descriptor("VELOCIDAD","Double", readOnly=True,
        label="_Velocidad"),
      Descriptor("SENTIDOS_VIA","Integer", readOnly=True,
        label="_Sentidos_via",
        shortlabel="_Sentidos"),
      Descriptor("NUMERO_CALZADAS","Integer", readOnly=True,
        label="_Numero_de_calzadas",
        shortlabel="_Num_calzadas")\
        .selectablefk("ARENA2_DIC_NUMERO_CALZADAS"),
      Descriptor("CARRILES_APTOS_CIRC_ASC","Integer", readOnly=True,
        label="_Carriles_aptos_circular_ascendente",
        shortlabel="_Carr_aptos_cir_asc"),
      Descriptor("CARRILES_APTOS_CIRC_DESC","Integer", readOnly=True,
        label="_Carriles_aptos_circular_descenente",
        shortlabel="_Carr_aptos_cir_desc"),
      Descriptor("ANCHURA_CARRIL","Integer", readOnly=True,
        label="_Anchura_de_carril",
        shortlabel="_Anchura_carril"),
      Descriptor("ARCEN","Integer", readOnly=True,
        label="_Arcen")\
        .selectablefk("ARENA2_DIC_ANCHURA_ARCEN"),
      Descriptor("ACERA","Integer", readOnly=True,
        label="_Acera")\
        .selectablefk("ARENA2_DIC_ACERA"),
      Descriptor("INFU_ACERA","Boolean", readOnly=True,
        label="_Influye_la_acera",
        shortLabel="_Influye_acera"),
      Descriptor("ANCHURA_ACERA","Integer", readOnly=True,
        label="_Anchua_acera"),
      Descriptor("TRAZADO_PLANTA","Integer", readOnly=True,
        label="_Trazado_planta")\
        .selectablefk("ARENA2_DIC_TRAZADO_PLANTA"),
      Descriptor("TRAZADO_ALZADO","Integer", readOnly=True,
        label="_Trazado_alzado")\
        .selectablefk("ARENA2_DIC_TRAZADO_ALZADO"),
      Descriptor("MARCAS_VIALES","Integer", readOnly=True,
        label="_Marcas_viales")\
        .selectablefk("ARENA2_DIC_MARCAS_VIALES"),
      Descriptor("DESCRIPCION","String",5120,profile="Text", readOnly=True),

      Descriptor("INFLU_PRIORIDAD","Boolean", readOnly=True,
        group="_Regulacion_prioridad",
        label="_Influye_la_regulacion_de_prioridad ",
        shortlabel="_Influye_RP"),
      Descriptor("PRIORI_NORMA","Boolean", readOnly=True,
        group="_Regulacion_prioridad",
        label="_RP_Norma_generica",
        shortlabel="_RP_Generica"),
      Descriptor("PRIORI_AGENTE","Boolean", readOnly=True,
        group="_Regulacion_prioridad",
        label="_RP_Agente",
        shortlabel="_RP_Agente"),
      Descriptor("PRIORI_SEMAFORO","Boolean", readOnly=True,
        group="_Regulacion_prioridad",
        label="_RP_Semaforo",
        shortlabel="_RP_Semaforo"),
      Descriptor("PRIORI_VERT_STOP","Boolean", readOnly=True,
        group="_Regulacion_prioridad",
        label="_RP_Señal_de_stop_vertical",
        shortlabel="_RP_Stop_vertical"),
      Descriptor("PRIORI_VERT_CEDA","Boolean", readOnly=True,
        group="_Regulacion_prioridad",
        label="_RP_Señal_ceda_el_paso_vertical",
        shortlabel="_RP_ceda_el_paso_vertical"),
      Descriptor("PRIORI_HORIZ_STOP","Boolean", readOnly=True,
        group="_Regulacion_prioridad",
        label="_RP_Señal_de_stop_horizontal",
        shortlabel="_RP_stop_horizontal"),
      Descriptor("PRIORI_HORIZ_CEDA","Boolean", readOnly=True,
        group="_Regulacion_prioridad",
        label="_RP_Señal_ceda_el_paso_horizontal",
        shortlabel="_RP_ceda_el_paso_horizontal"),
      Descriptor("PRIORI_MARCAS","Boolean", readOnly=True,
        group="_Regulacion_prioridad",
        label="_RP_Solo_marcas_viales",
        shortlabel="_RP_Marcas"),
      Descriptor("PRIORI_PEA_NO_ELEV","Boolean", readOnly=True,
        group="_Regulacion_prioridad",
        label="_RP_Paso_peatones_no_elevado",
        shortlabel="_RP_Paso_pea_no_elev"),
      Descriptor("PRIORI_PEA_ELEV","Boolean", readOnly=True,
        group="_Regulacion_prioridad",
        label="_RP_Paso_peatones_elevado",
        shortlabel="_RP_Paso_pea_elev"),
      Descriptor("PRIORI_MARCA_CICLOS","Boolean", readOnly=True,
        group="_Regulacion_prioridad",
        label="_RP_Paso_ciclistas",
        shortlabel="_RP_Paso_ciclistas"),
      Descriptor("PRIORI_CIRCUNSTANCIAL","Boolean", readOnly=True,
        group="_Regulacion_prioridad",
        label="_RP_Señalizacion_circunstancial",
        shortlabel="_RP_Circunstancial"),
      Descriptor("PRIORI_OTRA","Boolean", readOnly=True,
        group="_Regulacion_prioridad",
        label="_RP_Otra_señal",
        shortlabel="_RP_Otra"),

      Descriptor("TOTAL_VICTIMAS","Integer",
        label="_Total_victimas",
        shortlabel="_Victimas"),
      Descriptor("TOTAL_MUERTOS","Integer",
        label="_Total_muertos",
        shortlabel="_Muertos")\
        .set("DAL.Search.Attribute.Priority",10),
      Descriptor("TOTAL_GRAVES","Integer",
        label="_Total_graves",
        shortlabel="_Graves")\
        .set("DAL.Search.Attribute.Priority",11),
      Descriptor("TOTAL_LEVES","Integer",
        label="_Total_leves",
        shortlabel="_leves")\
        .set("DAL.Search.Attribute.Priority",12),
      Descriptor("TOTAL_ILESOS","Integer",
        label="_Total_ilesos",
        shortlabel="_Ilesos"),

      # Elementos de Balizamiento
      Descriptor("EB_PANELES_DIRECCIONALES","Boolean",
        label="_EB_Panels_direccionales",
        shortlabel="EB_Paneles"),
      Descriptor("EB_HITOS_ARISTA","Boolean",
        label="_EB_Hitos_arista",
        shortlabel="_EB_Hitos_arista"),
      Descriptor("EB_CAPTAFAROS","Boolean",
        label="_EB_Captafaros",
        shortlabel="_EB_Captafaros"),

      # Elementos de Separacion
      Descriptor("SEPARA_LINEA_LONG_SEPARACION","Boolean",
        label="_ES_Solo_linea_longitudinal",
        shortlabel="_ES_Linea_long"),
      Descriptor("SEPARA_CEBREADO","Boolean",
        label="_ES_Cebreado"),
      Descriptor("SEPARA_MEDIANA","Boolean",
        label="_ES_Mediana"),
      Descriptor("SEPARA_BARRERA_SEGURIDAD","Boolean",
        label="_ES_Barrera_de_seguridad",
        shortlabel="_ES_Barrera_seguridad"),
      Descriptor("SEPARA_ZONA_PEATONAL","Boolean",
        label="_ES_Zona_peatonal",
        shortlabel="_ES_Zona_peatonal"),
      Descriptor("SEPARA_OTRA_SEPARACION","Boolean",
        label="_ES_Otras"),
      Descriptor("SEPARA_NINGUNA_SEPARACION","Boolean",
        label="_ES_Ninguno"),

      Descriptor("BARRERA_SEG_LAT_ASC","Integer",group="_Barrera_seguridad"),
      Descriptor("BARRERA_SEG_LAT_ASC_MOTO","Boolean",group="_Barrera_seguridad"),
      Descriptor("BARRERA_SEG_LAT_DESC","Integer",group="_Barrera_seguridad"),
      Descriptor("BARRERA_SEG_LAT_DESC_MOTO","Boolean",group="_Barrera_seguridad"),
      Descriptor("BARRERA_SEG_MEDIANA_ASC","Integer",group="_Barrera_seguridad"),
      Descriptor("BARRERA_SEG_MEDIANA_ASC_MOTO","Boolean",group="_Barrera_seguridad"),
      Descriptor("BARRERA_SEG_MEDIANA_DESC","Integer",group="_Barrera_seguridad"),
      Descriptor("BARRERA_SEG_MEDIANA_DESC_MOTO","Boolean",group="_Barrera_seguridad"),

      Descriptor("TRAMO_PUENTE","Boolean",group="_Elementos_tramo"),
      Descriptor("TRAMO_TUNEL","Boolean",group="_Elementos_tramo"),
      Descriptor("TRAMO_PASO","Boolean",group="_Elementos_tramo"),
      Descriptor("TRAMO_ESTRECHA","Boolean",group="_Elementos_tramo"),
      Descriptor("TRAMO_RESALTOS","Boolean",group="_Elementos_tramo"),
      Descriptor("TRAMO_BADEN","Boolean",group="_Elementos_tramo"),
      Descriptor("TRAMO_APARTADERO","Boolean",group="_Elementos_tramo"),
      Descriptor("TRAMO_NINGUNA","Boolean",group="_Elementos_tramo"),

      Descriptor("INFLU_MARGEN","Boolean",group="_Caracteristicas_margen"),
      Descriptor("MARGEN_DESPEJADO","Boolean",group="_Caracteristicas_margen"),
      Descriptor("MARGEN_ARBOLES","Boolean",group="_Caracteristicas_margen"),
      Descriptor("MARGEN_OTROS_NATURALES","Boolean",group="_Caracteristicas_margen"),
      Descriptor("MARGEN_EDIFICIOS","Boolean",group="_Caracteristicas_margen"),
      Descriptor("MARGEN_POSTES","Boolean",group="_Caracteristicas_margen"),
      Descriptor("MARGEN_PUBLICIDAD","Boolean",group="_Caracteristicas_margen"),
      Descriptor("MARGEN_OTROS_ARTIFICIALES","Boolean",group="_Caracteristicas_margen"),
      Descriptor("MARGEN_OTROS_OBSTACULOS","Boolean",group="_Caracteristicas_margen"),
      Descriptor("MARGEN_DESC","Boolean",group="_Caracteristicas_margen"),

      Descriptor("INFLU_CIRCUNS_ESP","Boolean",group="_Circunstancias_especiales"),
      Descriptor("CIRCUNS_ESP_NINGUNA","Boolean",group="_Circunstancias_especiales"),
      Descriptor("CIRCUNS_ESP_CONOS","Boolean",group="_Circunstancias_especiales"),
      Descriptor("CIRCUNS_ESP_ZANJA","Boolean",group="_Circunstancias_especiales"),
      Descriptor("CIRCUNS_ESP_TAPA","Boolean",group="_Circunstancias_especiales"),
      Descriptor("CIRCUNS_ESP_OBRAS","Boolean",group="_Circunstancias_especiales"),
      Descriptor("CIRCUNS_ESP_OBSTACULO","Boolean",group="_Circunstancias_especiales"),
      Descriptor("CIRCUNS_ESP_DESPREND","Boolean",group="_Circunstancias_especiales"),
      Descriptor("CIRCUNS_ESP_ESCALON","Boolean",group="_Circunstancias_especiales"),
      Descriptor("CIRCUNS_ESP_FBACHES","Boolean",group="_Circunstancias_especiales"),
      Descriptor("CIRCUNS_ESP_FDETERIORADO","Boolean",group="_Circunstancias_especiales"),
      Descriptor("CIRCUNS_ESP_OTRAS","Boolean",group="_Circunstancias_especiales"),
      Descriptor("CIRCUNS_ESP_DESC","Boolean",group="_Circunstancias_especiales"),

      Descriptor("INFLU_DELIM_CALZADA","Boolean",group="_Delimitacion_calzada"),
      Descriptor("DELIM_CALZADA_BORDILLO","Boolean",group="_Delimitacion_calzada"),
      Descriptor("DELIM_CALZADA_VALLAS","Boolean",group="_Delimitacion_calzada"),
      Descriptor("DELIM_CALZADA_SETOS","Boolean",group="_Delimitacion_calzada"),
      Descriptor("DELIM_CALZADA_MARCAS","Boolean",group="_Delimitacion_calzada"),
      Descriptor("DELIM_CALZADA_BARRERA","Boolean",group="_Delimitacion_calzada"),
      Descriptor("DELIM_CALZADA_ISLETA","Boolean",group="_Delimitacion_calzada"),
      Descriptor("DELIM_CALZADA_PEATONAL","Boolean",group="_Delimitacion_calzada"),
      Descriptor("DELIM_CALZADA_OTRA","Boolean",group="_Delimitacion_calzada"),
      Descriptor("DELIM_CALZADA_SIN_DELIM","Boolean",group="_Delimitacion_calzada"),

      Descriptor("FC_CON_DISTRAIDA","Boolean",group="_Factores_concurrentes"),
      Descriptor("FC_VEL_INADECUADA","Boolean",group="_Factores_concurrentes"),
      Descriptor("FC_PRIORIDAD","Boolean",group="_Factores_concurrentes"),
      Descriptor("FC_SEGURIDAD","Boolean",group="_Factores_concurrentes"),
      Descriptor("FC_ADELANTAMIENTO","Boolean",group="_Factores_concurrentes"),
      Descriptor("FC_GIRO","Boolean",group="_Factores_concurrentes"),
      Descriptor("FC_CON_NEGLIGENTE","Boolean",group="_Factores_concurrentes"),
      Descriptor("FC_CON_TEMERARIA","Boolean",group="_Factores_concurrentes"),
      Descriptor("FC_IRRUPCION_ANIMAL","Boolean",group="_Factores_concurrentes"),
      Descriptor("FC_IRRUPCION_PEATON","Boolean",group="_Factores_concurrentes"),
      Descriptor("FC_ALCOHOL","Boolean",group="_Factores_concurrentes"),
      Descriptor("FC_DROGAS","Boolean",group="_Factores_concurrentes"),
      Descriptor("FC_ESTADO_VIA","Boolean",group="_Factores_concurrentes"),
      Descriptor("FC_METEORO","Boolean",group="_Factores_concurrentes"),
      Descriptor("FC_CANSANCIO","Boolean",group="_Factores_concurrentes"),
      Descriptor("FC_INEXPERIENCIA","Boolean",group="_Factores_concurrentes"),
      Descriptor("FC_AVERIA","Boolean",group="_Factores_concurrentes"),
      Descriptor("FC_OBRAS","Boolean",group="_Factores_concurrentes"),
      Descriptor("FC_MAL_ESTADO_VEHI","Boolean",group="_Factores_concurrentes"),
      Descriptor("FC_ENFERMEDAD","Boolean",group="_Factores_concurrentes"),
      Descriptor("FC_SENYALIZACION","Boolean",group="_Factores_concurrentes"),
      Descriptor("FC_OBSTACULO","Boolean",group="_Factores_concurrentes"),
      Descriptor("FC_OTRO_FACTOR","Boolean",group="_Factores_concurrentes"),

      Descriptor("VEHICULOS","List",group="_Vehiculos")\
        .relatedFeatures(
          "ARENA2_VEHICULOS",
          "LID_VEHICULO",
          ("ID_VEHICULO","NACIONALIDAD","TIPO_VEHICULO","MARCA_NOMBRE","MODELO"),
          "FEATURES('ARENA2_VEHICULOS',FORMAT('ID_ACCIDENTE = ''%s''',ID_ACCIDENTE))"
        )\
        .set("dynform.label.empty",True),
      Descriptor("PEATONES","List",group="_Peatones")\
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
          
  print Descriptor("TIPO_VIA","Integer", label="Tipo de via")\
          .selectablefk("ARENA2_DIC_TIPO_VIA")\
          
  print Descriptor("MAPA", "Geometry", hidden=True, 
        geomtype="Point:2D", 
        SRS="EPSG:4326", 
        expression="TRY ST_SetSRID(ST_Point(MAPAX,MAPAY),4326) EXCEPT NULL"
      )
  
