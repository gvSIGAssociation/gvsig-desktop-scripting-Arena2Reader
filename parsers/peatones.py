# encoding: utf-8

import gvsig

from org.gvsig.fmap.geom.aggregate import MultiPolygon
from org.gvsig.scripting.app.extension import ScriptingUtils
import xmltodic
from org.gvsig.fmap.geom import GeometryUtils

from util import sino2bool, null2empty, null2zero, get1, get2, Descriptor, generate_translations

COLUMNS_DEFINITION = [
  Descriptor("LID_PEATON","String",30,hidden=True, pk=True,
    label="_Id_peaton")\
    .tag("dynform.readonly",True),
  Descriptor("ID_ACCIDENTE","String",20,
    label="_Accidente")\
    .tag("dynform.readonly",True)\
    .set("relation","Collaboration")\
    .foreingkey("ARENA2_ACCIDENTES","ID_ACCIDENTE","FORMAT('%s',ID_ACCIDENTE)"),
  Descriptor("ID_PEATON","Integer", 
    label="_Codigo_peaton",
    shortlabel="_Cod_peaton")\
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
    .closedlistfk("ARENA2_DIC_FACTORES_ATENCION_PEA")\
    .tag("dynform.readonly",True),
  
  Descriptor("INFLU_PRES_ERROR","Boolean",
    label="_Influyen_presuntos_errores",
    shortlabel="_Influ_errores")\
    .tag("dynform.readonly",True),
  Descriptor("PRESUNTOS_ERRORES","Integer",
    label="_Presuntos_errores",
    shortlabel="_Errores")\
    .set("relation","Collaboration")\
    .closedlistfk("ARENA2_DIC_ERRORES_PEA")\
    .tag("dynform.readonly",True),
  
  Descriptor("INFLU_PRES_INFRAC","Boolean",
    label="_Influyen_presunta_infraccion",
    shortlabel="_Influ_infrac")\
    .tag("dynform.readonly",True),
  Descriptor("PRES_INFRAC_PEA","Integer",
    label="_Presunta_infraccion",
    shortlabel="_infraccion")\
    .tag("dynform.readonly",True)\
    .selectablefk("ARENA2_DIC_INFRACCIONES_PEATON"),

  # Seccion: Desplazamiento
  Descriptor("MOTIVO_DESPLAZAMIENTO","Integer",
    label="_Motivo_desplazamiento",
    shortlabel="_Motivo_despl")\
    .set("relation","Collaboration")\
    .closedlistfk("ARENA2_DIC_MOTIVO_DESPLAZA_PEA")\
    .tag("dynform.readonly",True)\
    .tag("dynform.separator","_Desplazamiento"),
  Descriptor("ACCION_PEA","Integer",
    label="_Accion_del_peaton",
    shortlabel="_Accion_pea")\
    .tag("dynform.readonly",True)\
    .set("relation","Collaboration")\
    .closedlistfk("ARENA2_DIC_ACCION_PEA"),

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
  
]

class PeatonesParser(object):
  
  def __init__(self, fname, xml=None):
    self.fname = fname
    self.xml = xml
    self.informeCorriente = None
    self.accidenteCorriente = None
    self.peatonCorriente = None

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
    self.peatonCorriente = 0
  
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

  def getPeatones(self, accidente):
    peatones = accidente["PEATONES"]
    if peatones==None:
      return tuple()
    peatones = peatones.get('PEATON',None)
    if peatones==None:
      return tuple()
    if not isinstance(peatones,list):
      peatones = [ peatones ]
    return peatones

  def getColumns(self):
    return COLUMNS_DEFINITION

  def getRowCount(self):
    self.rewind()
    rowCount = 0
    while True:
      row = self.next()
      if row == None:
        return rowCount
      rowCount+=1
    
  def read(self):
    peaton = self.next()
    if peaton == None:
      return None

    values = []
    peaton_id = None
    try:
      peaton_id = get1(peaton,"@ID_ACCIDENTE") +"/"+ get1(peaton,"@ID_PEATON")
    
      # LID_PEATON
      values.append(peaton_id)
      
      values.append(get1(peaton,"@ID_ACCIDENTE"))
      values.append(get1(peaton,"@ID_PEATON"))
      
      values.append(sino2bool(get1(peaton,"POSIBLE_RESPONSABLE")))
      
      values.append(get1(peaton,"FECHA_NACIMIENTO"))
      values.append(null2zero(get1(peaton,"SEXO")))
      values.append(get1(peaton,"PAIS_RESIDENCIA"))
      values.append(get1(peaton,"PROVINCIA_RESIDENCIA"))
      values.append(get1(peaton,"MUNICIPIO_RESIDENCIA"))
      values.append(null2zero(get1(peaton,"ASISTENCIA_SANITARIA")))

      values.append(sino2bool(get2(peaton,"FACTORES_ATENCION","@INFLU_FACT_ATENCION")))
      values.append(null2zero(get2(peaton,"FACTORES_ATENCION","#text")))
      values.append(sino2bool(get2(peaton,"PRESUNTOS_ERRORES","@INFLU_PRES_ERROR")))
      values.append(null2zero(get2(peaton,"PRESUNTOS_ERRORES","#text")))
      values.append(sino2bool(get2(peaton,"PRES_INFRAC_PEA","@INFLU_PRES_INFRAC")))
      values.append(null2zero(get2(peaton,"PRES_INFRAC_PEA","#text")))

      values.append(get1(peaton,"MOTIVO_DESPLAZAMIENTO"))
      values.append(null2zero(get1(peaton,"ACCION_PEA")))
      
      values.append(sino2bool(get2(peaton,"ALCOHOL","@INFLU_ALCOHOL")))
      values.append(null2zero(get2(peaton,"ALCOHOL","PRUEBA_ALCOHOLEMIA")))
      values.append(null2zero(get2(peaton,"ALCOHOL","TASA_ALCOHOLEMIA1")))
      values.append(null2zero(get2(peaton,"ALCOHOL","TASA_ALCOHOLEMIA2")))
      values.append(sino2bool(get2(peaton,"ALCOHOL","PRUEBA_ALC_SANGRE")))
      values.append(sino2bool(get2(peaton,"ALCOHOL","SIGNOS_INFLU_ALCOHOL")))

      values.append(sino2bool(get2(peaton,"DROGAS","@INFLU_DROGAS")))
      values.append(null2zero(get2(peaton,"DROGAS","PRUEBA_DROGAS")))
      values.append(sino2bool(get2(peaton,"DROGAS","AMP")))
      values.append(sino2bool(get2(peaton,"DROGAS","CONFIRMADO_AMP")))
      values.append(sino2bool(get2(peaton,"DROGAS","BDZ")))
      values.append(sino2bool(get2(peaton,"DROGAS","CONFIRMADO_BDZ")))
      values.append(sino2bool(get2(peaton,"DROGAS","COC")))
      values.append(sino2bool(get2(peaton,"DROGAS","CONFIRMADO_COC")))
      values.append(sino2bool(get2(peaton,"DROGAS","THC")))
      values.append(sino2bool(get2(peaton,"DROGAS","CONFIRMADO_THC")))
      values.append(sino2bool(get2(peaton,"DROGAS","METH")))
      values.append(sino2bool(get2(peaton,"DROGAS","CONFIRMADO_METH")))
      values.append(sino2bool(get2(peaton,"DROGAS","OPI")))
      values.append(sino2bool(get2(peaton,"DROGAS","CONFIRMADO_OPI")))
      values.append(sino2bool(get2(peaton,"DROGAS","OTRAS")))
      values.append(sino2bool(get2(peaton,"DROGAS","CONFIRMADO_OTRAS")))
      values.append(sino2bool(get2(peaton,"DROGAS","SIGNOS_INFLU_DROGAS")))

    except:
      ex = sys.exc_info()[1]
      gvsig.logger("No se puede leer el peaton %s. %s" % (peaton_id,str(ex)), gvsig.LOGGER_WARN, ex)
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
        peatones = self.getPeatones(accidente)
        if self.peatonCorriente < len(peatones) :
          peaton = peatones[self.peatonCorriente]
          #print "Peaton: ", get1(peaton,"@ID_ACCIDENTE")+"/"+get1(peaton,"@ID_PEATON"), self.peatonCorriente
          self.peatonCorriente += 1
          return peaton
        self.accidenteCorriente += 1
        self.peatonCorriente = 0

      self.informeCorriente += 1
      self.accidenteCorriente = 0
      self.peatonCorriente = 0

    self.informeCorriente = None
    return None


def main(*args):
  generate_translations(COLUMNS_DEFINITION)
  

