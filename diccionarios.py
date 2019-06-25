# encoding: utf-8

import gvsig

from gvsig import getResource

from org.gvsig.fmap.dal import DALLocator
from java.io import File

NAMES = (
  "ARENA2_DANYOS", 
  "ARENA2_ITV", 
  "ARENA2_LUGAR_CIRCULA",
  "ARENA2_NUDO",
  "ARENA2_NUDO_APROX",
  "ARENA2_NUDO_INFORMACION",
  "ARENA2_POSICION_VIA",
  "ARENA2_SENTIDO",
  "ARENA2_SENTIDO_CIRCULA",
  "ARENA2_TIPO_VEHICULO",
  "ARENA2_TIPO_VIA",
  "ARENA2_TITULARIDAD_VIA",
  "ARENA2_ZONA"
)

def getNames():
  return NAMES

def getParameters(name):
  dataManager = DALLocator.getDataManager()
  fname = getResource(__file__,"datos",name+".csv")
  parameters = dataManager.createStoreParameters("CSV")
  parameters.setFile(File(fname))
  return parameters
  
def main(*args):
    pass
