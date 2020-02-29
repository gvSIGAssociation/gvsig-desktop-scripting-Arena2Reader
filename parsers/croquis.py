# encoding: utf-8

import gvsig

import os

from org.gvsig.fmap.geom.aggregate import MultiPolygon
from org.gvsig.scripting.app.extension import ScriptingUtils
import xmltodic
from org.gvsig.fmap.geom import GeometryUtils

from util import sino2bool, null2empty, null2zero, get1, get2, Descriptor, generate_translations

COLUMNS_DEFINITION = [
  Descriptor("LID_CROQUIS","String",20,hidden=True, pk=True,
    label="_Id_croquis")\
    .tag("dynform.readonly",True),
  Descriptor("ID_ACCIDENTE","String",20,
    label="_Accidente")\
    .tag("dynform.readonly",True)\
    .set("relation","Collaboration")\
    .foreingkey("ARENA2_ACCIDENTES","ID_ACCIDENTE","FORMAT('%s',ID_ACCIDENTE)"),
  Descriptor("ID_CROQUIS","Integer", 
    label="_Codigo_croquis",
    shortlabel="_Cod_croquis")\
    .tag("dynform.readonly",True),
  Descriptor("IMAGEN","URL", 
    label="_Imagen", 
    profile="Image")\
    .tag("dynform.readonly",True)\
    .tag("dynform.height", 300)
] 


class CroquisParser(object):
  
  def __init__(self, fname, xml=None):
    self.fname = fname
    self.xml = xml
    self.informeCorriente = None
    self.accidenteCorriente = None
    self.croquisCorriente = None
    self.croquis = None

  def getXML(self):
    return self.xml
    
  def open(self):
    if self.xml == None:
      fileXml = open(self.fname,"r")
      data = fileXml.read()
      fileXml.close()
      self.xml = xmltodic.parse(data)
      #print self.xml

    self.croquis = self.loadCroquis(self.fname)
    self.rewind()

  def rewind(self):
    self.informeCorriente = 0
    self.accidenteCorriente = 0
    self.croquisCorriente = 0
  
  def loadCroquis(self, pathname):
    basedir = os.path.dirname(pathname)
    accidentesdir = os.path.join(basedir,"croquis")
    accidentes = dict()
    for ID_ACCIDENTE in os.listdir(accidentesdir):
      croquis = list()
      croquisdir = os.path.join(basedir,"croquis",ID_ACCIDENTE)
      n = 0
      for image in os.listdir(croquisdir):
        croquis.append( {
            "LID_CROQUIS": "%s/%s" % (ID_ACCIDENTE ,n),
            "ID_ACCIDENTE": ID_ACCIDENTE,
            "ID_CROQUIS": n,
            "IMAGEN": "file://"+os.path.join(basedir,"croquis",ID_ACCIDENTE,image)
          }
        )
        n += 1
      accidentes[ID_ACCIDENTE] = croquis
    return accidentes

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

  def getCroquis(self, accidente):
    return self.croquis.get(accidente["@ID_ACCIDENTE"], list())
    
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
    croquis = self.next()
    if croquis == None:
      return None
    
    values = [
      get1(croquis,"LID_CROQUIS"),
      get1(croquis,"ID_ACCIDENTE"),
      get1(croquis,"ID_CROQUIS"),
      get1(croquis,"IMAGEN")
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
        croquis = self.getCroquis(accidente)
        if self.croquisCorriente < len(croquis) :
          unCroquis = croquis[self.croquisCorriente]
          #print "Croquis: ", get1(unCroquis,"LID_CROQUIS"), self.croquisCorriente
          self.croquisCorriente += 1
          return unCroquis
        self.accidenteCorriente += 1
        self.croquisCorriente = 0

      self.informeCorriente += 1
      self.accidenteCorriente = 0
      self.croquisCorriente = 0

    self.informeCorriente = None
    return None


def main(*args):
  generate_translations(COLUMNS_DEFINITION)
  
    