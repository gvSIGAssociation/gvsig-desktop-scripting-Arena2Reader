# encoding: utf-8

import gvsig

from org.gvsig.fmap.geom.aggregate import MultiPolygon
from org.gvsig.scripting.app.extension import ScriptingUtils
import xmltodic
from org.gvsig.fmap.geom import GeometryUtils

from util import sino2bool, null2empty, null2zero, get1, get2, Descriptor, generate_translations

COLUMNS_DEFINITION = [
  Descriptor("LID_PASAJERO","String",size=20,hidden=True, pk=True,
    label="_Id_pasajero")\
    .tag("dynform.readonly",True),
  Descriptor("ID_ACCIDENTE","String",size=20,
    label="_Accidente")\
    .foreingkey("ARENA2_ACCIDENTES","ID_ACCIDENTE","FORMAT('%s',ID_ACCIDENTE)")\
    .tag("dynform.readonly",True),
  Descriptor("LID_VEHICULO","String",size=20,
    label="_Vehiculo")\
    .foreingkey("ARENA2_VEHICULOS","LID_VEHICULO","FORMAT('%s/%s %s %s %s %s',ID_ACCIDENTE,ID_VEHICULO,TIPO_VEHICULO,NACIONALIDAD,MARCA_NOMBRE,MODELO)")\
    .tag("dynform.readonly",True),
  Descriptor("ID_VEHICULO","String",size=5, hidden=True,
    label="Codigo_vehiculo",
    shortlabel="_Cod_vehiculo")\
    .tag("dynform.readonly",True),
  Descriptor("ID_PASAJERO","Integer", 
    label="_Codigo_pasajero",
    shortlabel="_Cod_pasajero")\
    .tag("dynform.readonly",True),
  
  Descriptor("FECHA_NACIMIENTO","Date",
    label="_Fecha_nacimiento")\
    .tag("dynform.readonly",True),
  Descriptor("SEXO","Integer",
    label="_Sexo",
    shortlabel="_Sexo")\
    .tag("dynform.readonly",True)\
    .selectablefk("ARENA2_DIC_SEXO"),
  Descriptor("PAIS_RESIDENCIA","String", size=100,
    label="_Pais_de_residencia",
    shortlabel="_Pais_resi")\
    .tag("dynform.readonly",True),
  Descriptor("PROVINCIA_RESIDENCIA","String", size=100,
    label="_Provincia_de_residencia",
    shortlabel="_Prov_resi")\
    .tag("dynform.readonly",True),
  Descriptor("MUNICIPIO_RESIDENCIA","String", size=100,
    label="_Municipio_de_residencia",
    shortlabel="_Muni_resi")\
    .tag("dynform.readonly",True),
  Descriptor("ASISTENCIA_SANITARIA","Integer",
    label="_Asistencia_sanitaria",
    shortlabel="_Asis_sanitaria")\
    .closedlistfk("ARENA2_DIC_ASISTENCIA_SANITARIA")\
    .tag("dynform.readonly",True),

  Descriptor("POSICION_VEHI","Integer",
    label="_Posicion_en_el_vehiculo",
    shortlabel="_Posicion")\
    .tag("dynform.readonly",True)\
    .selectablefk("ARENA2_DIC_POSICION_VEHICULO"),
  Descriptor("NINYO_EN_BRAZO","Boolean", 
    label="_Ninyo_en_brazo",
    shortlabel="_Ninyo_brazo")\
    .tag("dynform.readonly",True),

  # Grupo: Accesorios de seguridad
  Descriptor("ACC_SEG_CINTURON","Boolean",
    group="_Accesorios_de_seguridad",
    label="_Cinturon")\
    .tag("dynform.readonly",True),
  Descriptor("ACC_SEG_CASCO","Integer",
    group="_Accesorios_de_seguridad",
    label="_Casco")\
    .closedlistfk("ARENA2_DIC_ACC_SEG_CASCO")\
    .tag("dynform.readonly",True),
  Descriptor("ACC_SEG_SIS_RETEN_INFANTIL","Boolean",
    group="_Accesorios_de_seguridad",
    label="_Sistema_retencion_infantil",
    shortlabel="_Sist_ret_inf")\
    .tag("dynform.readonly",True),
  # Seccion: Accesorios de seguridad opcionales
  Descriptor("ACC_SEG_BRAZOS","Boolean",
    group="_Accesorios_de_seguridad",
    label="_Brazos")\
    .tag("dynform.separator","_Accesorios_de_seguridad_opcionales")\
    .tag("dynform.readonly",True),
  Descriptor("ACC_SEG_ESPALDA","Boolean",
    group="_Accesorios_de_seguridad",
    label="_Espalda")\
    .tag("dynform.readonly",True),
  Descriptor("ACC_SEG_TORSO","Boolean",
    group="_Accesorios_de_seguridad",
    label="_Torso")\
    .tag("dynform.readonly",True),
  Descriptor("ACC_SEG_MANOS","Boolean",
    group="_Accesorios_de_seguridad",
    label="_Manos")\
    .tag("dynform.readonly",True),
  Descriptor("ACC_SEG_PIERNAS","Boolean",
    group="_Accesorios_de_seguridad",
    label="_Piernas")\
    .tag("dynform.readonly",True),
  Descriptor("ACC_SEG_PIES","Boolean",
    group="_Accesorios_de_seguridad",
    label="_Pies")\
    .tag("dynform.readonly",True),
  Descriptor("ACC_SEG_PRENDA_REF","Boolean",
    group="_Accesorios_de_seguridad",
    label="_Prenda_reflectante",
    shortlabel="_Prenda_refl")\
    .tag("dynform.readonly",True),
]

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
    pasajero = self.next()
    if pasajero == None:
      return None

    values = [
      get1(pasajero,"@ID_ACCIDENTE") +"/"+ get1(pasajero,"@ID_VEHICULO") +"/"+ get1(pasajero,"@ID_PASAJERO"),
      
      get1(pasajero,"@ID_ACCIDENTE"),      
      
      get1(pasajero,"@ID_ACCIDENTE") +"/"+ get1(pasajero,"@ID_VEHICULO"),
      
      get1(pasajero,"@ID_VEHICULO"),
      
      get1(pasajero,"@ID_PASAJERO"),

      get1(pasajero,"FECHA_NACIMIENTO"),
      null2zero(get1(pasajero,"SEXO")),
      get1(pasajero,"PAIS_RESIDENCIA"),
      get1(pasajero,"PROVINCIA_RESIDENCIA"),
      get1(pasajero,"MUNICIPIO_RESIDENCIA"),
      null2zero(get1(pasajero,"ASISTENCIA_SANITARIA")),

      sino2bool(get2(pasajero,"ACCESORIOS_SEGURIDAD","ACC_SEG_CINTURON")),
      null2zero(get2(pasajero,"ACCESORIOS_SEGURIDAD","ACC_SEG_CASCO")),
      sino2bool(get2(pasajero,"ACCESORIOS_SEGURIDAD","ACC_SEG_SIS_RETEN_INFANTIL")),
      sino2bool(get2(pasajero,"ACCESORIOS_SEGURIDAD_OPCIONALES","ACC_SEG_BRAZOS")),
      sino2bool(get2(pasajero,"ACCESORIOS_SEGURIDAD_OPCIONALES","ACC_SEG_ESPALDA")),
      sino2bool(get2(pasajero,"ACCESORIOS_SEGURIDAD_OPCIONALES","ACC_SEG_TORSO")),
      sino2bool(get2(pasajero,"ACCESORIOS_SEGURIDAD_OPCIONALES","ACC_SEG_MANOS")),
      sino2bool(get2(pasajero,"ACCESORIOS_SEGURIDAD_OPCIONALES","ACC_SEG_PIERNAS")),
      sino2bool(get2(pasajero,"ACCESORIOS_SEGURIDAD_OPCIONALES","ACC_SEG_PIES")),
      sino2bool(get2(pasajero,"ACCESORIOS_SEGURIDAD_OPCIONALES","ACC_SEG_PRENDA_REF")),

      null2zero(get1(pasajero,"POSICION_VEHI")),
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

def main(*args):
  generate_translations(COLUMNS_DEFINITION)
  
