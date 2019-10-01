# encoding: utf-8

import gvsig
from gvsig import getResource

from org.gvsig.tools.resourcesstorage import FilesResourcesStorage

RESOURCE_NAMES = {
  "ARENA2_ACCIDENTES": ("jfrm","jasper","1.jasper"),
  #"ARENA2_ACCIDENTES": ("jfrm","jasper","RESUMEN_VEHICULOS_IMPLICADOS.jasper"),
  "ARENA2_CONDUCTORES": (),
  "ARENA2_CROQUIS": (),
  "ARENA2_INFORMES": (),
  "ARENA2_PASAJEROS": (),
  "ARENA2_PEATONES": (),
  "ARENA2_VEHICULOS": (),
}

def getResourceNames(tablename):
  return RESOURCE_NAMES.get(tablename,tuple())


def getResourcesStorage(tablename):
  resourcesPath = getResource(__file__,"datos", "recursos", tablename)
  resourcesStorage = FilesResourcesStorage(resourcesPath)
  return resourcesStorage
    

def main(*args):
    pass
