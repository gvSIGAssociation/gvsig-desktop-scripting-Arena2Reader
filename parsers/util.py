# encoding: utf-8

import gvsig

"""

ARENA2_CROQUIS:
- LID_CROQUIS:String:size:20
- LID_ACCIDENTE:String:size:20

- ID_ACCIDENTE:String:size:20
- DESCRIPCION:String:size:200
- DESCRIPCION:ByteArray

ARENA2_VEHICULO:
- LID_VEHICULO:String:size:20:set:hidden=true
- LID_ACCIDENTE:String:size:20:set:hidden=true

- ID_ACCIDENTE:String:size:20:set:profile=DAL.LinkedForeingKey:tag:DAL.foreingTable=ARENA2_ACCIDENTES:tag:DAL.foreingCode=ID_ACCIDENTE:tag:DAL.foreingLabel=FORMAT('%s',ID_ACCIDENTE)
- ID_VEHICULO:Integer
- SIN_CONDUCTOR:Boolean
- FECHA_MATRICULACION:Date
- NACIONALIDAD:String:size:45
- TIPO_VEHICULO:Integer
- MARCA_NOMBRE:String:size:45
- MODELO:String:size:45
- ITV:Integer
- SEGURO:Integer
- REMOLQUE:Boolean
- SEMIREMOLQUE:Boolean
- CARAVANA:Boolean
- REMOLQUE_OTROS:Boolean

- FACT_ANOMALIAS_PREVIAS:Boolean
- ANOMALIAS_NINGUNA:Boolean
- ANOMALIAS_NEUMATICOS:Boolean
- ANOMALIAS_REVENTON:Boolean
- ANOMALIAS_DIRECCION:Boolean
- ANOMALIAS_FRENOS:Boolean
- ANOMALIAS_OTRAS:Boolean

- VEHICULO_ADAPTADO:Boolean
- MERCANCIAS_PELIGROSAS:Boolean
- NUM_OCUPANTES:Integer
- FUGADO:Boolean
- INCENDIADO:Boolean
- TACOGRAFO_DISCO:Boolean

- AIRBAG_COND:Boolean
- AIRBAG_PAS_DEL:Boolean
- AIRBAG_ROD_IZDA:Boolean
- AIRBAG_ROD_DCHA:Boolean
- AIRBAG_LAT_DEL_IZDA:Boolean
- AIRBAG_LAT_DEL_DCHA:Boolean
- AIRBAG_CORT_DEL_IZDA:Boolean
- AIRBAG_CORT_DEL_DCHA:Boolean
- AIRBAG_LAT_TRAS_IZDA:Boolean
- AIRBAG_LAT_TRAS_DCHA:Boolean
- AIRBAG_CORT_TRAS_IZDA:Boolean
- AIRBAG_CORT_TRAS_DCHA:Boolean
- AIRBAG_OTROS:Boolean
- AIRBAG_DESCONOCIDO:Boolean

- TRANSPORTE_ESPECIAL:Boolean
- DANYOS:Integer
- POS_VIA:Integer
- APROXIMACION_NUDO:Integer
- SENTIDO_CIRCULACION:Integer
- POS_CALZADA:Integer
- POS_CARRIL:Integer
- LUGAR_CIRCULABA:Integer
- FACT_LUGAR_CIRCULA:Boolean

ARENA2_CONDUCTOR:
- LID_CONDUCTOR:String:size:20:set:hidden=true
- LID_VEHICULO:String:size:20:set:profile=DAL.LinkedForeingKey:tag:DAL.foreingTable=ARENA2_VEHICULOS:tag:DAL.foreingCode=LID_VEHICULO:tag:DAL.foreingLabel=FORMAT('%s',ID_VEHICULO)
- LID_ACCIDENTE:String:size:20:set:hidden=true

- ID_ACCIDENTE:String:size:20:set:profile=DAL.LinkedForeingKey:tag:DAL.foreingTable=ARENA2_ACCIDENTES:tag:DAL.foreingCode=ID_ACCIDENTE:tag:DAL.foreingLabel=FORMAT('%s',ID_ACCIDENTE)
- ID_VEHICULO:Integer:set:hidden=true

- FECHA_NACIMIENTO:Date
- SEXO:Integer
- NACIONALIDAD:String:size:45
- PAIS_RESIDENCIA:String:size:45
- PROVINCIA_RESIDENCIA:String:size:45
- MUNICIPIO_RESIDENCIA:String:size:100
- ASISTENCIA_SANITARIA:Integer
- ACC_SEG_CINTURON:Boolean
- ACC_SEG_BRAZOS:Boolean
- ACC_SEG_ESPALDA:Boolean
- ACC_SEG_TORSO:Boolean
- ACC_SEG_MANOS:Boolean
- ACC_SEG_PIERNAS:Boolean
- ACC_SEG_PIES:Boolean
- ACC_SEG_PRENDA_REF:Boolean

- CARACT_PERMISO:Integer
- CLASE_PERMISO:Integer
- FECHA_PERMISO:Date

- INFLU_ALCOHOL:Boolean
- PRUEBA_ALCOHOLEMIA:Integer
- TASA_ALCOHOLEMIA1:Double
- PRUEBA_ALC_SANGRE:Boolean
- SIGNOS_INFLU_ALCOHOL:Boolean

- INFLU_DROGAS:Boolean
- PRUEBA_DROGAS:Integer
- AMP:Boolean
- CONFIRMADO_AMP:Boolean
- BDZ:Boolean
- CONFIRMADO_BDZ:Boolean
- COC:Boolean
- CONFIRMADO_COC:Boolean
- THC:Boolean
- CONFIRMADO_THC:Boolean
- METH:Boolean
- CONFIRMADO_METH:Boolean
- OPI:Boolean
- CONFIRMADO_OPI:Boolean
- OTRAS:Boolean
- CONFIRMADO_OTRAS:Boolean
- SIGNOS_INFLU_DROGAS:Boolean

- MOTIVO_DESPLAZAMIENTO:Integer
- DESPLAZAMIENTO_PREVISTO:Integer
- INFLU_PRES_INFRAC_COND:Boolean
- PRES_INFRAC_COND:Integer
- PRES_INFRAC_SIN_LUCES:Boolean
- PRES_INFRAC_SIN_TRIANGULO:Boolean

- PRES_INFRAC_VEL_COND:Integer
- INFLU_PRES_INFRAC_VEL:Boolean
- OTRA_INFRAC_COND_TIPO:Integer
- INFLU_OTRA_INFRAC:Boolean

- POSIBLE_RESPONSABLE:Boolean
- FACTORES_ATENCION:Integer
- INFLU_FACT_ATENCION:Boolean
- PRESUNTOS_ERRORES:Integer
- INFLU_PRES_ERROR:Boolean


ARENA2_PASAJERO:
- LID_PASAGERO:String:size:20:set:hidden=true
- LID_VEHICULO:String:size:20:set:profile=DAL.LinkedForeingKey:tag:DAL.foreingTable=ARENA2_VEHICULOS:tag:DAL.foreingCode=LID_VEHICULO:tag:DAL.foreingLabel=FORMAT('%s',ID_VEHICULO)
- LID_ACCIDENTE:String:size:20:set:hidden=true

- ID_PASAJERO:Integer
- ID_VEHICULO:Integer:set:hidden=true
- ID_ACCIDENTE:String:size:20:set:profile=DAL.LinkedForeingKey:tag:DAL.foreingTable=ARENA2_ACCIDENTES:tag:DAL.foreingCode=ID_ACCIDENTE:tag:DAL.foreingLabel=FORMAT('%s',ID_ACCIDENTE)

- FECHA_NACIMIENTO:Date
- SEXO:Integer
- NACIONALIDAD:String:size:45
- PAIS_RESIDENCIA:String:size:45
- PROVINCIA_RESIDENCIA:String:size:45
- MUNICIPIO_RESIDENCIA:String:size:100
- ASISTENCIA_SANITARIA:Integer

- ACC_SEG_CINTURON:Boolean
- ACC_SEG_BRAZOS:Boolean
- ACC_SEG_ESPALDA:Boolean
- ACC_SEG_TORSO:Boolean
- ACC_SEG_MANOS:Boolean
- ACC_SEG_PIERNAS:Boolean
- ACC_SEG_PIES:Boolean
- ACC_SEG_PRENDA_REF:Boolean

- POSICION_VEHI:Integer
- NINYO_EN_BRAZO:Boolean

ARENA2_PEATON
- LID_PEATON:String:size:20:set:hidden=true
- LID_ACCIDENTE:String:size:20:set:hidden=true

- ID_PEATON:Integer
- ID_ACCIDENTE:String:size:20:set:profile=DAL.LinkedForeingKey:tag:DAL.foreingTable=ARENA2_ACCIDENTES:tag:DAL.foreingCode=ID_ACCIDENTE:tag:DAL.foreingLabel=FORMAT('%s',ID_ACCIDENTE)

- FECHA_NACIMIENTO:Date
- SEXO:Integer
- NACIONALIDAD:String:size:45
- PAIS_RESIDENCIA:String:size:45
- PROVINCIA_RESIDENCIA:String:size:45
- MUNICIPIO_RESIDENCIA:String:size:100
- ASISTENCIA_SANITARIA:Integer

- INFLU_ALCOHOL:Boolean
- PRUEBA_ALCOHOLEMIA:Integer
- TASA_ALCOHOLEMIA1:Double
- PRUEBA_ALC_SANGRE:Boolean
- SIGNOS_INFLU_ALCOHOL:Boolean

- INFLU_DROGAS:Boolean
- PRUEBA_DROGAS:Integer
- AMP:Boolean
- CONFIRMADO_AMP:Boolean
- BDZ:Boolean
- CONFIRMADO_BDZ:Boolean
- COC:Boolean
- CONFIRMADO_COC:Boolean
- THC:Boolean
- CONFIRMADO_THC:Boolean
- METH:Boolean
- CONFIRMADO_METH:Boolean
- OPI:Boolean
- CONFIRMADO_OPI:Boolean
- OTRAS:Boolean
- CONFIRMADO_OTRAS:Boolean
- SIGNOS_INFLU_DROGAS:Boolean

- MOTIVO_DESPLAZAMIENTO:Integer

- ACCION_PEA:Integer
- PRES_INFRAC_PEA:Integer
- INFLU_PRES_INFRAC:Boolean
- POSIBLE_RESPONSABLE:Boolean
- FACTORES_ATENCION:Integer
- INFLU_FACT_ATENCION:Boolean
- PRESUNTOS_ERRORES:Integer
- INFLU_PRES_ERROR:Boolean

"""

def get2(x, key1, key2):
  v = x.get(key1,None)
  if v == None:
    return None
  return v.get(key2, None)

def get1(x, key1):
  return x.get(key1,None)
  
def sino2bool(n):
  if n==None:
    return None
  if n.lower()=="no":
    return False
  return True

def null2empty(n):
  if n==None:
    return ""
  return n

def null2zero(n):
  if n==None:
    return 0
  return n

  