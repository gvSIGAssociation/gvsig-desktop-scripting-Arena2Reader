# encoding: utf-8

import gvsig

from org.gvsig.fmap.dal.feature.spi.simpleprovider import AbstractSimpleSequentialReaderFactory
from org.gvsig.fmap.dal.feature.spi.simpleprovider import AbstractSimpleSequentialReader
from gvsig import getResource
import re
import os.path
from java.net import URL
from java.io import File

from parsers.informes import InformesParser
from parsers.accidentes import AccidentesParser
from parsers.vehiculos import VehiculosParser
from parsers.conductores import ConductoresParser
from parsers.peatones import PeatonesParser
from parsers.pasajeros import PasajerosParser
from parsers.croquis import CroquisParser


class Table(object):
  def __init__(self, parser, name, label=None, tags=None):
    self.parser = parser
    self.name = name
    if label == None:
      self.label = name
    else:
      self.label = label
    self.tags = tags

tables = {
  "informes": Table(InformesParser, "informes", "Arena2 Informes", {"dynform.width":500}),
  "accidentes": Table(AccidentesParser, "accidentes", "Arena2 Accidentes", {"dynform.height":530, "dynform.width":800, "dynform.abeille.form.resource":"jfrm"} ),
  "vehiculos": Table(VehiculosParser, "vehiculos", "Arena2 Vehiculos", {"dynform.width":600} ),
  "conductores": Table(ConductoresParser, "conductores", "Arena2 Conductores", {"dynform.width":500} ),
  "peatones": Table(PeatonesParser, "peatones", "Arena2 Peatones", {"dynform.width":500} ),
  "pasajeros": Table(PasajerosParser, "pasajeros", "Arena2 Pasajeros", {"dynform.width":500} ),
  "croquis": Table(CroquisParser, "croquis", "Arena2 Croquis", {"dynform.width":500} )
}

class Arena2ReaderFactory(AbstractSimpleSequentialReaderFactory):

  def __init__(self):
    AbstractSimpleSequentialReaderFactory.__init__(self, "ARENA2", "Arena2", ("xml","arena2"))

  def accept(self, pathname):
    # Este metodo es opcional, si con la extension del fichero es
    # suficiente, no hace falta sobreescribirlo.
    if not AbstractSimpleSequentialReaderFactory.accept(self,pathname):
      return False
    f = open(pathname.getAbsolutePath(),"r")
    head = f.read(500)
    f.close()
    head = head.lower()
    head = head.replace("\r","").replace("\n"," ")
    #print pathname, repr(head)
    return ("<informe" in head) and ("cod_informe=" in head) and ("fecha_ini_export=" in head) and ("<accidentes>" in head) and ("<accidente" in head) and ("id_accidente=" in head)

  def fetchDefaultParameters(self, params):
    # Este metodo es opcional, si el fichero de datos no aporta ningun valor
    # de entre los requeridos en los parametros (como es el SRS), no hace
    # falta sobreescribirlo.
    srs = "EPSG:4258"
    params.setDynValue("CRS",srs)
    
  def createReader(self, params):
    reader = Arena2Reader(self, params)
    return reader

class Arena2Reader(AbstractSimpleSequentialReader):

  def __init__(self, factory, parameters, tableName=None, xml=None):
    AbstractSimpleSequentialReader.__init__(self, factory, parameters)
    self._fname = self.getParameters().getFile().getAbsolutePath()
    self._xml = xml
    if tableName == None:
      self._name = os.path.splitext(self.getParameters().getFile().getName())[0]
      self._table = tables[self.getParameter("Tabla").lower()]
    else:
      self._name = "arena2_"+tableName
      self._table = tables[tableName]
    self._parser = None
    
  def getParser(self):
    if self._parser == None:
      self._parser = self._table.parser(self._fname, self._xml)
      self._parser.open()
    return self._parser
      
  def getChildren(self):
    xml = self.getParser().getXML()
    children = list()
    for table in tables.values():
      children.append(Arena2Reader(self.getFactory(), self.getParameters(), table.name, xml))
    return children
    
  def getName(self):
    return self._name
    
  def getTags(self):
    return self._table.tags
  
  def getLabel(self):
    return self._table.label + " - " + os.path.splitext(self.getParameters().getFile().getName())[0]
  
  def getFieldNames(self):
    return self.getParser().getColumns()
    
  def getFile(self):
    return self.getParameters().getFile()

  def getRowCount(self):
    return self.getParser().getRowCount()
  
  def read(self):
    return self.getParser().read()
    
  def rewind(self):
    self.getParser().rewind()
    
  def close(self):
    self._parser = None

def selfRegister():
  factory = Arena2ReaderFactory()
  factory.selfRegister(
    URL("file://"+getResource(__file__,"Arena2Parameters.xml")),
    URL("file://"+getResource(__file__,"Arena2Metadata.xml")),
  )

def test(factory, fname, table):
  if not factory.accept(File(fname)):
    print "File not supported by this factory ", factory.getName()
    return
  params = factory.createStoreProviderFactory().createParameters()
  params.setFile(File(fname))
  params.setDynValue("Tabla",table)
  factory.fetchDefaultParameters(params)
  reader = factory.createReader(params)
  print "Reader: ", reader.getFactory().getName()
  print "table: ", reader.getName()
  print "Name: ", table
  print "File: ", reader.getFile()
  print "Fields: "
  n = 0
  fieldNames = list()
  for field in reader.getFieldNames():
    print "  %03d %s" % (n,field)
    fieldNames.append(field.split(":")[0])
    n += 1

  lineNum = 0
  line = reader.read()
  while line!=None and lineNum<10:
    #print line
    for fieldNum in range(len(line)):
      print "ROW %02d %03d %s: %r" %  (lineNum,fieldNum, fieldNames[fieldNum],line[fieldNum])
      n += 1
    line = reader.read()
    lineNum += 1
  reader.rewind() # test rewind
  reader.close()
    

def main(*args):
  selfRegister()
  fname = "/home/jjdelcerro/Descargas/ARENA/TV_03_2019_01_Q1/victimas.xml"
  #test(Arena2ReaderFactory(), fname, "informes")
  #test(Arena2ReaderFactory(), fname, "accidentes")
  test(Arena2ReaderFactory(), fname, "vehiculos")
  #test(Arena2ReaderFactory(), fname, "conductores")
  #test(Arena2ReaderFactory(), fname, "peatones")
  #test(Arena2ReaderFactory(), fname, "pasajeros")
  #test(Arena2ReaderFactory(), fname, "croquis")
  pass

  
