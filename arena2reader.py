# encoding: utf-8

import gvsig

from gvsig import getResource
import re
import os.path

from org.gvsig.fmap.dal import DALLocator
from org.gvsig.fmap.dal.feature.spi.simpleprovider import AbstractSimpleSequentialReaderFactory
from org.gvsig.fmap.dal.feature.spi.simpleprovider import AbstractSimpleSequentialReader
from org.gvsig.fmap.dal import BaseStoresRepository
from java.net import URL
from java.io import File

import addons.Arena2Reader.parsers.informes 
import addons.Arena2Reader.parsers.accidentes 
import addons.Arena2Reader.parsers.vehiculos 
import addons.Arena2Reader.parsers.conductores 
import addons.Arena2Reader.parsers.peatones 
import addons.Arena2Reader.parsers.pasajeros 
import addons.Arena2Reader.parsers.croquis

reload(addons.Arena2Reader.parsers.informes)
reload(addons.Arena2Reader.parsers.accidentes )
reload(addons.Arena2Reader.parsers.vehiculos )
reload(addons.Arena2Reader.parsers.conductores) 
reload(addons.Arena2Reader.parsers.peatones )
reload(addons.Arena2Reader.parsers.pasajeros )
reload(addons.Arena2Reader.parsers.croquis)


from addons.Arena2Reader.parsers.informes import InformesParser
from addons.Arena2Reader.parsers.accidentes import AccidentesParser
from addons.Arena2Reader.parsers.vehiculos import VehiculosParser
from addons.Arena2Reader.parsers.conductores import ConductoresParser
from addons.Arena2Reader.parsers.peatones import PeatonesParser
from addons.Arena2Reader.parsers.pasajeros import PasajerosParser
from addons.Arena2Reader.parsers.croquis import CroquisParser

from addons.Arena2Reader.arena2readerutils import isArena2File
from addons.Arena2Reader.arena2readerutils import getDictionaryNames, getOpenStoreParametersOfDictionary
from addons.Arena2Reader.arena2readerutils import getResourcesStorage

class Table: #(object):
  def __init__(self, parser, name, label=None, tags={}):
    self.parser = parser
    self.name = name
    if label == None:
      self.label = name
    else:
      self.label = label
    #self.tags = tags.update(self.parser.getParserTags())
    
  #def getParserTags(self):
  #  parserTags = self.parser.getParserTags()
  #  self.tags.update(parserTags)
  #  return self.tags
    
tables = {
  "ARENA2_INFORMES": Table(
    InformesParser, 
    "ARENA2_INFORMES", 
    "Arena2 Informes", 
    {
      "dynform.width":500,
    }
  ),
  
  "ARENA2_ACCIDENTES": Table(
    AccidentesParser, 
    "ARENA2_ACCIDENTES", 
    "Arena2 Accidentes", 
    {
      "dynform.height":550, 
      "dynform.width":830, 
      "DAL.Preferred.Columns":"COD_INFORME/ID_ACCIDENTE/TITULARIDAD_VIA/CALLE_NOMBRE/CALLE_NUMERO/CARRETERA/KM/COD_POBLACION/COD_MUNICIPIO/COD_PROVINCIA/FECHA_ACCIDENTE"
    } 
  ),
  
  "ARENA2_VEHICULOS": Table(
    VehiculosParser, 
    "ARENA2_VEHICULOS", 
    "Arena2 Vehiculos", 
    {
      "dynform.width":600
    } 
  ),
  
  "ARENA2_CONDUCTORES": Table(
    ConductoresParser, 
    "ARENA2_CONDUCTORES", 
    "Arena2 Conductores", 
    {
      "dynform.width":500
    } 
  ),
  
  "ARENA2_PEATONES": Table(
    PeatonesParser, 
    "ARENA2_PEATONES", 
    "Arena2 Peatones", 
    {
      "dynform.width":500
    } 
  ),
  
  "ARENA2_PASAJEROS": Table(
    PasajerosParser, 
    "ARENA2_PASAJEROS", 
    "Arena2 Pasajeros", 
    {
      "dynform.width":500
    } 
  ),
  
  "ARENA2_CROQUIS": Table(
    CroquisParser, 
    "ARENA2_CROQUIS", 
    "Arena2 Croquis", 
    {
      "dynform.width":500
    } 
  )
}

class Arena2ReaderFactory(AbstractSimpleSequentialReaderFactory):

  def __init__(self):
    AbstractSimpleSequentialReaderFactory.__init__(self, "ARENA2", "Arena2", ("xml","arena2"))

  def accept(self, f):
    # Este metodo es opcional, si con la extension del fichero es
    # suficiente, no hace falta sobreescribirlo.
    if not AbstractSimpleSequentialReaderFactory.accept(self,f):
      return False
    if isinstance(f,File):
      if f.isDirectory():
        return True
      f = f.getAbsolutePath()
    else:
      f = str(f)
      if os.path.isdir(f):
        return True
    return isArena2File(f)

  def fetchDefaultParameters(self, params):
    # Este metodo es opcional, si el fichero de datos no aporta ningun valor
    # de entre los requeridos en los parametros (como es el SRS), no hace
    # falta sobreescribirlo.
    srs = "EPSG:4326"
    params.setDynValue("CRS",srs)
    
  def createReader(self, params):
    f = params.getFile()
    dataManager = DALLocator.getDataManager()
    repo = BaseStoresRepository("ARENA2_"+f.getName())
    for name in getDictionaryNames():
      parameters = getOpenStoreParametersOfDictionary(name)
      repo.add(name,parameters)
    reader = Arena2Reader(self, params, repo)
    return reader

class Arena2Reader(AbstractSimpleSequentialReader):

  def __init__(self, factory, parameters, repo, name=None, xml=None):
    AbstractSimpleSequentialReader.__init__(self, factory, parameters)
    f = self.getParameters().getFile()
    self._repo = repo
    self._fname = f.getAbsolutePath()
    self._xml = xml
    if name==None:
      self._name = os.path.splitext(f.getName())[0]
    else:
      self._name = name
    self._table = tables[self.getParameter("Tabla").upper()]
    self._parser = None
    self._resourcesStorage = None
    
  def getParser(self):
    if self._parser == None:
      self._parser = self._table.parser(self._fname, self._xml)
      self._parser.open()
    return self._parser

  def getStoresRepository(self):
    return self._repo
    
  def getAlias(self):
    return self._table.name
    
  def getChildren(self):
    xml = self.getParser().getXML()
    children = list()
    for table in tables.values():
      if table.name == self._table.name:
        continue
      params = self.getParameters().getCopy()
      params.setDynValue("Tabla", table.name)
      children.append(Arena2Reader(self.getFactory(), params, self._repo, table.name, xml))
    return children

  def getResourcesStorage(self):
    if self._resourcesStorage == None:
      self._resourcesStorage = getResourcesStorage(self._table.name)
    return self._resourcesStorage
    
  def getName(self):
    return self._name
    
  #def getTags(self):
  #  return self._table.getParserTags()
  
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
    if self._parser!=None:
      self._parser.close()
      self._parser = None
    self._xml = None

def selfRegister():
  factory = Arena2ReaderFactory()
  factory.selfRegister(
    File(getResource(__file__,"Arena2Parameters.xml")).toURI().toURL(),
    File(getResource(__file__,"Arena2Metadata.xml")).toURI().toURL(),
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
    #fieldNames.append(field.split(":")[0])
    fieldNames.append(field.name)
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

def test2():
  factory = Arena2ReaderFactory()
  folder = '/home/jjdelcerro/arena2/quincenas'
  fnames = list()
  for root, dirs, files in os.walk(folder, followlinks=True):
     for name in files:
       pathname = os.path.join(root, name)
       if pathname.lower().endswith(".xml"):
        if factory.accept(File(pathname)):
          gvsig.logger("found file: %r" % pathname)
          fnames.append(pathname)
        else:
          gvsig.logger("skip file: %r" % pathname, gvsig.LOGGER_WARN)
  fnames.sort() 
  #fnames = ( '/home/jjdelcerro/arena2/quincenas/Valencia/TV_46_2018_01_Q1/victimas.xml', )
  n=1
  for fname in fnames:
    gvsig.logger("Process: %d/%d %r" % (n, len(fnames), fname))
    if not factory.accept(File(fname)):
      gvsig.logger("File not supported ", gvsig.LOGGER_WARN)
      continue
    params = factory.createStoreProviderFactory().createParameters()
    params.setFile(File(fname))
    params.setDynValue("Tabla","arena2_informes")
    factory.fetchDefaultParameters(params)
    main_reader = factory.createReader(params)
    readers = [ main_reader ]
    readers.extend(main_reader.getChildren())
    for reader in readers:
      gvsig.logger("  %s (%s)" % (reader.getName(), reader.getRowCount()))
      line = reader.read()
      while line!=None:
        #print line
        line = reader.read()
    main_reader.close()
    n+=1

def test3():
  from org.gvsig.fmap.dal import DALLocator

  dataManager = DALLocator.getDataManager()
  factory = Arena2ReaderFactory()
  folder = '/home/jjdelcerro/arena2/quincenas'
  fnames = list()
  for root, dirs, files in os.walk(folder, followlinks=True):
     for name in files:
       pathname = os.path.join(root, name)
       if pathname.lower().endswith(".xml"):
        if factory.accept(File(pathname)):
          gvsig.logger("found file: %r" % pathname)
          fnames.append(pathname)
        else:
          gvsig.logger("skip file: %r" % pathname, gvsig.LOGGER_WARN)
  fnames.sort() 
  #fnames = ( '/home/jjdelcerro/arena2/quincenas/Valencia/TV_46_2018_01_Q1/victimas.xml', )

  maxfiles = len(fnames)
  maxfiles = min(10,len(fnames))
  for n in range(0,maxfiles):
    fname = fnames[n]
    gvsig.logger("Process: %d/%d %r" % (n, maxfiles, fname))
    if not factory.accept(File(fname)):
      gvsig.logger("File not supported ", gvsig.LOGGER_WARN)
      continue
    store = dataManager.openStore("ARENA2", "file", fname, "CRS", "EPSG:25830")
    for feature in store:
      pass
    store.close()
    store = None
  
    
def main(*args):
  #test2()
  #test3()
  
  #selfRegister()
  fname = '/home/osc/gva_arena2/test/TV_12_2020_07_Q1/victimas.xml'
  fname = '/home/osc/gva_arena2/XML_test/victor_005/XML-CastellAleixandre/danyos-ejemplo-3.xml'
  fname = '/home/osc/gva_arena2/XML_test_cargaTablas/danyos.xml'
  fname = '/home/osc/gva_arena2/XML_test_cargaTablas/TV_03_2021_01_Q1/danyos.xml'
  #test(Arena2ReaderFactory(), fname, "arena2_informes")
  #test(Arena2ReaderFactory(), fname, "arena2_accidentes")
  #test(Arena2ReaderFactory(), fname, "arena2_vehiculos")
  test(Arena2ReaderFactory(), fname, "arena2_conductores")
  #test(Arena2ReaderFactory(), fname, "arena2_peatones")
  #test(Arena2ReaderFactory(), fname, "arena2_pasajeros")
  #test(Arena2ReaderFactory(), fname, "arena2_croquis")
  pass

  
