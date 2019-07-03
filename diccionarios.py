# encoding: utf-8

import gvsig

from gvsig import getResource

from org.gvsig.fmap.dal import DALLocator
from java.io import File

NAMES = (
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
  "ARENA2_DIC_NUDO_APROX",
  "ARENA2_DIC_NUDO",
  "ARENA2_DIC_NUDO_INFORMACION",
  "ARENA2_DIC_POSICION_VIA",
  "ARENA2_DIC_SENTIDO_CIRCULA",
  "ARENA2_DIC_SENTIDO",
  "ARENA2_DIC_TIPO_VEHICULO",
  "ARENA2_DIC_TIPO_VIA",
  "ARENA2_DIC_TITULARIDAD_VIA",
  "ARENA2_DIC_ZONA",
)

def getNames():
  return NAMES

def getParameters(name):
  dataManager = DALLocator.getDataManager()
  fname = getResource(__file__,"datos",name+".csv")
  parameters = dataManager.createStoreParameters("CSV")
  parameters.setDynValue("profile","STANDARD_PREFERENCE")
  parameters.setDynValue("quotePolicy","AlwaysQuoteMode")
  parameters.setDynValue("delimiter",";")
  parameters.setDynValue("commentStartMarker","#")
  parameters.setDynValue("automaticTypesDetection",False)
  parameters.setDynValue("firstLineHeader",True)
  parameters.setFile(File(fname))
  return parameters
  
def main(*args):
    pass
