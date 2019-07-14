# encoding: utf-8

import gvsig

from org.gvsig.fmap.geom.aggregate import MultiPolygon
from org.gvsig.scripting.app.extension import ScriptingUtils
import xmltodic
from org.gvsig.fmap.geom import GeometryUtils

from util import sino2bool, null2empty, null2zero, get1, get2, Descriptor, generate_translations

COLUMNS_DEFINITION = [
  Descriptor("LID_VEHICULO","String",20,hidden=True, pk=True,
    label="_ID_vehiculo"),
  Descriptor("ID_ACCIDENTE","String",20,
    label="_Accidente")\
    .foreingkey("ARENA2_ACCIDENTES","ID_ACCIDENTE","FORMAT('%s',ID_ACCIDENTE)")\
    .tag("dynform.readonly",True),
  Descriptor("ID_VEHICULO","Integer", 
    label="_Cod_vehiculo")\
    .tag("dynform.readonly",True),

  Descriptor("SIN_CONDUCTOR","Boolean", 
    label="_Sin_conducor")\
    .tag("dynform.readonly",True),
  Descriptor("LID_CONDUCTOR","String",20,
    label="_Conductor")\
    .foreingkey(
      "ARENA2_CONDUCTORES",
      "LID_CONDUCTOR",
      "FORMAT('%02d %s %s %s',TOINTEGER(ID_VEHICULO), TOSTR(FECHA_NACIMIENTO), NACIONALIDAD, MUNICIPIO_RESIDENCIA)")\
    .tag("dynform.readonly",True),
    
  Descriptor("FECHA_MATRICULACION","Date",
    label="_Fecha_matriculacion")\
    .tag("dynform.readonly",True),
  Descriptor("NACIONALIDAD","String",100,
    label="_Nacionalidad")\
    .tag("dynform.readonly",True),
  Descriptor("TIPO_VEHICULO","Integer", 
    label="_Tipo_vehiculo")\
    .closedlistfk("ARENA2_DIC_TIPO_VEHICULO")\
    .tag("dynform.dropdown","label")\
    .tag("dynform.readonly",True),
  Descriptor("MMA","Integer",
    label="_MMA")\
    .closedlistfk("ARENA2_DIC_MMA")\
    .tag("dynform.readonly",True),
  Descriptor("MARCA_NOMBRE","String",100,
    label="_Marca")\
    .tag("dynform.readonly",True),
  Descriptor("MODELO","String",100,
    label="_Modelo")\
    .tag("dynform.readonly",True),
  Descriptor("ITV","Integer", 
    label="_ITV")\
    .closedlistfk("ARENA2_DIC_ITV")\
    .tag("dynform.readonly",True),
  Descriptor("SEGURO","Integer", 
    label="_Seguro")\
    .closedlistfk("ARENA2_DIC_GENERICO2")\
    .tag("dynform.readonly",True),
  Descriptor("NUM_OCUPANTES","Integer", 
    label="_Numero_de_ocupantes",
    shortlabel="_Acupantes")\
    .tag("dynform.readonly",True),
  Descriptor("VEHICULO_ADAPTADO","Boolean", 
    label="_Vehiculo_adaptado",
    shortlabel="_Adaptado")\
    .tag("dynform.readonly",True),
  Descriptor("TRANSPORTE_ESPECIAL","Boolean", 
    label="_Transporte_especial",
    shortlabel="_Trans_especial")\
    .tag("dynform.readonly",True),
  
  Descriptor("FUGADO","Boolean", 
    label="_Fugado")\
    .tag("dynform.readonly",True),
  Descriptor("INCENDIADO","Boolean", 
    label="_Incendiado")\
    .tag("dynform.readonly",True),
    
  Descriptor("MP","Boolean", 
    label="_Mercancias_peligrosas",
    shortlabel="_Merc_peligrosos")\
    .tag("dynform.readonly",True),
  Descriptor("MP_NUMERO_ONU","Integer", 
    label="_MP_Numero_ONU",
    shortlabel="_MP_ONU")\
    .closedlistfk("ARENA2_DIC_ONU",code="ID", label="FORMAT('%02d - %s',CODIGO,DESCRIPCION)")\
    .tag("dynform.readonly",True),

  Descriptor("DANYOS","Integer", 
    label="_Danyos")\
    .closedlistfk("ARENA2_DIC_DANYOS")\
    .tag("dynform.readonly",True),
    
  # -- SECCION "Remolque"
  Descriptor("REMOLQUE","Boolean", 
    label="_Remolque")\
    .tag("dynform.readonly",True)\
    .tag("dynform.separator","_Remolque"),
  Descriptor("SEMIREMOLQUE","Boolean", 
    label="_Semiremolque")\
    .tag("dynform.readonly",True),
  Descriptor("CARAVANA","Boolean", 
    label="_Carabana")\
    .tag("dynform.readonly",True),
  Descriptor("REMOLQUE_OTROS","Boolean", 
    label="_Otros_remolques")\
    .tag("dynform.readonly",True),

  # -- SECCION "Posicion en la via"
  Descriptor("POS_VIA","Integer",
    label="_Posicion_en_la_via",
    shortlabel="_Posicion_via")\
    .tag("dynform.separator","_Posicion_en_la_via")\
    .closedlistfk("ARENA2_DIC_POSICION_VIA")\
    .tag("dynform.readonly",True),
  Descriptor("APROXIMACION_NUDO","Integer",
    label="_Aproximacion_a_nudo",
    shortlabel="_Aprox_nudo")\
    .closedlistfk("ARENA2_DIC_NUDO_APROX")\
    .tag("dynform.readonly",True),
  Descriptor("SENTIDO_CIRCULACION","Integer",
    label="_Sentido_de_la_circulacion",
    shortlabel="_Sentido_circulacion")\
    .closedlistfk("ARENA2_DIC_SENTIDO_CIRCULA")\
    .tag("dynform.readonly",True),
  Descriptor("LUGAR_CIRCULABA","Integer",
    label="_Lugar_por_el_que_circulaba",
    shortlabel="_Lugar_circulaba")\
    .closedlistfk("ARENA2_DIC_LUGAR_CIRCULA")\
    .tag("dynform.dropdown","label")\
    .tag("dynform.readonly",True),
  Descriptor("FACT_LUGAR_CIRCULA","Boolean",
    label="_Influye_el_lugar_por_el_que_circulaba",
    shortlabel="_Influye_lugar_circulaba")\
    .tag("dynform.readonly",True),

  # -- GRUPO "Tacografo"
  Descriptor("TACOGRAFO_DISCO","Boolean",
    label="_Disco_tacografo",
    shortlabel="_Tacografo",
    group="_Tacografo")\
    .tag("dynform.readonly",True),
  Descriptor("TACOGRAFO_LECTURA","Boolean",
    label="_Lectura_tacografo",
    shortlabel="_Lect_tacografo",
    group="_Tacografo")\
    .tag("dynform.readonly",True),
  Descriptor("DESCANSO_DIARIO","Boolean",
    label="_Respetado_el_descanso_diario",
    shortlabel="_Descanso_diario",
    group="_Tacografo")\
    .tag("dynform.readonly",True),
  Descriptor("HORAS_COND_CONTINU_SUP","Boolean",
    label="_Superadas_horas_conduccion_continuada",
    shortlabel="_horas_cond_continuada",
    group="_Tacografo")\
    .tag("dynform.readonly",True),
  Descriptor("HORAS_COND_DIARIA_SUP","Boolean",
    label="_Superadas_horas_de_conduccion_diaria",
    shortlabel="_horas_cond_diarias",
    group="_Tacografo")\
    .tag("dynform.readonly",True),
  Descriptor("HORAS_COND_CONTINUADAS_H","Integer",
    label="_Conduccion_continuada_horas",
    shortlabel="_cond_continuada_h",
    group="_Tacografo")\
    .tag("dynform.readonly",True),
  Descriptor("HORAS_COND_CONTINUADAS_MIN","Integer",
    label="_Conduccion_continuada_min",
    shortlabel="_cond_continuada_m",
    group="_Tacografo")\
    .tag("dynform.readonly",True),


  # -- GRUPO "Anomalias previas"
  Descriptor("FACT_ANOMALIAS_PREVIAS","Boolean", 
    label="_Influyen_las_anomalias_previas",
    shortlabel="_Influyen_anomalias",
    group="_Anomalias_previas")\
    .tag("dynform.readonly",True),
  Descriptor("ANOMALIAS_NINGUNA","Boolean", 
    label="_AP_Aparentemente_ninguna",
    shortlabel="_AP_Ninguna",
    group="_Anomalias_previas")\
    .tag("dynform.readonly",True),
  Descriptor("ANOMALIAS_NEUMATICOS","Boolean", 
    label="_AP_Neumaticos_desgastados_o_defectuosos",
    shortlabel="_AP_Neumaticos",
    group="_Anomalias_previas")\
    .tag("dynform.readonly",True),
  Descriptor("ANOMALIAS_REVENTON","Boolean", 
    label="_AP_Reventon",
    shortlabel="_AP_Reventon",
    group="_Anomalias_previas")\
    .tag("dynform.readonly",True),
  Descriptor("ANOMALIAS_DIRECCION","Boolean", 
    label="_AP_Direccion",
    shortlabel="_AP_Direccion",
    group="_Anomalias_previas")\
    .tag("dynform.readonly",True),
  Descriptor("ANOMALIAS_FRENOS","Boolean", 
    label="_AP_Frenos",
    shortlabel="_AP_Frenos",
    group="_Anomalias_previas")\
    .tag("dynform.readonly",True),
  Descriptor("ANOMALIAS_OTRAS","Boolean", 
    label="_AP_Otras",
    shortlabel="_AP_Otras",
    group="_Anomalias_previas")\
    .tag("dynform.readonly",True),
  Descriptor("ANOMALIAS_OTRA","String", 
    label="_AP_Otra",
    shortlabel="_AP_Otra",
    group="_Anomalias_previas")\
    .tag("dynform.readonly",True),

  # -- GRUPO "Airbag disparado"
  Descriptor("AIRBAG_COND","Boolean", 
    label="_AB_Frontal_del_conductor",
    shortlabel="_AB_Conductor",
    group="_Airbag_disparado")\
    .tag("dynform.readonly",True),
  Descriptor("AIRBAG_PAS_DEL","Boolean", 
    label="_AB_Frontal_pasajero_delantero",
    shortlabel="_AB_pas_del",
    group="_Airbag_disparado")\
    .tag("dynform.readonly",True),
  Descriptor("AIRBAG_ROD_IZDA","Boolean", 
    label="_AB_Frontal_Rodilla_izquierdo",
    shortlabel="_AB_Rod_izq",
    group="_Airbag_disparado")\
    .tag("dynform.readonly",True),
  Descriptor("AIRBAG_ROD_DCHA","Boolean", 
    label="_AB_Rodilla_derecho",
    shortlabel="_AB_Rod_der",
    group="_Airbag_disparado")\
    .tag("dynform.readonly",True),
  Descriptor("AIRBAG_LAT_DEL_IZDA","Boolean", 
    label="_AB_Lateral_delantero_izquierdo",
    shortlabel="_AB_Lat_del_izq",
    group="_Airbag_disparado")\
    .tag("dynform.readonly",True),
  Descriptor("AIRBAG_LAT_DEL_DCHA","Boolean", 
    label="_AB_Lateral_delantero_derecho",
    shortlabel="_AB_Lat_del_der",
    group="_Airbag_disparado")\
    .tag("dynform.readonly",True),
  Descriptor("AIRBAG_CORT_DEL_IZDA","Boolean", 
    label="_AB_Cortina_delantero_izquierdo",
    shortlabel="_AB_Cort_del_izq",
    group="_Airbag_disparado")\
    .tag("dynform.readonly",True),
  Descriptor("AIRBAG_CORT_DEL_DCHA","Boolean", 
    label="_AB_Cortina_delantero_derecho",
    shortlabel="_AB_Cort_del_der",
    group="_Airbag_disparado")\
    .tag("dynform.readonly",True),
  Descriptor("AIRBAG_LAT_TRAS_IZDA","Boolean", 
    label="_AB_Lateral_trasero_izquierdo",
    shortlabel="_AB_Lat_tras_izq",
    group="_Airbag_disparado")\
    .tag("dynform.readonly",True),
  Descriptor("AIRBAG_LAT_TRAS_DCHA","Boolean", 
    label="_AB_Lateral_trasero_derecho",
    shortlabel="_AB_Lat_tras_der",
    group="_Airbag_disparado")\
    .tag("dynform.readonly",True),
  Descriptor("AIRBAG_CORT_TRAS_IZDA","Boolean", 
    label="_AB_Cortina_trasero_izquierdo",
    shortlabel="_AB_Cort_tras_izq",
    group="_Airbag_disparado")\
    .tag("dynform.readonly",True),
  Descriptor("AIRBAG_CORT_TRAS_DCHA","Boolean", 
    label="_AB_Cortina_trasero_derecho",
    shortlabel="_AB_Cort_tras_der",
    group="_Airbag_disparado")\
    .tag("dynform.readonly",True),
  Descriptor("AIRBAG_OTROS","Boolean", 
    label="_AB_Otros",
    shortlabel="_AB_Otros",
    group="_Airbag_disparado")\
    .tag("dynform.readonly",True),
  Descriptor("AIRBAG_DESCONOCIDO","Boolean", 
    label="_AB_Se_desconoce",
    shortlabel="_AB_desconocido",
    group="_Airbag_disparado")\
    .tag("dynform.readonly",True),

  
  Descriptor("PASAJEROS","List",
    group="_Pasajeros")\
    .relatedFeatures(
      "ARENA2_PASAJEROS",
      "LID_PASAJERO",
      ("ID_PASAJERO","FECHA_NACIMIENTO","SEXO","PAIS_RESIDENCIA","PROVINCIA_RESIDENCIA","MUNICIPIO_RESIDENCIA"),
      "FEATURES('ARENA2_PASAJEROS',FORMAT('LID_VEHICULO = ''%s''',LID_VEHICULO))"
    )\
    .tag("dynform.label.empty",True)
]

class VehiculosParser(object):
  
  def __init__(self, fname, xml=None):
    self.fname = fname
    self.xml = xml
    self.informeCorriente = None
    self.accidenteCorriente = None
    self.vehiculoCorriente = None

  def getXML(self):
    return self.xml
    
  def open(self):
    if self.xml == None :
      fileXml = open(self.fname,"r")
      data = fileXml.read()
      fileXml.close()
      self.xml = xmltodic.parse(data)
    
    self.informeCorriente = 0
    self.rewind()
  
  def rewind(self):
    self.informeCorriente = 0
    self.accidenteCorriente = 0
    self.vehiculoCorriente = 0
  
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

  def getVehiculos(self, accidente):
    vehiculos = accidente["VEHICULOS"]['VEHICULO']
    if not isinstance(vehiculos,list):
      vehiculos = [ vehiculos ]
    return vehiculos

  def getColumns(self):
    return COLUMNS_DEFINITION

  def getRowCount(self):
    self.rewind()
    rowCount = 0
    while True:
      row = self.next()
      if row == None:
        return rowCount
      rowCount+=1

  def read(self):
    vehiculo = self.next()
    if vehiculo == None:
      return None

    values = [
      get1(vehiculo,"@ID_ACCIDENTE") +"/"+ get1(vehiculo,"@ID_VEHICULO"),
      get1(vehiculo,"@ID_ACCIDENTE"),
      
      get1(vehiculo,"@ID_VEHICULO"),
      sino2bool(get1(vehiculo,"SIN_CONDUCTOR")),
      get1(vehiculo,"@ID_ACCIDENTE") +"/"+ get1(vehiculo,"@ID_VEHICULO"),
      
      get1(vehiculo,"FECHA_MATRICULACION"),
      get1(vehiculo,"NACIONALIDAD"),
      null2zero(get1(vehiculo,"TIPO_VEHICULO")),
      null2zero(get1(vehiculo,"MMA")),
      get1(vehiculo,"MARCA_NOMBRE"),
      get1(vehiculo,"MODELO"),
      null2zero(get1(vehiculo,"ITV")),
      null2zero(get1(vehiculo,"SEGURO")),
      null2zero(get1(vehiculo,"NUM_OCUPANTES")),
      sino2bool(get1(vehiculo,"VEHICULO_ADAPTADO")),
      sino2bool(get1(vehiculo,"TRANSPORTE_ESPECIAL")),

      sino2bool(get1(vehiculo,"FUGADO")),
      sino2bool(get1(vehiculo,"INCENDIADO")),
      
      sino2bool(get2(vehiculo,"MERCANCIAS_PELIGROSAS","MP")),
      null2zero(get2(vehiculo,"MERCANCIAS_PELIGROSAS","MP_NUMERO_ONU")),
      
      null2zero(get1(vehiculo,"DANYOS")),

      sino2bool(get1(vehiculo,"REMOLQUE")),
      sino2bool(get1(vehiculo,"SEMIREMOLQUE")),
      sino2bool(get1(vehiculo,"CARAVANA")),
      sino2bool(get1(vehiculo,"REMOLQUE_OTROS")),
      
      null2zero(get1(vehiculo,"POS_VIA")),
      null2zero(get1(vehiculo,"APROXIMACION_NUDO")),
      null2zero(get1(vehiculo,"SENTIDO_CIRCULACION")),
      null2zero(get2(vehiculo,"LUGAR_CIRCULABA","#test")),
      sino2bool(get2(vehiculo,"LUGAR_CIRCULABA","@FACT_LUGAR_CIRCULA")),

      sino2bool(get1(vehiculo,"TACOGRAFO_DISCO")),
      sino2bool(get1(vehiculo,"TACOGRAFO_LECTURA")),
      sino2bool(get1(vehiculo,"DESCANSO_DIARIO")),
      sino2bool(get1(vehiculo,"HORAS_COND_CONTINU_SUP")),
      sino2bool(get1(vehiculo,"HORAS_COND_DIARIA_SUP")),
      null2zero(get1(vehiculo,"HORAS_COND_CONTINUADAS_H")),
      null2zero(get1(vehiculo,"HORAS_COND_CONTINUADAS_MIN")),

      sino2bool(get2(vehiculo,"ANOMALIAS_PREVIAS","@FACT_ANOMALIAS_PREVIAS")),
      sino2bool(get2(vehiculo,"ANOMALIAS_PREVIAS","ANOMALIAS_NINGUNA")),
      sino2bool(get2(vehiculo,"ANOMALIAS_PREVIAS","ANOMALIAS_NEUMATICOS")),
      sino2bool(get2(vehiculo,"ANOMALIAS_PREVIAS","ANOMALIAS_REVENTON")),
      sino2bool(get2(vehiculo,"ANOMALIAS_PREVIAS","ANOMALIAS_DIRECCION")),
      sino2bool(get2(vehiculo,"ANOMALIAS_PREVIAS","ANOMALIAS_FRENOS")),
      sino2bool(get2(vehiculo,"ANOMALIAS_PREVIAS","ANOMALIAS_OTRAS")),
      get2(vehiculo,"ANOMALIAS_PREVIAS","ANOMALIAS_OTRA"),
      
      sino2bool(get2(vehiculo,"AIRBAG","AIRBAG_COND")),
      sino2bool(get2(vehiculo,"AIRBAG","AIRBAG_PAS_DEL")),
      sino2bool(get2(vehiculo,"AIRBAG","AIRBAG_ROD_IZDA")),
      sino2bool(get2(vehiculo,"AIRBAG","AIRBAG_ROD_DCHA")),
      sino2bool(get2(vehiculo,"AIRBAG","AIRBAG_LAT_DEL_IZDA")),
      sino2bool(get2(vehiculo,"AIRBAG","AIRBAG_LAT_DEL_DCHA")),
      sino2bool(get2(vehiculo,"AIRBAG","AIRBAG_CORT_DEL_IZDA")),
      sino2bool(get2(vehiculo,"AIRBAG","AIRBAG_CORT_DEL_DCHA")),
      sino2bool(get2(vehiculo,"AIRBAG","AIRBAG_LAT_TRAS_IZDA")),
      sino2bool(get2(vehiculo,"AIRBAG","AIRBAG_LAT_TRAS_DCHA")),
      sino2bool(get2(vehiculo,"AIRBAG","AIRBAG_CORT_TRAS_IZDA")),
      sino2bool(get2(vehiculo,"AIRBAG","AIRBAG_CORT_TRAS_DCHA")),
      sino2bool(get2(vehiculo,"AIRBAG","AIRBAG_OTROS")),
      sino2bool(get2(vehiculo,"AIRBAG","AIRBAG_DESCONOCIDO")),
      None # Pasajeros
    ]
    return values

  def next(self):
    if self.informeCorriente == None:
      return None
    
    informes = self.getInformes()
    while self.informeCorriente < len(informes):
      informe = informes[self.informeCorriente]
      #print "Informe: ", get1(informe,"@COD_INFORME"), self.informeCorriente
      accidentes = self.getAccidentes(informe)
      while self.accidenteCorriente < len(accidentes):
        accidente = accidentes[self.accidenteCorriente]
        #print "Accidente: ", get1(accidente,"@ID_ACCIDENTE"), self.accidenteCorriente
        vehiculos = self.getVehiculos(accidente)
        if self.vehiculoCorriente < len(vehiculos) :
          vehiculo = vehiculos[self.vehiculoCorriente]
          #print "Vehiculo: ", get1(vehiculo,"@ID_ACCIDENTE")+"/"+get1(vehiculo,"@ID_VEHICULO"), self.vehiculoCorriente
          self.vehiculoCorriente += 1
          return vehiculo
        self.accidenteCorriente += 1
        self.vehiculoCorriente = 0

      self.informeCorriente += 1
      self.accidenteCorriente = 0
      self.vehiculoCorriente = 0

    self.informeCorriente = None
    return None


def main(*args):
  generate_translations(COLUMNS_DEFINITION)
  
