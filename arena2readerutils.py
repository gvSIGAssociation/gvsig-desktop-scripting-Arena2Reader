# encoding: utf-8

import gvsig

import os.path

from gvsig import getResource

from java.io import File

import java.io.FileFilter 
import javax.swing.filechooser.FileFilter

from org.gvsig.fmap.dal import DALLocator
from org.gvsig.tools.resourcesstorage import FilesResourcesStorage

DIC_NAMES = (
  "ARENA2_DIC_ACCION_CONDUCTOR",
  "ARENA2_DIC_ACCION_PAS",
  "ARENA2_DIC_ACCION_PEA",
  "ARENA2_DIC_ACC_SEG_CASCO",
  "ARENA2_DIC_ACC_SEG_COND",
  "ARENA2_DIC_ACC_SEG_PAS",
  "ARENA2_DIC_ACC_SEG_PEA",
  "ARENA2_DIC_ACERA",
  "ARENA2_DIC_ANCHURA_ARCEN",
  "ARENA2_DIC_ANCHURA_CALZADA",
  "ARENA2_DIC_ANCHURA_CARRIL",
  "ARENA2_DIC_ASISTENCIA_SANITARIA",
  "ARENA2_DIC_CARACTERISTICAS_PERMISO",
  "ARENA2_DIC_CARACT_FUNCIONAL_VIA",
  "ARENA2_DIC_CLASE_PERMISO",
  "ARENA2_DIC_CONDICION_FIRME",
  "ARENA2_DIC_DANYOS",
  "ARENA2_DIC_DESPLAZAMIENTO_PREVISTO",
  "ARENA2_DIC_ERRORES_COND",
  "ARENA2_DIC_ERRORES_PEA",
  "ARENA2_DIC_ESTADO_ACCIDENTE",
  "ARENA2_DIC_ESTADO_INFORME",
  "ARENA2_DIC_FACTORES_ATENCION_COND",
  "ARENA2_DIC_FACTORES_ATENCION_PEA",
  "ARENA2_DIC_GENERICO2",
  "ARENA2_DIC_GRAVEDAD",
  "ARENA2_DIC_ILUMINACION",
  "ARENA2_DIC_INFORME_JUDICIAL",
  "ARENA2_DIC_INFRACCIONES_CODUCTOR",
  "ARENA2_DIC_INFRACCIONES_OTRAS",
  "ARENA2_DIC_INFRACCIONES_PEATON",
  "ARENA2_DIC_ITV",
  "ARENA2_DIC_LUGAR_CIRCULA",
  "ARENA2_DIC_MARCAS_VIALES",
  "ARENA2_DIC_METEO",
  "ARENA2_DIC_MMA",
  "ARENA2_DIC_MOTIVO_DESPLAZA_COND",
  "ARENA2_DIC_NIEBLA",
  "ARENA2_DIC_NIVEL_CIRCULACION",
  "ARENA2_DIC_NUDO_APROX",
  "ARENA2_DIC_NUDO",
  "ARENA2_DIC_NUDO_INFORMACION",
  "ARENA2_DIC_NUMERO_CALZADAS",
  "ARENA2_DIC_ONU",
  "ARENA2_DIC_POSICION_VIA",
  "ARENA2_DIC_PRUEBA_ALCOHOLEMIA",
  "ARENA2_DIC_PRUEBA_DROGAS",
  "ARENA2_DIC_SENTIDO_CIRCULA",
  "ARENA2_DIC_SENTIDO",
  "ARENA2_DIC_SENTIDOS_VIA",
  "ARENA2_DIC_SEXO",
  "ARENA2_DIC_TIPO_ACCIDENTE_ANIMAL",
  "ARENA2_DIC_TIPO_ACCIDENTE_COLISION",
  "ARENA2_DIC_TIPO_ACCIDENTE_SALIDA",
  "ARENA2_DIC_TIPO_BARRERA",
  "ARENA2_DIC_TIPO_VEHICULO",
  "ARENA2_DIC_TIPO_VIA",
  "ARENA2_DIC_TITULARIDAD_VIA",
  "ARENA2_DIC_TRAZADO_ALZADO",
  "ARENA2_DIC_TRAZADO_PLANTA",
  "ARENA2_DIC_VEL_GENERICA",
  "ARENA2_DIC_VIENTO",
  "ARENA2_DIC_VISIBILIDAD_RESTRINGIDA_POR",
  "ARENA2_DIC_ZONA",
  "ARENA2_DIC_INFRACCIONES_VELOCIDAD",
  "ARENA2_DIC_MOTIVO_DESPLAZA_PEA",
  "ARENA2_DIC_POSICION_VEHICULO",
)

RESOURCE_NAMES = {
  "ARENA2_ACCIDENTES": ("jfrm","jasper", "report", "1.report"),
  "ARENA2_CONDUCTORES": (),
  "ARENA2_CROQUIS": (),
  "ARENA2_INFORMES": (),
  "ARENA2_PASAJEROS": (),
  "ARENA2_PEATONES": (),
  "ARENA2_VEHICULOS": (),
  "ARENA2_AC_VE_CO_PA": ("dal","jasper", "report", "1.report"),
}

class Arena2XMLFileFilter(javax.swing.filechooser.FileFilter, java.io.FileFilter):
  def __init__(self):
    pass

  def accept(self, f):
    if isinstance(f,File):
      if f.isDirectory():
        return True
      f = f.getAbsolutePath()
    else:
      f = str(f)
      if os.path.isdir(f):
        return True
    return isArena2File(f)

  def getDescription(self):
    return "XML of ARENA2"
    
def createArena2XMLFileFilter():
  return Arena2XMLFileFilter()

def isArena2File(pathname):
  try:
    if pathname==None:
      return False
    if os.path.splitext(pathname)[1].lower() != ".xml":
      return False
    if isinstance(pathname,File):
      pathname = pathname.getAbsolutePath()
    f = open(pathname,"r")
    head = f.read(500)
    f.close()
    head = head.lower()
    head = head.replace("\r","").replace("\n"," ")
    x = ("<informe" in head) and ("cod_informe=" in head) and ("fecha_ini_export=" in head) and ("<accidentes>" in head) and ("<accidente" in head) and ("id_accidente=" in head)
    #if not x:
    #  print "@@@@ isArena2File return False (3) head=", repr(head)
    return x
  except:
    return False
    
def getDictionaryNames():
  return DIC_NAMES

def getOpenStoreParametersOfDictionary(name):
  dataManager = DALLocator.getDataManager()
  fname = getResource(__file__,"datos", "tablas",name+".csv")
  parameters = dataManager.createStoreParameters("CSV")
  parameters.setDynValue("profile","STANDARD_PREFERENCE")
  parameters.setDynValue("quotePolicy","AlwaysQuoteMode")
  parameters.setDynValue("delimiter",";")
  parameters.setDynValue("commentStartMarker","#")
  parameters.setDynValue("automaticTypesDetection",False)
  parameters.setDynValue("firstLineHeader",True)
  parameters.setFile(File(fname))
  return parameters

def getResourceNames(tablename):
  return RESOURCE_NAMES.get(tablename,tuple())

def getResourcesStorage(tablename):
  resourcesPath = getResource(__file__,"datos", "recursos", tablename)
  resourcesStorage = FilesResourcesStorage(resourcesPath)
  return resourcesStorage

def main(*args):
  pass
