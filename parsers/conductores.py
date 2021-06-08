# encoding: utf-8

import gvsig
import sys

from org.gvsig.fmap.geom.aggregate import MultiPolygon
from org.gvsig.scripting.app.extension import ScriptingUtils
import xmltodic
from org.gvsig.fmap.geom import GeometryUtils

from util import parseToBool, parseToString, parseToNumber, get1, get2, Descriptor, generate_translations, parseToNull

COLUMNS_DEFINITION = [
  Descriptor("LID_CONDUCTOR","String",30,hidden=True, pk=True,
    label="_Id_conduct")\
    .tag("dynform.readonly",True),
  Descriptor("ID_ACCIDENTE","String",20,
    label="_Accidente")\
    .set("relation","Collaboration")\
    .foreingkey("ARENA2_ACCIDENTES","ID_ACCIDENTE","FORMAT('%s',ID_ACCIDENTE)")\
    .tag("dynform.readonly",True),
    
  Descriptor("LID_VEHICULO","String",20,
    label="_Vehiculo")\
    .set("relation","Collaboration")\
    .foreingkey(
      "ARENA2_VEHICULOS",
      "LID_VEHICULO",
      "FORMAT('%s/%s %s %s %s %s',ID_ACCIDENTE,ID_VEHICULO,TIPO_VEHICULO,NACIONALIDAD,MARCA_NOMBRE,MODELO)"
     )\
    .tag("dynform.readonly",True),
  Descriptor("ID_VEHICULO","String",5, hidden=True,
    label="_Id_vehiculo")\
    .tag("dynform.readonly",True),
  
  Descriptor("POSIBLE_RESPONSABLE","Boolean",
    label="_Posible_responsable",
    shortlabel="_Responsable",)\
    .tag("dynform.readonly",True),

  # Seccion: Datos personales
  Descriptor("FECHA_NACIMIENTO","Date",
    label="_Fecha_nacimiento")\
    .tag("dynform.readonly",True)\
    .tag("dynform.separator","_Datos_personales"),
  Descriptor("SEXO","Integer",
    label="_Sexo")\
    .set("relation","Collaboration")\
    .closedlistfk("ARENA2_DIC_SEXO")\
    .tag("dynform.readonly",True),
  Descriptor("NACIONALIDAD","String", size=100,
    label="_Nacionalidad")\
    .tag("dynform.readonly",True),
  Descriptor("PAIS_RESIDENCIA","String", size=100,
    label="_Pais_de_residencia",
    shortlabel="_Pais_resi")\
    .tag("dynform.readonly",True),
  Descriptor("PROVINCIA_RESIDENCIA","String", size=100,
    label="_Provincia_de_residencia",
    shortlabel="_Prov_resi")\
    .tag("dynform.readonly",True),
  Descriptor("MUNICIPIO_RESIDENCIA","String", size=100,
    label="_Municipio_de_residencia",
    shortlabel="_Muni_resi")\
    .tag("dynform.readonly",True),
  Descriptor("ASISTENCIA_SANITARIA","Integer",
    label="_Asistencia_sanitaria",
    shortlabel="_Asis_sanitaria")\
    .set("relation","Collaboration")\
    .closedlistfk("ARENA2_DIC_ASISTENCIA_SANITARIA")\
    .tag("dynform.readonly",True),

  # Seccion: Posibles errores
  Descriptor("INFLU_FACT_ATENCION","Boolean",
    label="_Influyen_factores_atencion",
    shortlabel="_Infl_fact_atencion")\
    .tag("dynform.readonly",True)\
    .tag("dynform.separator","_Posibles_errores"),
  Descriptor("FACTORES_ATENCION","Integer",
    label="_Factores_afectan_atencion",
    shortlabel="_Fact_atencion")\
    .set("relation","Collaboration")\
    .closedlistfk("ARENA2_DIC_FACTORES_ATENCION_COND")\
    .tag("dynform.readonly",True),
  
  Descriptor("INFLU_PRES_ERROR","Boolean",
    label="_Influyen_presuntos_errores",
    shortlabel="_Influ_errores")\
    .tag("dynform.readonly",True),
  Descriptor("PRESUNTOS_ERRORES","Integer",
    label="_Presuntos_errores",
    shortlabel="_Errores")\
    .set("relation","Collaboration")\
    .closedlistfk("ARENA2_DIC_ERRORES_COND")\
    .tag("dynform.readonly",True),

  # Seccion: Permiso
  Descriptor("CARACT_PERMISO","Integer",
    label="_Caracteristicas_del_permiso",
    shortlabel="_Carac_permiso")\
    .set("relation","Collaboration")\
    .closedlistfk("ARENA2_DIC_CARACTERISTICAS_PERMISO")\
    .tag("dynform.readonly",True)\
    .tag("dynform.separator","_Permiso"),
  Descriptor("CLASE_PERMISO","Integer",
    label="_Clase_del_permiso",
    shortlabel="_Clase_perm")\
    .set("relation","Collaboration")\
    .closedlistfk("ARENA2_DIC_CLASE_PERMISO")\
    .tag("dynform.readonly",True),
  Descriptor("FECHA_PERMISO","Date",
    label="_Fecha_permiso",
    shortlabel="_Fech_perm")\
    .tag("dynform.readonly",True),

  # Seccion: Desplazamiento
  Descriptor("MOTIVO_DESPLAZAMIENTO","Integer",
    label="_Motivo_desplazamiento",
    shortlabel="_Motivo_despl")\
    .set("relation","Collaboration")\
    .closedlistfk("ARENA2_DIC_MOTIVO_DESPLAZA_COND")\
    .tag("dynform.readonly",True)\
    .tag("dynform.separator","_Desplazamiento"),
  Descriptor("DESPLAZAMIENTO_PREVISTO","Integer",
    label="_Desplazamiento_previsto",
    shortlabel="_Despl_prev")\
    .set("relation","Collaboration")\
    .closedlistfk("ARENA2_DIC_DESPLAZAMIENTO_PREVISTO")\
    .tag("dynform.readonly",True),

  # Grupo: Accesorios de seguridad
  Descriptor("ACC_SEG_CINTURON","Boolean",
    group="_Accesorios_de_seguridad",
    label="_Cinturon")\
    .tag("dynform.readonly",True),
  Descriptor("ACC_SEG_CASCO","Integer",
    group="_Accesorios_de_seguridad",
    label="_Casco")\
    .set("relation","Collaboration")\
    .closedlistfk("ARENA2_DIC_ACC_SEG_CASCO")\
    .tag("dynform.readonly",True),
  # Seccion: Accesorios de seguridad opcionales
  Descriptor("ACC_SEG_BRAZOS","Boolean",
    group="_Accesorios_de_seguridad",
    label="_Brazos")\
    .tag("dynform.separator","_Accesorios_de_seguridad_opcionales")\
    .tag("dynform.readonly",True),
  Descriptor("ACC_SEG_ESPALDA","Boolean",
    group="_Accesorios_de_seguridad",
    label="_Espalda")\
    .tag("dynform.readonly",True),
  Descriptor("ACC_SEG_TORSO","Boolean",
    group="_Accesorios_de_seguridad",
    label="_Torso")\
    .tag("dynform.readonly",True),
  Descriptor("ACC_SEG_MANOS","Boolean",
    group="_Accesorios_de_seguridad",
    label="_Manos")\
    .tag("dynform.readonly",True),
  Descriptor("ACC_SEG_PIERNAS","Boolean",
    group="_Accesorios_de_seguridad",
    label="_Piernas")\
    .tag("dynform.readonly",True),
  Descriptor("ACC_SEG_PIES","Boolean",
    group="_Accesorios_de_seguridad",
    label="_Pies")\
    .tag("dynform.readonly",True),
  Descriptor("ACC_SEG_PRENDA_REF","Boolean",
    group="_Accesorios_de_seguridad",
    label="_Prenda_reflectante",
    shortlabel="_Prenda_refl")\
    .tag("dynform.readonly",True),

  # Grupo: Pruebas
  # Seccion: Alcohol
  Descriptor("INFLU_ALCOHOL","Boolean",
    group="_Pruebas",
    label="_Influye_el_alcohol",
    shortlabel="_Influ_alcohol")\
    .tag("dynform.separator","_Prueba_de_alcohol")\
    .tag("dynform.readonly",True),
  Descriptor("PRUEBA_ALCOHOLEMIA","Integer",
    group="_Pruebas",
    label="_Prueba_en_aire",
    shortlabel="_Prueba_aire")\
    .set("relation","Collaboration")\
    .closedlistfk("ARENA2_DIC_PRUEBA_ALCOHOLEMIA")\
    .tag("dynform.readonly",True),
  Descriptor("TASA_ALCOHOLEMIA1","Integer",
    group="_Pruebas",
    label="_Tasa_1_en_aire_mg_l",
    shortlabel="_Tasa_1")\
    .tag("dynform.readonly",True),
  Descriptor("TASA_ALCOHOLEMIA2","Integer",
    group="_Pruebas",
    label="_Tasa_2_en_aire_mg_l",
    shortlabel="_Tasa_2")\
    .tag("dynform.readonly",True),
  Descriptor("PRUEBA_ALC_SANGRE","Boolean",
    group="_Pruebas",
    label="_Prueba_en_sangre",
    shortlabel="_Prueba_sang")\
    .tag("dynform.readonly",True),
  Descriptor("SIGNOS_INFLU_ALCOHOL","Boolean",
    group="_Pruebas",
    label="_Signos_de_influencia_del_alcohol",
    shortlabel="_Signos_infl_alcohol")\
    .tag("dynform.readonly",True),
  # Seccion: Drogas
  Descriptor("INFLU_DROGAS","Boolean",
    group="_Pruebas",
    label="_Influyen_las_drogas",
    shortlabel="_Influ_drogas")\
    .tag("dynform.separator","_Prueba_de_drogas")\
    .tag("dynform.readonly",True),
  Descriptor("PRUEBA_DROGAS","Integer",
    group="_Pruebas",
    label="_Prueba_de_drogas",
    shortlabel="_Prueba_drogas")\
    .set("relation","Collaboration")\
    .closedlistfk("ARENA2_DIC_PRUEBA_DROGAS")\
    .tag("dynform.readonly",True),
  Descriptor("AMP","Boolean",
    group="_Pruebas",
    label="_Positivo_anfetaminas",
    shortlabel="_Anfetaminas")\
    .tag("dynform.readonly",True),
  Descriptor("CONFIRMADO_AMP","Boolean",
    group="_Pruebas",
    label="_Confirmado_anfetaminas",
    shortlabel="_Conf_anfeta")\
    .tag("dynform.readonly",True),
  Descriptor("BDZ","Boolean",
    group="_Pruebas",
    label="_Positivo_benzodiacepinas",
    shortlabel="_Benzodiacepinas")\
    .tag("dynform.readonly",True),
  Descriptor("CONFIRMADO_BDZ","Boolean",
    group="_Pruebas",
    label="_Confirmado_benzodiacepinas",
    shortlabel="_Conf_benzo")\
    .tag("dynform.readonly",True),
  Descriptor("COC","Boolean",
    group="_Pruebas",
    label="_Positivo_cocaina",
    shortlabel="_Cocaina")\
    .tag("dynform.readonly",True),
  Descriptor("CONFIRMADO_COC","Boolean",
    group="_Pruebas",
    label="_Confirmado_cocaina",
    shortlabel="_Conf_cocaina")\
    .tag("dynform.readonly",True),
  Descriptor("THC","Boolean",
    group="_Pruebas",
    label="_Positivo_cannabis_y_derivados",
    shortlabel="_Cannabis")\
    .tag("dynform.readonly",True),
  Descriptor("CONFIRMADO_THC","Boolean",
    group="_Pruebas",
    label="_Confirmado_cannabis_y_derivados",
    shortlabel="_Conf_cannabis")\
    .tag("dynform.readonly",True),
  Descriptor("METH","Boolean",
    group="_Pruebas",
    label="_Positivo_metanfetaminas",
    shortlabel="_Metanfetaminas")\
    .tag("dynform.readonly",True),
  Descriptor("CONFIRMADO_METH","Boolean",
    group="_Pruebas",
    label="_Confirmado_metanfetaminas",
    shortlabel="_Conf_metanf")\
    .tag("dynform.readonly",True),
  Descriptor("OPI","Boolean",
    group="_Pruebas",
    label="_Positivo_opiaceos",
    shortlabel="_Opiaceos")\
    .tag("dynform.readonly",True),
  Descriptor("CONFIRMADO_OPI","Boolean",
    group="_Pruebas",
    label="_Confirmado_opiaceos",
    shortlabel="_Conf_opiaceos")\
    .tag("dynform.readonly",True),
  Descriptor("OTRAS","Boolean",
    group="_Pruebas",
    label="_Positivo_benzodiacepinas",
    shortlabel="_Benzodiacepinas")\
    .tag("dynform.readonly",True),
  Descriptor("CONFIRMADO_OTRAS","Boolean",
    group="_Pruebas",
    label="_Confirmado_otra_sustancias",
    shortlabel="_Conf_otra")\
    .tag("dynform.readonly",True),
  Descriptor("SIGNOS_INFLU_DROGAS","Boolean",
    group="_Pruebas",
    label="_Signos_de_influencia_de_drogas",
    shortlabel="_Signos_infl_drogas")\
    .tag("dynform.readonly",True),
  
  # Grupo: Presuntas infracciones
  Descriptor("INFLU_PRES_INFRAC_COND","Boolean",
    group="_Presuntas_infracciones",
    label="_Influyen_las_infracciones_del_conductor",
    shortlabel="_Influ_infrac_cond")\
    .tag("dynform.readonly",True),
  Descriptor("PRES_INFRAC_COND","Integer",
    group="_Presuntas_infracciones",
    label="_Presuntas_infracciones_del_conductor",
    shortlabel="_Infrac_cond")\
    .set("relation","Collaboration")\
    .closedlistfk("ARENA2_DIC_INFRACCIONES_CODUCTOR")\
    .tag("dynform.readonly",True),
  Descriptor("PRES_INFRAC_SIN_LUCES","Boolean",
    group="_Presuntas_infracciones",
    label="_Sin_luces_de_emergencia",
    shortlabel="_Sin_luces")\
    .tag("dynform.readonly",True),
  Descriptor("PRES_INFRAC_SIN_TRIANGULO","Boolean",
    group="_Presuntas_infracciones",
    label="_Sin_triangulo_de_presenalizacion",
    shortlabel="_Sin_triangulo")\
    .tag("dynform.readonly",True),
  Descriptor("INFLU_PRES_INFRAC_VEL","Boolean",
    group="_Presuntas_infracciones",
    label="_Influye_infraccion_velocidad",
    shortlabel="_Infl_velocidad")\
    .tag("dynform.readonly",True),
  Descriptor("PRES_INFRAC_VEL_COND","Integer",
    group="_Presuntas_infracciones",
    label="_Presuntas_infracciones_de_velocidad",
    shortlabel="_Infrac_veloc")\
    .tag("dynform.readonly",True)\
    .set("relation","Collaboration")\
    .closedlistfk("ARENA2_DIC_INFRACCIONES_VELOCIDAD"),
  Descriptor("INFLU_OTRA_INFRAC","Boolean",
    group="_Presuntas_infracciones",
    label="_Influye_otra_infraccion",
    shortlabel="_Infl_otra")\
    .tag("dynform.readonly",True),
  Descriptor("OTRA_INFRAC_COND","Integer",
    group="_Presuntas_infracciones",
    label="_Otra_infraccion",
    shortlabel="_Infrac_otra")\
    .tag("dynform.readonly",True)\
    .set("relation","Collaboration")\
    .closedlistfk("ARENA2_DIC_INFRACCIONES_OTRAS")
]

class ConductoresParser(object):
  
  def __init__(self, fname, xml=None):
    self.fname = fname
    self.xml = xml
    self.informeCorriente = None
    self.accidenteCorriente = None
    self.vehiculoCorriente = None
    self.tags = {}
    
  def getParserTags(self):
    return self.tags
    
  def close(self):
    self.xml = None
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
    accidentes = informe["ACCIDENTES"]
    if accidentes==None:
      return tuple()
    accidentes = accidentes.get('ACCIDENTE',None)
    if accidentes==None:
      return tuple()
    if not isinstance(accidentes,list):
      accidentes = [ accidentes ]
    return accidentes

  def getVehiculos(self, accidente):
    vehiculos = accidente["VEHICULOS"]
    if vehiculos==None:
      return tuple()
    vehiculos = vehiculos.get('VEHICULO',None)
    if vehiculos==None:
      return tuple()
    if not isinstance(vehiculos,list):
      vehiculos = [ vehiculos ]
    return vehiculos

  def getColumns(self):
    return COLUMNS_DEFINITION

  def getRowCount(self):
    self.rewind()
    rowCount = 0
    while True:
      row = self.next()
      if row == None:
        return rowCount
      #conductor_id = get1(row,"@ID_ACCIDENTE") +"/"+ get1(row,"@ID_VEHICULO")
      #print "Conductor: ", conductor_id
      rowCount+=1
    
  def read(self):
    conductor = self.next()
    if conductor == None:
      return None
      
    values = []
    conductor_id = None
    try:
      conductor_id = get1(conductor,"@ID_ACCIDENTE") +"/"+ get1(conductor,"@ID_VEHICULO")
      
      # LID_CONDUCTOR
      values.append(conductor_id)
      
      values.append(get1(conductor,"@ID_ACCIDENTE"))
      # LID_VEHICULO
      values.append(get1(conductor,"@ID_ACCIDENTE") +"/"+ get1(conductor,"@ID_VEHICULO"))
      
      values.append(get1(conductor,"@ID_VEHICULO"))
            
      values.append(parseToBool(get1(conductor,"POSIBLE_RESPONSABLE")))
      
      values.append(get1(conductor,"FECHA_NACIMIENTO"))
      values.append(parseToNull(get1(conductor,"SEXO")))
      values.append(get1(conductor,"NACIONALIDAD"))
      values.append(get1(conductor,"PAIS_RESIDENCIA"))
      values.append(get1(conductor,"PROVINCIA_RESIDENCIA"))
      values.append(get1(conductor,"MUNICIPIO_RESIDENCIA"))
      values.append(parseToNull(get1(conductor,"ASISTENCIA_SANITARIA")))
          
      values.append(parseToBool(get2(conductor,"FACTORES_ATENCION","@INFLU_FACT_ATENCION")))
      values.append(parseToNull(get2(conductor,"FACTORES_ATENCION","#text")))
      
      values.append(parseToBool(get2(conductor,"PRESUNTOS_ERRORES","@INFLU_PRES_ERROR")))
      values.append(parseToNull(get2(conductor,"PRESUNTOS_ERRORES","#text")))
        
      values.append(parseToNull(get1(conductor,"CARACT_PERMISO")))
      values.append(parseToNull(get1(conductor,"CLASE_PERMISO")))
      values.append(get1(conductor,"FECHA_PERMISO"))
      
      values.append(parseToNull(get1(conductor,"MOTIVO_DESPLAZAMIENTO")))
      values.append(parseToNull(get1(conductor,"DESPLAZAMIENTO_PREVISTO")))
      
      values.append(parseToBool(get2(conductor,"ACCESORIOS_SEGURIDAD","ACC_SEG_CINTURON")))
      values.append(parseToNull(get2(conductor,"ACCESORIOS_SEGURIDAD","ACC_SEG_CASCO")))
      values.append(parseToBool(get2(conductor,"ACCESORIOS_SEGURIDAD_OPCIONALES","ACC_SEG_BRAZOS")))
      values.append(parseToBool(get2(conductor,"ACCESORIOS_SEGURIDAD_OPCIONALES","ACC_SEG_ESPALDA")))
      values.append(parseToBool(get2(conductor,"ACCESORIOS_SEGURIDAD_OPCIONALES","ACC_SEG_TORSO")))
      values.append(parseToBool(get2(conductor,"ACCESORIOS_SEGURIDAD_OPCIONALES","ACC_SEG_MANOS")))
      values.append(parseToBool(get2(conductor,"ACCESORIOS_SEGURIDAD_OPCIONALES","ACC_SEG_PIERNAS")))
      values.append(parseToBool(get2(conductor,"ACCESORIOS_SEGURIDAD_OPCIONALES","ACC_SEG_PIES")))
      values.append(parseToBool(get2(conductor,"ACCESORIOS_SEGURIDAD_OPCIONALES","ACC_SEG_PRENDA_REF")))
      
      values.append(parseToBool(get2(conductor,"ALCOHOL","@INFLU_ALCOHOL")))
      values.append(parseToNull(get2(conductor,"ALCOHOL","PRUEBA_ALCOHOLEMIA")))
      values.append(parseToNumber(get2(conductor,"ALCOHOL","TASA_ALCOHOLEMIA1")))
      values.append(parseToNumber(get2(conductor,"ALCOHOL","TASA_ALCOHOLEMIA2")))
      values.append(parseToBool(get2(conductor,"ALCOHOL","PRUEBA_ALC_SANGRE")))
      values.append(parseToBool(get2(conductor,"ALCOHOL","SIGNOS_INFLU_ALCOHOL")))
      
      values.append(parseToBool(get2(conductor,"DROGAS","@INFLU_DROGAS")))
      values.append(parseToNull(get2(conductor,"DROGAS","PRUEBA_DROGAS")))
      values.append(parseToBool(get2(conductor,"DROGAS","AMP")))
      values.append(parseToBool(get2(conductor,"DROGAS","CONFIRMADO_AMP")))
      values.append(parseToBool(get2(conductor,"DROGAS","BDZ")))
      values.append(parseToBool(get2(conductor,"DROGAS","CONFIRMADO_BDZ")))
      values.append(parseToBool(get2(conductor,"DROGAS","COC")))
      values.append(parseToBool(get2(conductor,"DROGAS","CONFIRMADO_COC")))
      values.append(parseToBool(get2(conductor,"DROGAS","THC")))
      values.append(parseToBool(get2(conductor,"DROGAS","CONFIRMADO_THC")))
      values.append(parseToBool(get2(conductor,"DROGAS","METH")))
      values.append(parseToBool(get2(conductor,"DROGAS","CONFIRMADO_METH")))
      values.append(parseToBool(get2(conductor,"DROGAS","OPI")))
      values.append(parseToBool(get2(conductor,"DROGAS","CONFIRMADO_OPI")))
      values.append(parseToBool(get2(conductor,"DROGAS","OTRAS")))
      values.append(parseToBool(get2(conductor,"DROGAS","CONFIRMADO_OTRAS")))
      values.append(parseToBool(get2(conductor,"DROGAS","SIGNOS_INFLU_DROGAS")))
      
      values.append(parseToBool(get2(conductor,"INFRACIONES","@INFLU_PRES_INFRAC_COND")))
      values.append(parseToNull(get2(conductor,"INFRACIONES","PRES_INFRAC_COND")))
      values.append(parseToBool(get2(conductor,"INFRACIONES","PRES_INFRAC_SIN_LUCES")))
      values.append(parseToBool(get2(conductor,"INFRACIONES","PRES_INFRAC_SIN_TRIANGULO")))
          
      values.append(parseToBool(get2(conductor,"PRES_INFRAC_VEL_COND","@INFLU_PRES_INFRAC_VEL")))
      values.append(parseToNull(get2(conductor,"PRES_INFRAC_VEL_COND","#text")))
      
      values.append(parseToBool(get2(conductor,"OTRA_INFRAC_COND","@INFLU_OTRA_INFRAC")))
      values.append(parseToNumber(get2(conductor,"OTRA_INFRAC_COND","@TIPO")))
    
    except:
      ex = sys.exc_info()[1]
      gvsig.logger("No se puede leer el conductor %s. %s" % (conductor_id,str(ex)), gvsig.LOGGER_WARN, ex)
      raise
    
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

def main(*args):
  generate_translations(COLUMNS_DEFINITION)
  
