# encoding: utf-8

import gvsig

from org.gvsig.fmap.geom.aggregate import MultiPolygon
from org.gvsig.scripting.app.extension import ScriptingUtils
import xmltodic
from org.gvsig.fmap.geom import GeometryUtils

from util import sino2bool, null2empty, null2zero, get1, get2

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
    columns = [
      "LID_VEHICULO:String:set:size=20:set:hidden=true",
      "ID_ACCIDENTE:String:set:size=20:set:label=Accidente:set:profile=DAL.ForeingKey:tag:DAL.foreingTable=ARENA2_ACCIDENTES:tag:DAL.foreingCode=ID_ACCIDENTE:tag:DAL.foreingLabel=FORMAT('%s',ID_ACCIDENTE)",
      "ID_VEHICULO:Integer:set:label=Cod. vehiculo",
      "SIN_CONDUCTOR:Boolean:set:label=Sin conducor",
      "LID_CONDUCTOR:String:set:size=20:set:label=Conductor:set:profile=DAL.ForeingKey:tag:DAL.foreingTable=ARENA2_CONDUCTORES:tag:DAL.foreingCode=LID_CONDUCTOR:tag:DAL.foreingLabel=FORMAT('%02d %s %s %s',TOINTEGER(ID_VEHICULO), TOSTR(FECHA_NACIMIENTO), NACIONALIDAD, MUNICIPIO_RESIDENCIA)",
      "FECHA_MATRICULACION:Date:set:label=Fecha matriculacion",
      "NACIONALIDAD:String:set:size=100:set:label=Nacionalidad",
      "TIPO_VEHICULO:Integer:set:label=Tipo vehiculo:set:profile=DAL.SelectableForeingKey:tag:DAL.foreingTable=ARENA2_TIPO_VEHICULO:tag:DAL.foreingCode=ID:tag:DAL.foreingLabel=FORMAT('%02d - %s',ID,DESCRIPCION)",
      "MARCA_NOMBRE:String:set:size=100:set:label=Marca",
      "MODELO:String:set:size=100:set:label=Modelo",
      "ITV:Integer:set:label=ITV:set:profile=DAL.SelectableForeingKey:tag:DAL.foreingTable=ARENA2_ITV:tag:DAL.foreingCode=ID:tag:DAL.foreingLabel=FORMAT('%02d - %s',ID,DESCRIPCION)",
      "SEGURO:Integer:set:label=Seguro",
      "REMOLQUE:Boolean:set:label=Remolque",
      "SEMIREMOLQUE:Boolean:set:label=Semiremolque",
      "CARAVANA:Boolean:set:label=Carabana",
      "REMOLQUE_OTROS:Boolean:set:label=Otros remolques",
      "FACT_ANOMALIAS_PREVIAS:Boolean:set:group=Anomalias previas",
      "ANOMALIAS_NINGUNA:Boolean:set:group=Anomalias previas",
      "ANOMALIAS_NEUMATICOS:Boolean:set:group=Anomalias previas",
      "ANOMALIAS_REVENTON:Boolean:set:group=Anomalias previas",
      "ANOMALIAS_DIRECCION:Boolean:set:group=Anomalias previas",
      "ANOMALIAS_FRENOS:Boolean:set:group=Anomalias previas",
      "ANOMALIAS_OTRAS:Boolean:set:group=Anomalias previas",
      "MP:Boolean:set:label=Mercancias peligrosas",
      "VEHICULO_ADAPTADO:Boolean:set:label=Vehiculo adaptado",
      "NUM_OCUPANTES:Integer:set:label=Numero de ocupantes",
      "FUGADO:Boolean:set:label=Fugado",
      "INCENDIADO:Boolean:set:label=Incendiado",
      "TACOGRAFO_DISCO:Boolean",
      "AIRBAG_COND:Boolean:set:group=Airbag",
      "AIRBAG_PAS_DEL:Boolean:set:group=Airbag",
      "AIRBAG_ROD_IZDA:Boolean:set:group=Airbag",
      "AIRBAG_ROD_DCHA:Boolean:set:group=Airbag",
      "AIRBAG_LAT_DEL_IZDA:Boolean:set:group=Airbag",
      "AIRBAG_LAT_DEL_DCHA:Boolean:set:group=Airbag",
      "AIRBAG_CORT_DEL_IZDA:Boolean:set:group=Airbag",
      "AIRBAG_CORT_DEL_DCHA:Boolean:set:group=Airbag",
      "AIRBAG_LAT_TRAS_IZDA:Boolean:set:group=Airbag",
      "AIRBAG_LAT_TRAS_DCHA:Boolean:set:group=Airbag",
      "AIRBAG_CORT_TRAS_IZDA:Boolean:set:group=Airbag",
      "AIRBAG_CORT_TRAS_DCHA:Boolean:set:group=Airbag",
      "AIRBAG_OTROS:Boolean:set:group=Airbag",
      "AIRBAG_DESCONOCIDO:Boolean:set:group=Airbag",
      "TRANSPORTE_ESPECIAL:Boolean:set:label=Transporte especial",
      "DANYOS:Integer:set:label=Da\xf1os:set:profile=DAL.SelectableForeingKey:tag:DAL.foreingTable=ARENA2_DANYOS:tag:DAL.foreingCode=ID:tag:DAL.foreingLabel=FORMAT('%02d - %s',ID,DESCRIPCION)",
      "POS_VIA:Integer:set:profile=DAL.SelectableForeingKey:tag:DAL.foreingTable=ARENA2_POSICION_VIA:tag:DAL.foreingCode=ID:tag:DAL.foreingLabel=FORMAT('%02d - %s',ID,DESCRIPCION)",
      "APROXIMACION_NUDO:Integer:set:profile=DAL.SelectableForeingKey:tag:DAL.foreingTable=ARENA2_NUDO_APROX:tag:DAL.foreingCode=ID:tag:DAL.foreingLabel=FORMAT('%02d - %s',ID,DESCRIPCION)",
      "SENTIDO_CIRCULACION:Integer:set:profile=DAL.SelectableForeingKey:tag:DAL.foreingTable=ARENA2_SENTIDO_CIRCULA:tag:DAL.foreingCode=ID:tag:DAL.foreingLabel=FORMAT('%02d - %s',ID,DESCRIPCION)",
      "LUGAR_CIRCULABA:Integer:set:profile=DAL.SelectableForeingKey:tag:DAL.foreingTable=ARENA2_LUGAR_CIRCULA:tag:DAL.foreingCode=ID:tag:DAL.foreingLabel=FORMAT('%02d - %s',ID,DESCRIPCION)",
      "FACT_LUGAR_CIRCULA:Boolean",
      "PASAJEROS:List:set:group=Pasajeros:set:profile=DAL.Features:set:expression=FEATURES('ARENA2_PASAJEROS',FORMAT('LID_VEHICULO = ''%s''',LID_VEHICULO)):tag:dynform.label.empty=true:tag:DAL.features.columns=ID_PASAJERO/FECHA_NACIMIENTO/SEXO/PAIS_RESIDENCIA/PROVINCIA_RESIDENCIA/MUNICIPIO_RESIDENCIA:tag:DAL.features.tableName=ARENA2_PASAJEROS:tag:DAL.features.codeName=LID_PASAJERO"
    ]
    return columns

  def getRowCount(self):
    self.rewind()
    rowCount = 0
    while True:
      row = self.next()
      if row == None:
        return rowCount;
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
      get1(vehiculo,"MARCA_NOMBRE"),
      get1(vehiculo,"MODELO"),
      null2zero(get1(vehiculo,"ITV")),
      null2zero(get1(vehiculo,"SEGURO")),
      sino2bool(get1(vehiculo,"REMOLQUE")),
      sino2bool(get1(vehiculo,"SEMIREMOLQUE")),
      sino2bool(get1(vehiculo,"CARAVANA")),
      sino2bool(get1(vehiculo,"REMOLQUE_OTROS")),
      sino2bool(get2(vehiculo,"ANOMALIAS_PREVIAS","@FACT_ANOMALIAS_PREVIAS")),
      sino2bool(get2(vehiculo,"ANOMALIAS_PREVIAS","ANOMALIAS_NINGUNA")),
      sino2bool(get2(vehiculo,"ANOMALIAS_PREVIAS","ANOMALIAS_NEUMATICOS")),
      sino2bool(get2(vehiculo,"ANOMALIAS_PREVIAS","ANOMALIAS_REVENTON")),
      sino2bool(get2(vehiculo,"ANOMALIAS_PREVIAS","ANOMALIAS_DIRECCION")),
      sino2bool(get2(vehiculo,"ANOMALIAS_PREVIAS","ANOMALIAS_FRENOS")),
      sino2bool(get2(vehiculo,"ANOMALIAS_PREVIAS","ANOMALIAS_OTRAS")),
      sino2bool(get2(vehiculo,"MERCANCIAS_PELIGROSAS","MP")),
      sino2bool(get1(vehiculo,"VEHICULO_ADAPTADO")),
      null2zero(get1(vehiculo,"NUM_OCUPANTES")),
      sino2bool(get1(vehiculo,"FUGADO")),
      sino2bool(get1(vehiculo,"INCENDIADO")),
      sino2bool(get1(vehiculo,"TACOGRAFO_DISCO")),
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
      sino2bool(get1(vehiculo,"TRANSPORTE_ESPECIAL")),
      null2zero(get1(vehiculo,"DANYOS")),
      null2zero(get1(vehiculo,"POS_VIA")),
      null2zero(get1(vehiculo,"APROXIMACION_NUDO")),
      null2zero(get1(vehiculo,"SENTIDO_CIRCULACION")),
      null2zero(get2(vehiculo,"LUGAR_CIRCULABA","#test")),
      sino2bool(get2(vehiculo,"LUGAR_CIRCULABA","@FACT_LUGAR_CIRCULA")),
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
