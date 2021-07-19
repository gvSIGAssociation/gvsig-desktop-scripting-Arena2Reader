# encoding: utf-8

import gvsig
import sys

import os
from gvsig.utils import getTempFile
from org.gvsig.fmap.geom.aggregate import MultiPolygon
from org.gvsig.scripting.app.extension import ScriptingUtils
import xmltodic
from org.gvsig.fmap.geom import GeometryUtils
from org.apache.tika import Tika
from util import parseToBool, parseToString, parseToNumber, get1, get2, Descriptor, generate_translations, parseToNull
from gvsig.uselib import use_plugin
use_plugin("org.gvsig.pdf.app.mainplugin")
from org.gvsig.pdf.lib.impl import DefaultPDFDocument
from java.io import File
from javax.imageio import ImageIO

COLUMNS_DEFINITION = [
  Descriptor("LID_CROQUIS","String",100,hidden=True, pk=True,
    label="_Id_croquis")\
    .tag("dynform.readonly",True),
  Descriptor("ID_ACCIDENTE","String",20,
    label="_Accidente")\
    .tag("dynform.readonly",True)\
    .set("relation","Collaboration")\
    .set("indexed",True)\
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
    self.tags = {}
    
  def getParserTags(self):
    return self.tags
    
  def close(self):
    self.xml = None
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
    tika = Tika()
    doc = DefaultPDFDocument();
    for ID_ACCIDENTE in os.listdir(accidentesdir):
      croquis = list()
      croquisdir = os.path.join(basedir,"croquis",ID_ACCIDENTE)
      n = 0
      try:
        iterDir = os.listdir(croquisdir)
      except:
        continue
      for image in iterDir:
        # chec if is pdf -> image
        pathImage = os.path.join(basedir,"croquis",ID_ACCIDENTE,image)
        fileImage  = File(pathImage)
        mimeType = tika.detect(fileImage);
        if mimeType == "application/pdf":
          # convertir a imagen el pdf
          filePdf = fileImage
          doc.setSource(filePdf)
          for i in range(0, doc.getNumPages()):
            img = doc.toImage(i)
            tempPdfImage = getTempFile("tempPDF", ".png")
            f = File(tempPdfImage)
            ImageIO.write(img, "png", f)
            croquis.append( {
                "LID_CROQUIS": "%s/%s" % (ID_ACCIDENTE ,n),
                "ID_ACCIDENTE": ID_ACCIDENTE,
                "ID_CROQUIS": n,
                "IMAGEN": "file://"+tempPdfImage
              }
            )
            n+=1
            #print "temppdf:"+ID_ACCIDENTE+":"+pathImage
          doc.dispose()
        else:
          croquis.append( {
                "LID_CROQUIS": "%s/%s" % (ID_ACCIDENTE ,n),
                "ID_ACCIDENTE": ID_ACCIDENTE,
                "ID_CROQUIS": n,
                "IMAGEN": "file://"+pathImage
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
    accidentes = informe["ACCIDENTES"]
    if accidentes==None:
      return tuple()
    accidentes = accidentes.get('ACCIDENTE',None)
    if accidentes==None:
      return tuple()
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
    
    values = []
    croquis_id = None
    try:
      croquis_id = get1(croquis,"LID_CROQUIS")
    
      values.append(croquis_id)
      values.append(get1(croquis,"ID_ACCIDENTE"))
      values.append(get1(croquis,"ID_CROQUIS"))
      values.append(get1(croquis,"IMAGEN"))

    except:
      ex = sys.exc_info()[1]
      gvsig.logger("No se puede leer el croquis %s. %s" % (croquis_id,str(ex)), gvsig.LOGGER_WARN, ex)
      raise

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

def test3():
  #fname = '/home/osc/gva_arena2/test/TV_12_2020_07_Q1/victimas.xml'  
  #fname = '/home/osc/gva_arena2/XML_test/victor_005/XML-CastellAleixandre/danyos-prueba-10001.xml'
  fname = '/home/osc/gva_arena2/IMPORT_TEST_ERROR_CROQUIS/TV_03_2019_01_Q2/victimas.xml'
  p = CroquisParser(fname)
  p.open()
  print "Num accidentes: ", p.getRowCount()
  p.rewind()
  while True:
    print "In"
    line = p.read()
    if line == None:
      break
    print p.accidenteCorriente, line[0]
    for i in range(0, len(line)):
      print COLUMNS_DEFINITION[i].name, ": ", line[i]
    print len(line)
    return
    
def main(*args):
  #generate_translations(COLUMNS_DEFINITION)
  test3()
  pass
    