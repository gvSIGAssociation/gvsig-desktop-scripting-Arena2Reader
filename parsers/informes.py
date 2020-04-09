# encoding: utf-8

import gvsig

from org.gvsig.fmap.geom.aggregate import MultiPolygon
from org.gvsig.scripting.app.extension import ScriptingUtils
import xmltodic
from org.gvsig.fmap.geom import GeometryUtils

from util import sino2bool, null2empty, null2zero, get1, get2, Descriptor, generate_translations

COLUMNS_DEFINITION = [
  Descriptor("LID_INFORME","String",20,hidden=True, pk=True, 
    label="Id_informe")\
    .tag("dynform.readonly",True),
  Descriptor("COD_INFORME","String",20, 
    label="_Codigo_informe",
    shortlabel="_Cod_informe")\
    .tag("dynform.readonly",True),
  
  Descriptor("FECHA_INI_EXPORT","Date",
    label="_Fecha_inicio")\
    .tag("dynform.readonly",True),
  Descriptor("FECHA_FIN_EXPORT","Date",
    label="_Fecha_fin")\
    .tag("dynform.readonly",True),
  Descriptor("ACCIDENTES","List", group="_Accidentes")\
    .set("relation","Aggregation")\
    .relatedFeatures(
      "ARENA2_ACCIDENTES",
      "ID_ACCIDENTE",
      ("ID_ACCIDENTE","FECHA_ACCIDENTE","COD_PROVINCIA","COD_MUNICIPIO","COD_POBLACION"),
      "SELECT * FROM ARENA2_ACCIDENTES WHERE ARENA2_INFORMES.COD_INFORME = ARENA2_ACCIDENTES.COD_INFORME;"
    )\
    .tag("dynform.label.empty",True)
]

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
    return COLUMNS_DEFINITION

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


def main(*args):
  generate_translations(COLUMNS_DEFINITION)
  
    