# encoding: utf-8

import gvsig

from org.gvsig.fmap.geom.aggregate import MultiPolygon
from org.gvsig.scripting.app.extension import ScriptingUtils
import xmltodic
from org.gvsig.fmap.geom import GeometryUtils

from util import sino2bool, null2empty, null2zero, get1, get2

class PeatonesParser(object):
  
  def __init__(self, fname, xml=None):
    self.fname = fname
    self.xml = xml
    self.informeCorriente = None
    self.accidenteCorriente = None
    self.peatonCorriente = None

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
    self.peatonCorriente = 0
  
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

  def getPeatones(self, accidente):
    try:
      peatones = accidente["PEATONES"]['PEATON']
      if not isinstance(peatones,list):
        peatones = [ peatones ]
      return peatones
    except: # Si no hay peatones da error; nosotros devolvemos una lista vacia
      return list()

  def getColumns(self):
    columns = [
      "LID_PEATON:String:set:size=20:set:hidden=true",
      "ID_ACCIDENTE:String:set:size=20:set:label=Accidente:set:profile=DAL.ForeingKey:tag:DAL.foreingTable=ARENA2_ACCIDENTES:tag:DAL.foreingCode=ID_ACCIDENTE:tag:DAL.foreingLabel=FORMAT('%s',ID_ACCIDENTE)",
      "ID_PEATON:Integer:set:label=Cod. peaton",
      
      "FECHA_NACIMIENTO:Date:set:label=Fecha nacimiento",
      "SEXO:Integer:set:label=Sexo:set:profile=DAL.SelectableForeingKey:tag:DAL.foreingTable=ARENA2_SEXO:tag:DAL.foreingCode=ID:tag:DAL.foreingLabel=FORMAT('%02d - %s',ID,DESCRIPCION)",
      "PAIS_RESIDENCIA:String:set:size=100:set:label=Pais de residencia",
      "PROVINCIA_RESIDENCIA:String:set:size=100:set:label=Provincia de residencia",
      "MUNICIPIO_RESIDENCIA:String:set:size=100:set:label=Municipio de residencia",
      "ASISTENCIA_SANITARIA:Integer:set:label=Asistencia sanitaria:set:profile=DAL.SelectableForeingKey:tag:DAL.foreingTable=ARENA2_ASISTENCIA_SANITARIA:tag:DAL.foreingCode=ID:tag:DAL.foreingLabel=FORMAT('%02d - %s',ID,DESCRIPCION)",

      # ALCOHOL
      "INFLU_ALCOHOL:Boolean",
      "PRUEBA_ALCOHOLEMIA:Integer",
      "TASA_ALCOHOLEMIA1:Integer",
      "TASA_ALCOHOLEMIA2:Integer",
      "PRUEBA_ALC_SANGRE:Boolean",
      "SIGNOS_INFLU_ALCOHOL:Boolean",

      # DROGAS
      "INFLU_DROGAS:Boolean",
      "PRUEBA_DROGAS:Integer:set:label=Prueba drogas:set:profile=DAL.SelectableForeingKey:tag:DAL.foreingTable=ARENA2_ PRUEBA_DROGAS:tag:DAL.foreingCode=ID:tag:DAL.foreingLabel=FORMAT('%02d - %s',ID,DESCRIPCION)",
      "AMP:Boolean",
      "CONFIRMADO_AMP:Boolean",
      "BDZ:Boolean",
      "CONFIRMADO_BDZ:Boolean",
      "COC:Boolean",
      "CONFIRMADO_COC:Boolean",
      "THC:Boolean",
      "CONFIRMADO_THC:Boolean",
      "METH:Boolean",
      "CONFIRMADO_METH:Boolean",
      "OPI:Boolean",
      "CONFIRMADO_OPI:Boolean",
      "OTRAS:Boolean",
      "CONFIRMADO_OTRAS:Boolean",
      "SIGNOS_INFLU_DROGAS:Boolean",

      "MOTIVO_DESPLAZAMIENTO:Integer",
      "ACCION_PEA:Integer",

      # PRES_INFRAC_PEA
      "INFLU_PRES_INFRAC:Boolean",
      "PRES_INFRAC_PEA:Integer",

      "POSIBLE_RESPONSABLE:Boolean",

      # FACTORES_ATENCION
      "INFLU_FACT_ATENCION:Boolean",
      "FACTORES_ATENCION:Integer",
      
      # PRESUNTOS_ERRORES
      "INFLU_PRES_ERROR:Boolean",
      "PRESUNTOS_ERRORES:Integer",
      
    ]
    return columns
    
  def read(self):
    peaton = self.next()
    if peaton == None:
      return None

    values = [
      # LID_PEATON
      get1(peaton,"@ID_ACCIDENTE") +"/"+ get1(peaton,"@ID_PEATON"),
      
      get1(peaton,"@ID_ACCIDENTE"),      
      get1(peaton,"@ID_PEATON"),
      
      get1(peaton,"FECHA_NACIMIENTO"),
      null2zero(get1(peaton,"SEXO")),
      get1(peaton,"PAIS_RESIDENCIA"),
      get1(peaton,"PROVINCIA_RESIDENCIA"),
      get1(peaton,"MUNICIPIO_RESIDENCIA"),
      null2zero(get1(peaton,"ASISTENCIA_SANITARIA")),

      sino2bool(get2(peaton,"ALCOHOL","@INFLU_ALCOHOL")),
      null2zero(get2(peaton,"ALCOHOL","PRUEBA_ALCOHOLEMIA")),
      null2zero(get2(peaton,"ALCOHOL","TASA_ALCOHOLEMIA1")),
      null2zero(get2(peaton,"ALCOHOL","TASA_ALCOHOLEMIA2")),
      sino2bool(get2(peaton,"ALCOHOL","PRUEBA_ALC_SANGRE")),
      sino2bool(get2(peaton,"ALCOHOL","SIGNOS_INFLU_ALCOHOL")),

      sino2bool(get2(peaton,"DROGAS","@INFLU_DROGAS")),
      null2zero(get2(peaton,"DROGAS","PRUEBA_DROGAS")),
      sino2bool(get2(peaton,"DROGAS","AMP")),
      sino2bool(get2(peaton,"DROGAS","CONFIRMADO_AMP")),
      sino2bool(get2(peaton,"DROGAS","BDZ")),
      sino2bool(get2(peaton,"DROGAS","CONFIRMADO_BDZ")),
      sino2bool(get2(peaton,"DROGAS","COC")),
      sino2bool(get2(peaton,"DROGAS","CONFIRMADO_COC")),
      sino2bool(get2(peaton,"DROGAS","THC")),
      sino2bool(get2(peaton,"DROGAS","CONFIRMADO_THC")),
      sino2bool(get2(peaton,"DROGAS","METH")),
      sino2bool(get2(peaton,"DROGAS","CONFIRMADO_METH")),
      sino2bool(get2(peaton,"DROGAS","OPI")),
      sino2bool(get2(peaton,"DROGAS","CONFIRMADO_OPI")),
      sino2bool(get2(peaton,"DROGAS","OTRAS")),
      sino2bool(get2(peaton,"DROGAS","CONFIRMADO_OTRAS")),
      sino2bool(get2(peaton,"DROGAS","SIGNOS_INFLU_DROGAS")),

      get1(peaton,"MOTIVO_DESPLAZAMIENTO"),
      null2zero(get1(peaton,"ACCION_PEA")),
      
      sino2bool(get2(peaton,"PRES_INFRAC_PEA","@INFLU_PRES_INFRAC")),
      null2zero(get2(peaton,"PRES_INFRAC_PEA","#text")),

      sino2bool(get1(peaton,"POSIBLE_RESPONSABLE")),
      
      sino2bool(get2(peaton,"FACTORES_ATENCION","@INFLU_FACT_ATENCION")),
      null2zero(get2(peaton,"FACTORES_ATENCION","#text")),

      sino2bool(get2(peaton,"PRESUNTOS_ERRORES","@INFLU_PRES_ERROR")),
      null2zero(get2(peaton,"PRESUNTOS_ERRORES","#text")),

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
        peatones = self.getPeatones(accidente)
        if self.peatonCorriente < len(peatones) :
          peaton = peatones[self.peatonCorriente]
          #print "Peaton: ", get1(peaton,"@ID_ACCIDENTE")+"/"+get1(peaton,"@ID_PEATON"), self.peatonCorriente
          self.peatonCorriente += 1
          return peaton
        self.accidenteCorriente += 1
        self.peatonCorriente = 0

      self.informeCorriente += 1
      self.accidenteCorriente = 0
      self.peatonCorriente = 0

    self.informeCorriente = None
    return None
    