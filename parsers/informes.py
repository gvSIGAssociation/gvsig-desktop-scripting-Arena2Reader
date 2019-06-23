# encoding: utf-8

import gvsig

from org.gvsig.fmap.geom.aggregate import MultiPolygon
from org.gvsig.scripting.app.extension import ScriptingUtils
import xmltodic
from org.gvsig.fmap.geom import GeometryUtils

from util import sino2bool, null2empty, null2zero, get1, get2

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
      "LID_INFORME:String:size:20:set:hidden=true",
      "COD_INFORME:String:size:20:set:label=Codigo",
      "FECHA_INI_EXPORT:Date:set:label=Fecha inicio",
      "FECHA_FIN_EXPORT:Date:set:label=Fecha fin",
      "ACCIDENTES:List:set:group=Accidentes:set:profile=DAL.Features:set:expression=FEATURES('ARENA2_ACCIDENTES',FORMAT('COD_INFORME = ''%s''',COD_INFORME)):tag:dynform.label.empty=true:tag:DAL.features.columns=ID_ACCIDENTE/FECHA_ACCIDENTE/COD_PROVINCIA/COD_MUNICIPIO/COD_POBLACION:tag:DAL.features.tableName=ARENA2_ACCIDENTES:tag:DAL.features.codeName=ID_ACCIDENTE"
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
