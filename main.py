# encoding: utf-8

import gvsig

from gvsig import getResource

from org.gvsig.fmap.dal import DALLocator

from java.io import File

from arena2reader import selfRegister

def carga_diccionario(name):
  fname = getResource(__file__,"diccionarios",name+".csv")
  dataManager = DALLocator.getDataManager()
  parameters = dataManager.createStoreParameters("CSV")
  parameters.setFile(File(fname))
  dataManager.getStoresRepository().add(name,parameters)

def cargar_diccionarios():
  carga_diccionario("ARENA2_DANYOS")
  carga_diccionario("ARENA2_ITV")
  carga_diccionario("ARENA2_LUGAR_CIRCULA")
  carga_diccionario("ARENA2_NUDO")
  carga_diccionario("ARENA2_NUDO_APROX")
  carga_diccionario("ARENA2_NUDO_INFORMACION")
  carga_diccionario("ARENA2_POSICION_VIA")
  carga_diccionario("ARENA2_SENTIDO")
  carga_diccionario("ARENA2_SENTIDO_CIRCULA")
  carga_diccionario("ARENA2_TIPO_VEHICULO")
  carga_diccionario("ARENA2_TIPO_VIA")
  carga_diccionario("ARENA2_TITULARIDAD_VIA")
  carga_diccionario("ARENA2_ZONA")

def main(*args):
  selfRegister()
  cargar_diccionarios()
  
  