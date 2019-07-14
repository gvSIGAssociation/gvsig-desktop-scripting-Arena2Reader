# encoding: utf-8

import gvsig
from gvsig import getResource

from org.gvsig.tools.resourcesstorage import FilesResourcesStorage

RESOURCE_NAMES = {
  "ARENA2_ACCIDENTES": tuple("jfrm"),
  "ARENA2_CONDUCTORES": tuple(),
  "ARENA2_CROQUIS": tuple(),
  "ARENA2_INFORMES": tuple(),
  "ARENA2_PASAJEROS": tuple(),
  "ARENA2_PEATONES": tuple(),
  "ARENA2_VEHICULOS": tuple(),
}

def getResourceNames(tablename):
  return RESOURCE_NAMES.get(tablename,tuple())


def getResourcesStorage(tablename):
  resourcesPath = getResource(__file__,"datos", "recursos", tablename)
  resourcesStorage = FilesResourcesStorage(resourcesPath)
  return resourcesStorage
    

def main(*args):
    pass
