# encoding: utf-8

import gvsig

from org.gvsig.fmap.geom.aggregate import MultiPolygon
from org.gvsig.scripting.app.extension import ScriptingUtils
import xmltodic
from org.gvsig.fmap.geom import GeometryUtils

from util import sino2bool, null2empty, null2zero, get1, get2, Descriptor

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
      Descriptor("LID_CONDUCTOR","String",20,hidden=True, pk=True).build(),
      Descriptor("ID_ACCIDENTE","String",20,label="Accidente")\
        .foreingkey("ARENA2_ACCIDENTES","ID_ACCIDENTE","FORMAT('%s',ID_ACCIDENTE)")\
        .build(),
      Descriptor("LID_VEHICULO","String",20,label="Vehiculo")\
        .foreingkey("ARENA2_VEHICULOS","LID_VEHICULO","FORMAT('%s/%s %s %s %s %s',ID_ACCIDENTE,ID_VEHICULO,TIPO_VEHICULO,NACIONALIDAD,MARCA_NOMBRE,MODELO)")\
        .build(),
      Descriptor("ID_VEHICULO","String",5, hidden=True).build(),
      
      Descriptor("FECHA_NACIMIENTO","Date",label="Fecha nacimiento").build(),
      Descriptor("SEXO","Integer",label="Sexo")\
        .selectablefk("ARENA2_DIC_SEXO")\
        .build(),
      Descriptor("NACIONALIDAD","String", size=100,label="Nacionalidad").build(),
      Descriptor("PAIS_RESIDENCIA","String", size=100,label="Pais de residencia").build(),
      Descriptor("PROVINCIA_RESIDENCIA","String", size=100,label="Provincia de residencia").build(),
      Descriptor("MUNICIPIO_RESIDENCIA","String", size=100,label="Municipio de residencia").build(),
      Descriptor("ASISTENCIA_SANITARIA","Integer",label="Asistencia sanitaria")\
        .selectablefk("ARENA2_DIC_ASISTENCIA_SANITARIA")\
        .build(),
      Descriptor("CARACT_PERMISO","Integer",label="Caracteristicas del permiso")\
        .selectablefk("ARENA2_DIC_CARACTERISTICAS_PERMISO")\
        .build(),
      Descriptor("CLASE_PERMISO","Integer",label="Clase del permiso")\
        .selectablefk("ARENA2_DIC_CLASE_PERMISO")\
        .build(),
      Descriptor("FECHA_PERMISO","Date",label="Fecha permiso").build(),

      #ACCESORIOS_SEGURIDAD
      Descriptor("ACC_SEG_CINTURON","Boolean",label="Cinturon").build(),
      Descriptor("ACC_SEG_CASCO","Integer",label="Casco")\
        .selectablefk("ARENA2_DIC_ACC_SEG_CASCO")\
        .build(),

      #ACCESORIOS_SEGURIDAD_OPCIONALES
      Descriptor("ACC_SEG_BRAZOS","Boolean",label="Brazos").build(),
      Descriptor("ACC_SEG_ESPALDA","Boolean",label="Espalda").build(),
      Descriptor("ACC_SEG_TORSO","Boolean",label="Torso").build(),
      Descriptor("ACC_SEG_MANOS","Boolean",label="Manos").build(),
      Descriptor("ACC_SEG_PIERNAS","Boolean",label="Piernas").build(),
      Descriptor("ACC_SEG_PIES","Boolean",label="Pies").build(),
      Descriptor("ACC_SEG_PRENDA_REF","Boolean").build(),

      # ALCOHOL
      Descriptor("INFLU_ALCOHOL","Boolean").build(),
      Descriptor("PRUEBA_ALCOHOLEMIA","Integer")
        .selectablefk("ARENA2_DIC_PRUEBA_ALCOHOLEMIA"),
      Descriptor("TASA_ALCOHOLEMIA1","Integer").build(),
      Descriptor("TASA_ALCOHOLEMIA2","Integer").build(),
      Descriptor("PRUEBA_ALC_SANGRE","Boolean").build(),
      Descriptor("SIGNOS_INFLU_ALCOHOL","Boolean").build(),

      # DROGAS
      Descriptor("INFLU_DROGAS","Boolean").build(),
      Descriptor("PRUEBA_DROGAS","Integer",label="Prueba drogas")\
        .selectablefk("ARENA2_DIC_PRUEBA_DROGAS")\
        .build(),
      Descriptor("AMP","Boolean").build(),
      Descriptor("CONFIRMADO_AMP","Boolean").build(),
      Descriptor("BDZ","Boolean").build(),
      Descriptor("CONFIRMADO_BDZ","Boolean").build(),
      Descriptor("COC","Boolean").build(),
      Descriptor("CONFIRMADO_COC","Boolean").build(),
      Descriptor("THC","Boolean").build(),
      Descriptor("CONFIRMADO_THC","Boolean").build(),
      Descriptor("METH","Boolean").build(),
      Descriptor("CONFIRMADO_METH","Boolean").build(),
      Descriptor("OPI","Boolean").build(),
      Descriptor("CONFIRMADO_OPI","Boolean").build(),
      Descriptor("OTRAS","Boolean").build(),
      Descriptor("CONFIRMADO_OTRAS","Boolean").build(),
      Descriptor("SIGNOS_INFLU_DROGAS","Boolean").build(),
      
      Descriptor("MOTIVO_DESPLAZAMIENTO","Integer",label="Motivo desplazamiento")\
        .selectablefk("ARENA2_DIC_MOTIVO_DESPLAZA_COND")\
        .build(),
      Descriptor("DESPLAZAMIENTO_PREVISTO","Integer",label="Desplazamiento previsto")\
        .selectablefk("ARENA2_DIC_DESPLAZAMIENTO_PREVISTO")\
        .build(),

      # INFRACIONES
      Descriptor("INFLU_PRES_INFRAC_COND","Boolean").build(),
      Descriptor("PRES_INFRAC_COND","Integer")\
        .selectablefk("ARENA2_DIC_INFRACCIONES_CODUCTOR"),
      Descriptor("PRES_INFRAC_SIN_LUCES","Boolean").build(),
      Descriptor("PRES_INFRAC_SIN_TRIANGULO","Boolean").build(),

      # PRES_INFRAC_VEL_COND
      Descriptor("INFLU_PRES_INFRAC_VEL","Boolean").build(),
      Descriptor("PRES_INFRAC_VEL_COND","Integer").build(),

      # OTRA_INFRAC_COND
      Descriptor("INFLU_OTRA_INFRAC","Boolean").build(),
      Descriptor("OTRA_INFRAC_COND_TIPO","Integer").build(),
      
      Descriptor("POSIBLE_RESPONSABLE","Boolean").build(),

      # FACTORES_ATENCION
      Descriptor("INFLU_FACT_ATENCION","Boolean").build(),
      Descriptor("FACTORES_ATENCION","Integer")\
        .selectablefk("ARENA2_DIC_FACTORES_ATENCION_COND"),
      
      # PRESUNTOS_ERRORES
      Descriptor("INFLU_PRES_ERROR","Boolean").build(),
      Descriptor("PRESUNTOS_ERRORES","Integer").build()
    ]
    return columns

  def getRowCount(self):
    self.rewind()
    rowCount = 0
    while True:
      row = self.next()
      if row == None:
        return rowCount
      rowCount+=1
    
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
