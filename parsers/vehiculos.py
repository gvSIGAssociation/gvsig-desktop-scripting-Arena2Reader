# encoding: utf-8

import gvsig

from org.gvsig.fmap.geom.aggregate import MultiPolygon
from org.gvsig.scripting.app.extension import ScriptingUtils
import xmltodic
from org.gvsig.fmap.geom import GeometryUtils

from util import sino2bool, null2empty, null2zero, get1, get2, Descriptor

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
      Descriptor("LID_VEHICULO","String",20,hidden=True, pk=True),
      Descriptor("ID_ACCIDENTE","String",20,label="Accidente")\
        .foreingkey("ARENA2_ACCIDENTES","ID_ACCIDENTE","FORMAT('%s',ID_ACCIDENTE)"),
      Descriptor("ID_VEHICULO","Integer", label="Cod.vehiculo"),

      
      Descriptor("SIN_CONDUCTOR","Boolean", label="Sin conducor"),
      Descriptor("LID_CONDUCTOR","String",20,label="Conductor")\
        .foreingkey("ARENA2_CONDUCTORES","LID_CONDUCTOR",
          "FORMAT('%02d %s %s %s',TOINTEGER(ID_VEHICULO), TOSTR(FECHA_NACIMIENTO), NACIONALIDAD, MUNICIPIO_RESIDENCIA)"),
        
      Descriptor("FECHA_MATRICULACION","Date",label="Fecha matriculacion"),
      Descriptor("NACIONALIDAD","String",100,label="Nacionalidad"),
      Descriptor("TIPO_VEHICULO","Integer", label="Tipo vehiculo")\
        .selectablefk("ARENA2_DIC_TIPO_VEHICULO"),
      Descriptor("MARCA_NOMBRE","String",100,label="Marca"),
      Descriptor("MODELO","String",100,label="Modelo"),
      Descriptor("ITV","Integer", label="ITV")\
        .selectablefk("ARENA2_DIC_ITV"),
      Descriptor("SEGURO","Integer", label="Seguro"),
      Descriptor("REMOLQUE","Boolean", label="Remolque"),
      Descriptor("SEMIREMOLQUE","Boolean", label="Semiremolque"),
      Descriptor("CARAVANA","Boolean", label="Carabana"),
      Descriptor("REMOLQUE_OTROS","Boolean", label="Otros remolques"),
      Descriptor("FACT_ANOMALIAS_PREVIAS","Boolean", group="Anomalias previas"),
      Descriptor("ANOMALIAS_NINGUNA","Boolean", group="Anomalias previas"),
      Descriptor("ANOMALIAS_NEUMATICOS","Boolean", group="Anomalias previas"),
      Descriptor("ANOMALIAS_REVENTON","Boolean", group="Anomalias previas"),
      Descriptor("ANOMALIAS_DIRECCION","Boolean", group="Anomalias previas"),
      Descriptor("ANOMALIAS_FRENOS","Boolean", group="Anomalias previas"),
      Descriptor("ANOMALIAS_OTRAS","Boolean", group="Anomalias previas"),
      Descriptor("MP","Boolean", label="Mercancias peligrosas"),
      Descriptor("VEHICULO_ADAPTADO","Boolean", label="Vehiculo adaptado"),
      Descriptor("NUM_OCUPANTES","Integer", label="Numero de ocupantes"),
      Descriptor("FUGADO","Boolean", label="Fugado"),
      Descriptor("INCENDIADO","Boolean", label="Incendiado"),
      Descriptor("TACOGRAFO_DISCO","Boolean"),
      Descriptor("AIRBAG_COND","Boolean", group="Airbag"),
      Descriptor("AIRBAG_PAS_DEL","Boolean", group="Airbag"),
      Descriptor("AIRBAG_ROD_IZDA","Boolean", group="Airbag"),
      Descriptor("AIRBAG_ROD_DCHA","Boolean", group="Airbag"),
      Descriptor("AIRBAG_LAT_DEL_IZDA","Boolean", group="Airbag"),
      Descriptor("AIRBAG_LAT_DEL_DCHA","Boolean", group="Airbag"),
      Descriptor("AIRBAG_CORT_DEL_IZDA","Boolean", group="Airbag"),
      Descriptor("AIRBAG_CORT_DEL_DCHA","Boolean", group="Airbag"),
      Descriptor("AIRBAG_LAT_TRAS_IZDA","Boolean", group="Airbag"),
      Descriptor("AIRBAG_LAT_TRAS_DCHA","Boolean", group="Airbag"),
      Descriptor("AIRBAG_CORT_TRAS_IZDA","Boolean", group="Airbag"),
      Descriptor("AIRBAG_CORT_TRAS_DCHA","Boolean", group="Airbag"),
      Descriptor("AIRBAG_OTROS","Boolean", group="Airbag"),
      Descriptor("AIRBAG_DESCONOCIDO","Boolean", group="Airbag"),
      Descriptor("TRANSPORTE_ESPECIAL","Boolean", label="Transporte especial"),
      Descriptor("DANYOS","Integer", label="Da\xf1os")\
        .selectablefk("ARENA2_DIC_DANYOS"),
      Descriptor("POS_VIA","Integer")\
        .selectablefk("ARENA2_DIC_POSICION_VIA"),
      Descriptor("APROXIMACION_NUDO","Integer")\
        .selectablefk("ARENA2_DIC_NUDO_APROX"),
      Descriptor("SENTIDO_CIRCULACION","Integer")\
        .selectablefk("ARENA2_DIC_SENTIDO_CIRCULA"),
      Descriptor("LUGAR_CIRCULABA","Integer")\
        .selectablefk("ARENA2_DIC_LUGAR_CIRCULA"),
      Descriptor("FACT_LUGAR_CIRCULA","Boolean"),

      Descriptor("PASAJEROS","List",group="Pasajeros")\
        .relatedFeatures(
          "ARENA2_PASAJEROS",
          "LID_PASAJERO",
          ("ID_PASAJERO","FECHA_NACIMIENTO","SEXO","PAIS_RESIDENCIA","PROVINCIA_RESIDENCIA","MUNICIPIO_RESIDENCIA"),
          "FEATURES('ARENA2_PASAJEROS',FORMAT('LID_VEHICULO = ''%s''',LID_VEHICULO))"
        )\
        .set("dynform.label.empty",True)
    ]
    return columns

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
