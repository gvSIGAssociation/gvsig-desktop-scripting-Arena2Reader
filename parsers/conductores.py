# encoding: utf-8

import gvsig

from org.gvsig.fmap.geom.aggregate import MultiPolygon
from org.gvsig.scripting.app.extension import ScriptingUtils
import xmltodic
from org.gvsig.fmap.geom import GeometryUtils

from util import sino2bool, null2empty, null2zero, get1, get2

class ConductoresParser(object):
  
  def __init__(self, fname, xml=None):
    self.fname = fname
    self.xml = xml
    self.informeCorriente = None
    self.accidenteCorriente = None
    self.vehiculoCorriente = None

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
    self.accidenteCorriente = 0
    self.vehiculoCorriente = 0
  
  def getInformes(self):
    informes = self.xml["INFORME"]
    if not isinstance(informes,list):
      informes = [ informes ]
    return informes

  def getAccidentes(self, informe):
    accidentes = informe["ACCIDENTES"]['ACCIDENTE']
    if not isinstance(accidentes,list):
      accidentes = [ accidentes ]
    return accidentes

  def getVehiculos(self, accidente):
    vehiculos = accidente["VEHICULOS"]['VEHICULO']
    if not isinstance(vehiculos,list):
      vehiculos = [ vehiculos ]
    return vehiculos

  def getColumns(self):
    columns = [
      "LID_CONDUCTOR:String:set:size=20:set:hidden=true",
      "ID_ACCIDENTE:String:set:size=20:set:label=Accidente:set:profile=DAL.ForeingKey:tag:DAL.foreingTable=ARENA2_ACCIDENTES:tag:DAL.foreingCode=ID_ACCIDENTE:tag:DAL.foreingLabel=FORMAT('%s',ID_ACCIDENTE)",
      "LID_VEHICULO:String:set:size=20:set:label=Vehiculo:set:profile=DAL.ForeingKey:tag:DAL.foreingTable=ARENA2_VEHICULOS:tag:DAL.foreingCode=LID_VEHICULO:tag:DAL.foreingLabel=FORMAT('%s/%s %s %s %s %s',ID_ACCIDENTE,ID_VEHICULO,TIPO_VEHICULO,NACIONALIDAD,MARCA_NOMBRE,MODELO)",
      "ID_VEHICULO:String:set:size=5:set:hidden=true",
      
      "FECHA_NACIMIENTO:Date:set:label=Fecha nacimiento",
      "SEXO:Integer:set:label=Sexo:set:profile=DAL.SelectableForeingKey:tag:DAL.foreingTable=ARENA2_SEXO:tag:DAL.foreingCode=ID:tag:DAL.foreingLabel=FORMAT('%02d - %s',ID,DESCRIPCION)",
      "NACIONALIDAD:String:set:size=100:set:label=Nacionalidad",
      "PAIS_RESIDENCIA:String:set:size=100:set:label=Pais de residencia",
      "PROVINCIA_RESIDENCIA:String:set:size=100:set:label=Provincia de residencia",
      "MUNICIPIO_RESIDENCIA:String:set:size=100:set:label=Municipio de residencia",
      "ASISTENCIA_SANITARIA:Integer:set:label=Asistencia sanitaria:set:profile=DAL.SelectableForeingKey:tag:DAL.foreingTable=ARENA2_ASISTENCIA_SANITARIA:tag:DAL.foreingCode=ID:tag:DAL.foreingLabel=FORMAT('%02d - %s',ID,DESCRIPCION)",
      "CARACT_PERMISO:Integer:set:label=Caracteristicas del permiso:set:profile=DAL.SelectableForeingKey:tag:DAL.foreingTable=ARENA2_CARACTERISTICAS_PERMISO:tag:DAL.foreingCode=ID:tag:DAL.foreingLabel=FORMAT('%02d - %s',ID,DESCRIPCION)",
      "CLASE_PERMISO:Integer:set:label=Clase del permiso:set:profile=DAL.SelectableForeingKey:tag:DAL.foreingTable=ARENA2_CLASE_PERMISO:tag:DAL.foreingCode=ID:tag:DAL.foreingLabel=FORMAT('%02d - %s',ID,DESCRIPCION)",
      "FECHA_PERMISO:Date:set:label=Fecha permiso",

      #ACCESORIOS_SEGURIDAD
      "ACC_SEG_CINTURON:Boolean:set:label=Cinturon",
      "ACC_SEG_CASCO:Integer:set:label=Casco:set:profile=DAL.SelectableForeingKey:tag:DAL.foreingTable=ARENA2_ ACC_SEG_CASCO:tag:DAL.foreingCode=ID:tag:DAL.foreingLabel=FORMAT('%02d - %s',ID,DESCRIPCION)",

      #ACCESORIOS_SEGURIDAD_OPCIONALES
      "ACC_SEG_BRAZOS:Boolean:set:label=Brazos",
      "ACC_SEG_ESPALDA:Boolean:set:label=Espalda",
      "ACC_SEG_TORSO:Boolean:set:label=Torso",
      "ACC_SEG_MANOS:Boolean:set:label=Manos",
      "ACC_SEG_PIERNAS:Boolean:set:label=Piernas",
      "ACC_SEG_PIES:Boolean:set:label=Pies",
      "ACC_SEG_PRENDA_REF:Boolean",

      # ALCOHOL
      "INFLU_ALCOHOL:Boolean",
      "PRUEBA_ALCOHOLEMIA:Integer",
      "TASA_ALCOHOLEMIA1:Integer",
      "TASA_ALCOHOLEMIA2:Integer",
      "PRUEBA_ALC_SANGRE:Boolean",
      "SIGNOS_INFLU_ALCOHOL:Boolean",

      # DROGAS
      "INFLU_DROGAS:Boolean",
      "PRUEBA_DROGAS:Integer:set:label=Prueba drogas:set:profile=DAL.SelectableForeingKey:tag:DAL.foreingTable=ARENA2_ PRUEBA_DROGAS:tag:DAL.foreingCode=ID:tag:DAL.foreingLabel=FORMAT('%02d - %s',ID,DESCRIPCION)",
      "AMP:Boolean",
      "CONFIRMADO_AMP:Boolean",
      "BDZ:Boolean",
      "CONFIRMADO_BDZ:Boolean",
      "COC:Boolean",
      "CONFIRMADO_COC:Boolean",
      "THC:Boolean",
      "CONFIRMADO_THC:Boolean",
      "METH:Boolean",
      "CONFIRMADO_METH:Boolean",
      "OPI:Boolean",
      "CONFIRMADO_OPI:Boolean",
      "OTRAS:Boolean",
      "CONFIRMADO_OTRAS:Boolean",
      "SIGNOS_INFLU_DROGAS:Boolean",
      
      "MOTIVO_DESPLAZAMIENTO:Integer:set:label=Motivo desplazamiento:set:profile=DAL.SelectableForeingKey:tag:DAL.foreingTable=ARENA2_MOTIVO_DESPLAZA_COND:tag:DAL.foreingCode=ID:tag:DAL.foreingLabel=FORMAT('%02d - %s',ID,DESCRIPCION)",
      "DESPLAZAMIENTO_PREVISTO:Integer:set:label=Desplazamiento previsto:set:profile=DAL.SelectableForeingKey:tag:DAL.foreingTable=ARENA2_DESPLAZAMIENTO_PREVISTO:tag:DAL.foreingCode=ID:tag:DAL.foreingLabel=FORMAT('%02d - %s',ID,DESCRIPCION)",

      # INFRACIONES
      "INFLU_PRES_INFRAC_COND:Boolean",
      "PRES_INFRAC_COND:Integer",
      "PRES_INFRAC_SIN_LUCES:Boolean",
      "PRES_INFRAC_SIN_TRIANGULO:Boolean",

      # PRES_INFRAC_VEL_COND
      "INFLU_PRES_INFRAC_VEL:Boolean",
      "PRES_INFRAC_VEL_COND:Integer",

      # OTRA_INFRAC_COND
      "INFLU_OTRA_INFRAC:Boolean",
      "OTRA_INFRAC_COND_TIPO:Integer",
      
      "POSIBLE_RESPONSABLE:Boolean",

      # FACTORES_ATENCION
      "INFLU_FACT_ATENCION:Boolean",
      "FACTORES_ATENCION:Integer",
      
      # PRESUNTOS_ERRORES
      "INFLU_PRES_ERROR:Boolean",
      "PRESUNTOS_ERRORES:Integer"
    ]
    return columns
    
  def read(self):
    conductor = self.next()
    if conductor == None:
      return None
      
    values = [ None ] * 61
    # LID_CONDUCTOR
    values[ 0] = get1(conductor,"@ID_ACCIDENTE") +"/"+ get1(conductor,"@ID_VEHICULO")
    
    values[ 1] = get1(conductor,"@ID_ACCIDENTE")
    # LID_VEHICULO
    values[ 2] = get1(conductor,"@ID_ACCIDENTE") +"/"+ get1(conductor,"@ID_VEHICULO")

    values[ 3] = get1(conductor,"@ID_VEHICULO")
      
    values[ 4] = get1(conductor,"FECHA_NACIMIENTO")
    values[ 5] = null2zero(get1(conductor,"SEXO"))
    values[ 6] = get1(conductor,"NACIONALIDAD")
    values[ 7] = get1(conductor,"PAIS_RESIDENCIA")
    values[ 8] = get1(conductor,"PROVINCIA_RESIDENCIA")
    values[ 9] = get1(conductor,"MUNICIPIO_RESIDENCIA")
    values[10] = null2zero(get1(conductor,"ASISTENCIA_SANITARIA"))
    
    values[11] = null2zero(get1(conductor,"CARACT_PERMISO"))
    values[12] = null2zero(get1(conductor,"CLASE_PERMISO"))
    values[13] = get1(conductor,"FECHA_PERMISO")

    values[14] = sino2bool(get2(conductor,"ACCESORIOS_SEGURIDAD","ACC_SEG_CINTURON"))
    values[15] = null2zero(get2(conductor,"ACCESORIOS_SEGURIDAD","ACC_SEG_CASCO"))

    values[16] = sino2bool(get2(conductor,"ACCESORIOS_SEGURIDAD_OPCIONALES","ACC_SEG_BRAZOS"))
    values[17] = sino2bool(get2(conductor,"ACCESORIOS_SEGURIDAD_OPCIONALES","ACC_SEG_ESPALDA"))
    values[18] = sino2bool(get2(conductor,"ACCESORIOS_SEGURIDAD_OPCIONALES","ACC_SEG_TORSO"))
    values[19] = sino2bool(get2(conductor,"ACCESORIOS_SEGURIDAD_OPCIONALES","ACC_SEG_MANOS"))
    values[20] = sino2bool(get2(conductor,"ACCESORIOS_SEGURIDAD_OPCIONALES","ACC_SEG_PIERNAS"))
    values[21] = sino2bool(get2(conductor,"ACCESORIOS_SEGURIDAD_OPCIONALES","ACC_SEG_PIES"))
    values[22] = sino2bool(get2(conductor,"ACCESORIOS_SEGURIDAD_OPCIONALES","ACC_SEG_PRENDA_REF"))

    values[23] = sino2bool(get2(conductor,"ALCOHOL","@INFLU_ALCOHOL"))
    values[24] = null2zero(get2(conductor,"ALCOHOL","PRUEBA_ALCOHOLEMIA"))
    values[25] = null2zero(get2(conductor,"ALCOHOL","TASA_ALCOHOLEMIA1"))
    values[26] = null2zero(get2(conductor,"ALCOHOL","TASA_ALCOHOLEMIA2"))
    values[27] = sino2bool(get2(conductor,"ALCOHOL","PRUEBA_ALC_SANGRE"))
    values[28] = sino2bool(get2(conductor,"ALCOHOL","SIGNOS_INFLU_ALCOHOL"))

    values[29] = sino2bool(get2(conductor,"DROGAS","@INFLU_DROGAS"))
    values[30] = null2zero(get2(conductor,"DROGAS","PRUEBA_DROGAS"))
    values[31] = sino2bool(get2(conductor,"DROGAS","AMP"))
    values[32] = sino2bool(get2(conductor,"DROGAS","CONFIRMADO_AMP"))
    values[33] = sino2bool(get2(conductor,"DROGAS","BDZ"))
    values[34] = sino2bool(get2(conductor,"DROGAS","CONFIRMADO_BDZ"))
    values[35] = sino2bool(get2(conductor,"DROGAS","COC"))
    values[36] = sino2bool(get2(conductor,"DROGAS","CONFIRMADO_COC"))
    values[37] = sino2bool(get2(conductor,"DROGAS","THC"))
    values[38] = sino2bool(get2(conductor,"DROGAS","CONFIRMADO_THC"))
    values[39] = sino2bool(get2(conductor,"DROGAS","METH"))
    values[40] = sino2bool(get2(conductor,"DROGAS","CONFIRMADO_METH"))
    values[41] = sino2bool(get2(conductor,"DROGAS","OPI"))
    values[42] = sino2bool(get2(conductor,"DROGAS","CONFIRMADO_OPI"))
    values[43] = sino2bool(get2(conductor,"DROGAS","OTRAS"))
    values[44] = sino2bool(get2(conductor,"DROGAS","CONFIRMADO_OTRAS"))
    values[45] = sino2bool(get2(conductor,"DROGAS","SIGNOS_INFLU_DROGAS"))

    values[46] = null2zero(get1(conductor,"MOTIVO_DESPLAZAMIENTO"))
    values[47] = null2zero(get1(conductor,"DESPLAZAMIENTO_PREVISTO"))

    values[48] = sino2bool(get2(conductor,"INFRACIONES","@INFLU_PRES_INFRAC_COND"))
    values[49] = null2zero(get2(conductor,"INFRACIONES","PRES_INFRAC_COND"))
    values[50] = sino2bool(get2(conductor,"INFRACIONES","PRES_INFRAC_SIN_LUCES"))
    values[51] = sino2bool(get2(conductor,"INFRACIONES","PRES_INFRAC_SIN_TRIANGULO"))
    
    values[52] = sino2bool(get2(conductor,"PRES_INFRAC_VEL_COND","@INFLU_PRES_INFRAC_VEL"))
    values[53] = null2zero(get2(conductor,"PRES_INFRAC_VEL_COND","#text"))

    values[54] = sino2bool(get2(conductor,"OTRA_INFRAC_COND","@INFLU_OTRA_INFRAC"))
    values[55] = null2zero(get2(conductor,"OTRA_INFRAC_COND","@TIPO"))

    values[56] = sino2bool(get1(conductor,"POSIBLE_RESPONSABLE"))

    values[57] = sino2bool(get2(conductor,"FACTORES_ATENCION","@INFLU_FACT_ATENCION"))
    values[58] = null2zero(get2(conductor,"FACTORES_ATENCION","#text"))

    values[59] = sino2bool(get2(conductor,"PRESUNTOS_ERRORES","@INFLU_PRES_ERROR"))
    values[60] = null2zero(get2(conductor,"PRESUNTOS_ERRORES","#text"))
  
    return values

  def next(self):
    if self.informeCorriente == None:
      return None
    
    informes = self.getInformes()
    while self.informeCorriente < len(informes):
      informe = informes[self.informeCorriente]
      #print "Informe: ", get1(informe,"@COD_INFORME"), self.informeCorriente
      accidentes = self.getAccidentes(informe)
      while self.accidenteCorriente < len(accidentes):
        accidente = accidentes[self.accidenteCorriente]
        #print "Accidente: ", get1(accidente,"@ID_ACCIDENTE"), self.accidenteCorriente
        vehiculos = self.getVehiculos(accidente)
        while self.vehiculoCorriente < len(vehiculos) :
          vehiculo = vehiculos[self.vehiculoCorriente]
          #print "Vehiculo: ", get1(vehiculo,"@ID_ACCIDENTE")+"/"+get1(vehiculo,"@ID_VEHICULO"), self.vehiculoCorriente
          conductor = vehiculo.get("CONDUCTOR",None)
          if conductor!=None:
            #print "Conductor: ", get1(conductor,"@ID_ACCIDENTE")+"/"+get1(conductor,"@ID_VEHICULO")
            self.vehiculoCorriente += 1
            return conductor
          self.vehiculoCorriente += 1
        
        self.accidenteCorriente += 1
        self.vehiculoCorriente = 0

      self.informeCorriente += 1
      self.accidenteCorriente = 0
      self.vehiculoCorriente = 0

    self.informeCorriente = None
    return None
