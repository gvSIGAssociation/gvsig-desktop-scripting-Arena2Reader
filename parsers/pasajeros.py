# encoding: utf-8

import gvsig

from org.gvsig.fmap.geom.aggregate import MultiPolygon
from org.gvsig.scripting.app.extension import ScriptingUtils
import xmltodic
from org.gvsig.fmap.geom import GeometryUtils

from util import sino2bool, null2empty, null2zero, get1, get2

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
      "LID_PASAJERO:String:set:size=20:set:hidden=true",
      "ID_ACCIDENTE:String:set:size=20:set:label=Accidente:set:profile=DAL.ForeingKey:tag:DAL.foreingTable=ARENA2_ACCIDENTES:tag:DAL.foreingCode=ID_ACCIDENTE:tag:DAL.foreingLabel=FORMAT('%s',ID_ACCIDENTE)",
      "LID_VEHICULO:String:set:size=20:set:label=Vehiculo:set:profile=DAL.ForeingKey:tag:DAL.foreingTable=ARENA2_VEHICULOS:tag:DAL.foreingCode=LID_VEHICULO:tag:DAL.foreingLabel=FORMAT('%s',LID_VEHICULO)",
      "ID_VEHICULO:Integer:set:hidden=true",
      "ID_PASAJERO:Integer:set:label=Cod. pasajero",
      
      "FECHA_NACIMIENTO:Date:set:label=Fecha nacimiento",
      "SEXO:Integer:set:label=Sexo:set:profile=DAL.SelectableForeingKey:tag:DAL.foreingTable=ARENA2_SEXO:tag:DAL.foreingCode=ID:tag:DAL.foreingLabel=FORMAT('%02d - %s',ID,DESCRIPCION)",
      "PAIS_RESIDENCIA:String:set:size=100:set:label=Pais de residencia",
      "PROVINCIA_RESIDENCIA:String:set:size=100:set:label=Provincia de residencia",
      "MUNICIPIO_RESIDENCIA:String:set:size=100:set:label=Municipio de residencia",
      "ASISTENCIA_SANITARIA:Integer:set:label=Asistencia sanitaria:set:profile=DAL.SelectableForeingKey:tag:DAL.foreingTable=ARENA2_ASISTENCIA_SANITARIA:tag:DAL.foreingCode=ID:tag:DAL.foreingLabel=FORMAT('%02d - %s',ID,DESCRIPCION)",

      #ACCESORIOS_SEGURIDAD
      "ACC_SEG_CINTURON:Boolean:set:label=Cinturon",
      "ACC_SEG_CASCO:Integer:set:label=Casco:set:profile=DAL.SelectableForeingKey:tag:DAL.foreingTable=ARENA2_ ACC_SEG_CASCO:tag:DAL.foreingCode=ID:tag:DAL.foreingLabel=FORMAT('%02d - %s',ID,DESCRIPCION)",

      #ACCESORIOS_SEGURIDAD_OPCIONALES
      "ACC_SEG_BRAZOS:Boolean:set:label=Brazos",
      "ACC_SEG_ESPALDA:Boolean:set:label=Espalda",
      "ACC_SEG_TORSO:Boolean:set:label=Torso",
      "ACC_SEG_MANOS:Boolean:set:label=Manos",
      "ACC_SEG_PIERNAS:Boolean:set:label=Piernas",
      "ACC_SEG_PIES:Boolean:set:label=Pies",
      "ACC_SEG_PRENDA_REF:Boolean",

      "POSICION_VEHI:Integer:set:label=Posicion",
      "NINYO_EN_BRAZO:Boolean:set:label=Ni\xf1o en brazo"

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
