# encoding: utf-8

import gvsig

from org.gvsig.fmap.geom.aggregate import MultiPolygon
from org.gvsig.scripting.app.extension import ScriptingUtils
import xmltodic
from org.gvsig.fmap.geom import GeometryUtils

from util import sino2bool, null2empty, null2zero, get1, get2, Descriptor

class InformesParser(object):
  
  def __init__(self, fname, xml=None):
    self.fname = fname
    self.xml = xml
    self.informeCorriente = None

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
  
  def getInformes(self):
    informes = self.xml["INFORME"]
    if not isinstance(informes,list):
      informes = [ informes ]
    return informes

  def getColumns(self):
    columns = [
      Descriptor("LID_INFORME","String",20,hidden=True, pk=True),
      Descriptor("COD_INFORME","String",20, hidden=False),
      
      Descriptor("FECHA_INI_EXPORT","Date",label="Fecha inicio"),
      Descriptor("FECHA_FIN_EXPORT","Date",label="Fecha fin"),
      Descriptor("ACCIDENTES","List", group="Accidentes")\
        .relatedFeatures(
          "ARENA2_ACCIDENTES",
          "ID_ACCIDENTE",
          ("ID_ACCIDENTE","FECHA_ACCIDENTE","COD_PROVINCIA","COD_MUNICIPIO","COD_POBLACION"),
          "FEATURES('ARENA2_ACCIDENTES',FORMAT('COD_INFORME = ''%s''',COD_INFORME))"
        )\
        .set("dynform.label.empty",True)
    ]
    return columns

  def getRowCount(self):
    informes = self.getInformes()
    return len(informes)
   
  def read(self):
    informes = self.getInformes()
    if self.informeCorriente >= len(informes):
      return None
    informe = informes[self.informeCorriente]
    values = [
      null2empty(informe.get("@COD_INFORME", None)),
      null2empty(informe.get("@COD_INFORME", None)),
      null2empty(informe.get("@FECHA_INI_EXPORT", None)),
      null2empty(informe.get("@FECHA_FIN_EXPORT", None)),
      None # ACCIDENTES
    ]
    self.next()
    return values

  def next(self):
    self.informeCorriente += 1
