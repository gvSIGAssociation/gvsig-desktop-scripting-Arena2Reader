# encoding: utf-8

import gvsig

from org.gvsig.fmap.geom.aggregate import MultiPolygon
from org.gvsig.scripting.app.extension import ScriptingUtils
import xmltodic
from org.gvsig.fmap.geom import GeometryUtils

from util import sino2bool, null2empty, null2zero, get1, get2, Descriptor

class PasajerosParser(object):
  
  def __init__(self, fname, xml=None):
    self.fname = fname
    self.xml = xml
    self.informeCorriente = None
    self.accidenteCorriente = None
    self.vehiculoCorriente = None
    self.pasajeroCorriente = None

  def getXML(self):
    return self.xml
    
  def open(self):
    if self.xml == None :
      fileXml = open(self.fname,"r")
      data = fileXml.read()
      fileXml.close()
      self.xml = xmltodic.parse(data)
    
    self.rewind()
  
  def rewind(self):
    self.informeCorriente = 0
    self.accidenteCorriente = 0
    self.vehiculoCorriente = 0
    self.pasajeroCorriente = 0
  
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

  def getPasajeros(self, vehiculo):
    try:
      pasajeros = vehiculo["PASAJEROS"]['PASAJERO']
      if not isinstance(pasajeros,list):
        pasajeros = [ pasajeros ]
      return pasajeros
    except: # Si no hay pasajeros da error; devolvemos una lista vacia
      return list()

  def getColumns(self):
    columns = [
      Descriptor("LID_PASAJERO","String",20,hidden=True, pk=True),
      Descriptor("ID_ACCIDENTE","String",20,label="Accidente")\
        .foreingkey("ARENA2_ACCIDENTES","ID_ACCIDENTE","FORMAT('%s',ID_ACCIDENTE)"),
      Descriptor("LID_VEHICULO","String",20,label="Vehiculo")\
        .foreingkey("ARENA2_VEHICULOS","LID_VEHICULO","FORMAT('%s/%s %s %s %s %s',ID_ACCIDENTE,ID_VEHICULO,TIPO_VEHICULO,NACIONALIDAD,MARCA_NOMBRE,MODELO)"),
      Descriptor("ID_VEHICULO","String",5, hidden=True),
      Descriptor("ID_PASAJERO","Integer", label="Cod.pasajero"),
      
      Descriptor("FECHA_NACIMIENTO","Date",label="Fecha nacimiento"),
      Descriptor("SEXO","Integer",label="Sexo")\
        .selectablefk("ARENA2_DIC_SEXO"),
      Descriptor("PAIS_RESIDENCIA","String", size=100,label="Pais de residencia"),
      Descriptor("PROVINCIA_RESIDENCIA","String", size=100,label="Provincia de residencia"),
      Descriptor("MUNICIPIO_RESIDENCIA","String", size=100,label="Municipio de residencia"),
      Descriptor("ASISTENCIA_SANITARIA","Integer",label="Asistencia sanitaria")\
        .selectablefk("ARENA2_DIC_ASISTENCIA_SANITARIA"),


      #ACCESORIOS_SEGURIDAD
      Descriptor("ACC_SEG_CINTURON","Boolean",label="Cinturon"),
      Descriptor("ACC_SEG_CASCO","Integer",label="Casco")\
        .selectablefk("ARENA2_DIC_ACC_SEG_CASCO"),

      #ACCESORIOS_SEGURIDAD_OPCIONALES
      Descriptor("ACC_SEG_BRAZOS","Boolean",label="Brazos"),
      Descriptor("ACC_SEG_ESPALDA","Boolean",label="Espalda"),
      Descriptor("ACC_SEG_TORSO","Boolean",label="Torso"),
      Descriptor("ACC_SEG_MANOS","Boolean",label="Manos"),
      Descriptor("ACC_SEG_PIERNAS","Boolean",label="Piernas"),
      Descriptor("ACC_SEG_PIES","Boolean",label="Pies"),
      Descriptor("ACC_SEG_PRENDA_REF","Boolean"),

      Descriptor("POSICION_VEHI","Integer",label="Posicion en el vehiculo")\
        .selectablefk("ARENA2_DIC_POSICION_VEHICULO"),
      Descriptor("NINYO_EN_BRAZO","Boolean", label="Ni\xf1o en brazo"),

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
    pasajero = self.next()
    if pasajero == None:
      return None

    values = [
      # 0 LID_PASAJERO
      get1(pasajero,"@ID_ACCIDENTE") +"/"+ get1(pasajero,"@ID_VEHICULO") +"/"+ get1(pasajero,"@ID_PASAJERO"),
      
      # 1 ID_ACCIDENTE
      get1(pasajero,"@ID_ACCIDENTE"),      
      
      # 2 LID_VEHICULO
      get1(pasajero,"@ID_ACCIDENTE") +"/"+ get1(pasajero,"@ID_VEHICULO"),
      
      # 3 ID_VEHICULO
      get1(pasajero,"@ID_VEHICULO"),
      
      # 4 ID_PASAJERO
      get1(pasajero,"@ID_PASAJERO"),

      # 5 FECHA_NACIMIENTO
      get1(pasajero,"FECHA_NACIMIENTO"),
      # 6
      null2zero(get1(pasajero,"SEXO")),
      # 7
      get1(pasajero,"PAIS_RESIDENCIA"),
      # 8
      get1(pasajero,"PROVINCIA_RESIDENCIA"),
      # 9
      get1(pasajero,"MUNICIPIO_RESIDENCIA"),
      # 10
      null2zero(get1(pasajero,"ASISTENCIA_SANITARIA")),

      # 11
      sino2bool(get2(pasajero,"ACCESORIOS_SEGURIDAD","ACC_SEG_CINTURON")),
      # 12
      null2zero(get2(pasajero,"ACCESORIOS_SEGURIDAD","ACC_SEG_CASCO")),

      # 13
      sino2bool(get2(pasajero,"ACCESORIOS_SEGURIDAD_OPCIONALES","ACC_SEG_BRAZOS")),
      # 14
      sino2bool(get2(pasajero,"ACCESORIOS_SEGURIDAD_OPCIONALES","ACC_SEG_ESPALDA")),
      # 15
      sino2bool(get2(pasajero,"ACCESORIOS_SEGURIDAD_OPCIONALES","ACC_SEG_TORSO")),
      # 16
      sino2bool(get2(pasajero,"ACCESORIOS_SEGURIDAD_OPCIONALES","ACC_SEG_MANOS")),
      # 17
      sino2bool(get2(pasajero,"ACCESORIOS_SEGURIDAD_OPCIONALES","ACC_SEG_PIERNAS")),
      # 18
      sino2bool(get2(pasajero,"ACCESORIOS_SEGURIDAD_OPCIONALES","ACC_SEG_PIES")),
      # 19
      sino2bool(get2(pasajero,"ACCESORIOS_SEGURIDAD_OPCIONALES","ACC_SEG_PRENDA_REF")),

      # 20
      null2zero(get1(pasajero,"POSICION_VEHI")),
      # 21
      sino2bool(get1(pasajero,"NINYO_EN_BRAZO"))

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
        while self.vehiculoCorriente < len(vehiculos) :
          vehiculo = vehiculos[self.vehiculoCorriente]
          #print "Vehiculo: ", get1(vehiculo,"@ID_ACCIDENTE")+"/"+get1(vehiculo,"@ID_VEHICULO"), self.vehiculoCorriente
          pasajeros = self.getPasajeros(vehiculo)
          if self.pasajeroCorriente < len(pasajeros) :
            pasajero = pasajeros[self.pasajeroCorriente]
            #print "Pasajero: ", get1(pasajero,"@ID_ACCIDENTE")+"/"+get1(pasajero,"@ID_VEHICULO")+"/"+get1(pasajero,"@ID_PASAJERO")
            self.pasajeroCorriente += 1
            return pasajero
          self.vehiculoCorriente += 1
          self.pasajeroCorriente = 0
        
        self.accidenteCorriente += 1
        self.vehiculoCorriente = 0
        self.pasajeroCorriente = 0

      self.informeCorriente += 1
      self.accidenteCorriente = 0
      self.vehiculoCorriente = 0
      self.pasajeroCorriente = 0

    self.informeCorriente = None
    return None
