# encoding: utf-8

import gvsig

from org.gvsig.fmap.geom.aggregate import MultiPolygon
from org.gvsig.scripting.app.extension import ScriptingUtils
import xmltodic
from org.gvsig.fmap.geom import GeometryUtils

from util import sino2bool, null2empty, null2zero, get1, get2, Descriptor

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
      Descriptor("LID_PEATON","String",20,hidden=True, pk=True),
      Descriptor("ID_ACCIDENTE","String",20,label="Accidente")\
        .foreingkey("ARENA2_ACCIDENTES","ID_ACCIDENTE","FORMAT('%s',ID_ACCIDENTE)"),
      Descriptor("ID_PEATON","Integer", label="Cod.pasajero"),
      
      Descriptor("FECHA_NACIMIENTO","Date",label="Fecha nacimiento"),
      Descriptor("SEXO","Integer",label="Sexo")\
        .selectablefk("ARENA2_DIC_SEXO"),
      Descriptor("PAIS_RESIDENCIA","String", size=100,label="Pais de residencia"),
      Descriptor("PROVINCIA_RESIDENCIA","String", size=100,label="Provincia de residencia"),
      Descriptor("MUNICIPIO_RESIDENCIA","String", size=100,label="Municipio de residencia"),
      Descriptor("ASISTENCIA_SANITARIA","Integer",label="Asistencia sanitaria")\
        .selectablefk("ARENA2_DIC_ASISTENCIA_SANITARIA"),

      
      # ALCOHOL
      Descriptor("INFLU_ALCOHOL","Boolean"),
      Descriptor("PRUEBA_ALCOHOLEMIA","Integer")
        .selectablefk("ARENA2_DIC_PRUEBA_ALCOHOLEMIA"),
      Descriptor("TASA_ALCOHOLEMIA1","Integer"),
      Descriptor("TASA_ALCOHOLEMIA2","Integer"),
      Descriptor("PRUEBA_ALC_SANGRE","Boolean"),
      Descriptor("SIGNOS_INFLU_ALCOHOL","Boolean"),

      # DROGAS
      Descriptor("INFLU_DROGAS","Boolean"),
      Descriptor("PRUEBA_DROGAS","Integer",label="Prueba drogas")\
        .selectablefk("ARENA2_DIC_PRUEBA_DROGAS"),
      Descriptor("AMP","Boolean").build(),
      Descriptor("CONFIRMADO_AMP","Boolean"),
      Descriptor("BDZ","Boolean"),
      Descriptor("CONFIRMADO_BDZ","Boolean"),
      Descriptor("COC","Boolean"),
      Descriptor("CONFIRMADO_COC","Boolean"),
      Descriptor("THC","Boolean"),
      Descriptor("CONFIRMADO_THC","Boolean"),
      Descriptor("METH","Boolean"),
      Descriptor("CONFIRMADO_METH","Boolean"),
      Descriptor("OPI","Boolean"),
      Descriptor("CONFIRMADO_OPI","Boolean"),
      Descriptor("OTRAS","Boolean"),
      Descriptor("CONFIRMADO_OTRAS","Boolean"),
      Descriptor("SIGNOS_INFLU_DROGAS","Boolean"),

      Descriptor("MOTIVO_DESPLAZAMIENTO","Integer",label="Motivo desplazamiento")\
        .selectablefk("ARENA2_DIC_MOTIVO_DESPLAZA_PEA"),
      Descriptor("ACCION_PEA","Integer",label="Accion del peaton")\
        .selectablefk("ARENA2_DIC_ACCION_PEA"),

      # PRES_INFRAC_PEA
      Descriptor("INFLU_PRES_INFRAC","Boolean"),
      Descriptor("PRES_INFRAC_PEA","Integer")\
        .selectablefk("ARENA2_DIC_INFRACCIONES_PEATON"),

      Descriptor("POSIBLE_RESPONSABLE","Boolean"),
      
      # FACTORES_ATENCION
      Descriptor("INFLU_FACT_ATENCION","Boolean"),
      Descriptor("FACTORES_ATENCION","Integer")\
        .selectablefk("ARENA2_DIC_FACTORES_ATENCION_PEA"),
      
      # PRESUNTOS_ERRORES
      Descriptor("INFLU_PRES_ERROR","Boolean"),
      Descriptor("PRESUNTOS_ERRORES","Integer")
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
    