# encoding: utf-8

import gvsig
import sys
import os

from org.gvsig.fmap.geom.aggregate import MultiPolygon
from org.gvsig.scripting.app.extension import ScriptingUtils
import xmltodic
from org.gvsig.fmap.geom import GeometryUtils

from org.gvsig.tools.dynobject.DynField import RELATION_TYPE_COLLABORATION, RELATION_TYPE_AGGREGATE

from util import parseToBool, parseToString, parseToNumber, get1, get2, Descriptor, generate_translations, parseToNull



GROUPS_DEFINITION = [u'REGULACION_PRIORIDAD', 
          u'VICTIMAS', 
          u'TIPO_ACCIDENTE', 
          u'NUM_CARRILES', 
          u'ELEMENTOS_BALIZAMIENTO', 
          u'ELEMENTOS_SEPARACION_SENTIDO', 
          u'BARRERA_SEGURIDAD', 
          u'ELEMENTOS_TRAMO', 
          u'CARACTERISTICAS_MARGEN', 
          u'CIRCUNSTANCIAS_ESPECIALES_VIA', 
          u'DELIMITACION_CALZADA', 
          u'FACTORES_CONCURRENTES']

COLUMNS_DEFINITION = [
  Descriptor("LID_ACCIDENTE","String",20,hidden=True, pk=True,
    label="_Id_accidente",
    shortLabel="_Id_accidente")\
    .tag("dynform.readonly",True),
    
  Descriptor("COD_INFORME","String",20, pk=False,
    label="_Codigo_informe",
    shortLabel="_Cod_informe")\
    .tag("dynform.readonly",True)\
    .set("relation","Collaboration")\
    .set("indexed",True)\
    .set("allowIndexDuplicateds",True)\
    .foreingkey("ARENA2_INFORMES","COD_INFORME","FORMAT('%s',COD_INFORME)"),
    
  Descriptor("ID_ACCIDENTE","String",20, 
    label="_Codigo_accidente",
    shortLabel="_Cod_accidente")\
    .set("indexed",True)\
    .set("allowIndexDuplicateds",False)\
    .tag("dynform.readonly",True)\
    .tag("DAL.Search.Attribute.Priority",1),
    
  Descriptor("ESTADO_ACCIDENTE","Integer",
    label="_Estado_accidente",
    shortLabel="_Estado_accidente")\
    .set("relation","Collaboration")\
    .closedlistfk("ARENA2_DIC_ESTADO_ACCIDENTE")\
    .tag("report.attr.label", "DESCRIPCION"),
    
  Descriptor("OPERACION","String",30,
    label="_Operacion")\
    .tag("dynform.readonly",True),
    
  Descriptor("FECHA_ACCIDENTE","Date", 
    label= "_Fecha_accidente")\
    .tag("dynform.readonly",True)\
    .tag("DAL.Search.Attribute.Priority",6),
    
  Descriptor("HORA_ACCIDENTE","Time",  
    label="_Hora_accidente")\
    .tag("dynform.readonly",True)\
    .tag("DAL.Search.Attribute.Priority",7),
    
  Descriptor("COD_PROVINCIA","String",45,  
    label="_Provincia")\
    .set("indexed",True)\
    .set("allowIndexDuplicateds",True)\
    .tag("dynform.readonly",True)\
    .tag("DAL.Search.Attribute.Priority",2),
    
    
  Descriptor("COD_MUNICIPIO","String",100,  
    label="_Municipio")\
    .set("indexed",True)\
    .set("allowIndexDuplicateds",True)\
    .tag("dynform.readonly",True),
   
  Descriptor("COD_POBLACION","String",100,  
    label="_Poblacion")\
    .set("indexed",True)\
    .set("allowIndexDuplicateds",True)\
    .tag("dynform.readonly",True),
    
  Descriptor("ZONA","Integer",  
    label="_Zona")\
    .tag("dynform.readonly",True)\
    .set("indexed",True)\
    .set("allowIndexDuplicateds",True)\
    .set("relation","Collaboration")\
    .closedlistfk("ARENA2_DIC_ZONA")\
    .tag("report.attr.label", "DESCRIPCION"),
    
  Descriptor("TIPO_VIA","Integer",
    label="_Tipo_de_via",
    shortLabel="_Tipo_via")\
    .set("indexed",True)\
    .set("allowIndexDuplicateds",True)\
    .set("relation","Collaboration")\
    .closedlistfk("ARENA2_DIC_TIPO_VIA")\
    .tag("report.attr.label", "DESCRIPCION"),
    

  Descriptor("CARRETERA","String",
    label="_Carretera")\
    .tag("DAL.Search.Attribute.Priority",3),

  Descriptor("KM","Double", 
    label="_Punto_kilometrico",
    shortLabel="_Pk")\
    .tag("dynform.readonly",False)\
    .tag("DAL.Search.Attribute.Priority",4),

  Descriptor("TITULARIDAD_VIA","Integer",
    label="_Titularidad_de_la_via",
    shortLabel="_Titularidad_via")\
    .set("indexed",True)\
    .set("allowIndexDuplicateds",True)\
    .set("relation","Collaboration")\
    .closedlistfk("ARENA2_DIC_TITULARIDAD_VIA")\
    .tag("report.attr.label", "DESCRIPCION"),

  Descriptor("SENTIDO","Integer",  
    label="_Sentido")\
    .tag("dynform.readonly",True)\
    .set("indexed",True)\
    .set("allowIndexDuplicateds",True)\
    .set("relation","Collaboration")\
    .closedlistfk("ARENA2_DIC_SENTIDO")\
    .tag("DAL.Search.Attribute.Priority",5)\
    .tag("report.attr.label", "DESCRIPCION"),
  Descriptor("CALLE_CODIGO","String",15, 
    label="_Codigo_calle",
    shortLabel="_Cod_calle")\
    .tag("dynform.readonly",True),
  Descriptor("CALLE_NOMBRE","String",150, 
    label="_Calle")\
    .tag("dynform.readonly",True),
  Descriptor("CALLE_NUMERO","String",10, 
    label="_Numero_de_calle",
    shortLabel="_Num_calle")\
    .tag("dynform.readonly",True),
  Descriptor("MAPAY","Double")\
    .tag("dynform.readonly",True),
  Descriptor("MAPAX","Double")\
    .tag("dynform.readonly",True),
  Descriptor("MAPA", "Geometry", hidden=True, 
        geomtype="Point:2D", 
        SRS="EPSG:4326" #, 
        #expression="TRY ST_SetSRID(ST_Point(MAPAX,MAPAY),4326) EXCEPT NULL"
      )\
    .tag("dynform.readonly",True),

  Descriptor("NUDO","Integer", 
    label="_Nudo")\
    .tag("dynform.readonly",True)\
    .set("relation","Collaboration")\
    .set("indexed",True)\
    .set("allowIndexDuplicateds",True)\
    .closedlistfk("ARENA2_DIC_NUDO")\
    .tag("report.attr.label", "DESCRIPCION"),
  Descriptor("NUDO_INFO","Integer", 
    label="_Informacion_nudo",
    shortLabel="_Inf_nudo")\
    .tag("dynform.readonly",True)\
    .set("indexed",True)\
    .set("allowIndexDuplicateds",True)\
    .set("relation","Collaboration")\
    .closedlistfk("ARENA2_DIC_NUDO_INFORMACION")\
    .tag("report.attr.label", "DESCRIPCION"),
  Descriptor("CRUCE_CALLE","String",150, 
    label="_Cruce"),
  Descriptor("CRUCE_INE_CALLE","String",10, 
    label="_Cruce_INE")\
    .tag("dynform.readonly",True),
  
  Descriptor("TOTAL_VICTIMAS","Integer",
    label="_Total_victimas",
    shortlabel="_Victimas"),

  Descriptor("TOTAL_MUERTOS","Integer",
    label="_Total_muertos",
    shortlabel="_Muertos")\
    .tag("DAL.Search.Attribute.Priority",10),

  Descriptor("TOTAL_GRAVES","Integer",
    label="_Total_graves",
    shortlabel="_Graves")\
    .tag("DAL.Search.Attribute.Priority",11),  
   
  Descriptor("TOTAL_LEVES","Integer",
    label="_Total_Leves",
    shortlabel="_Leves")\
    .tag("DAL.Search.Attribute.Priority",12),
    
  Descriptor("TOTAL_ILESOS","Integer",
    label="_Total_ilesos",
    shortlabel="_Ilesos"),

  Descriptor("TOTAL_VEHICULOS","Integer", 
    label="_Total_vehiculos_implicados",
    shortlabel="_Tot_vehiculos")\
    .tag("DAL.Search.Attribute.Priority",13),

  Descriptor("TOTAL_CONDUCTORES","Integer", 
    label="_Total_conductores_implicados",
    shortlabel="_Tot_conductores"),

  Descriptor("TOTAL_PASAJEROS","Integer", 
    label="_Total_pasajeros_implicados",
    shortlabel="_Tot_pasajeros"),

  Descriptor("TOTAL_PEATONES","Integer", 
    label="_Total_peatones_implicados",
    shortlabel="_Tot_peatones"),
    
  Descriptor("NUM_TURISMOS","Integer", 
    label="_Num_turismos_implicados",
    shortlabel="_Num_turismos"),

  Descriptor("NUM_FURGONETAS","Integer", 
    label="_Num_furgonetas_implicadas",
    shortlabel="_Num_furgonetas"),

  Descriptor("NUM_CAMIONES","Integer", 
    label="_Num_camiones_implicados",
    shortlabel="_Num_camiones"),

  Descriptor("NUM_AUTOBUSES","Integer", 
    label="_Num_autobuses_implicados",
    shortlabel="_Num_autobuses"),

  Descriptor("NUM_CICLOMOTORES","Integer", 
    label="_Num_ciclomotores_implicados",
    shortlabel="_Num_ciclomotores"),

  Descriptor("NUM_MOTOCICLETAS","Integer", 
    label="_Num_motocicletas_implicadas",
    shortlabel="_Num_motocicletas"),

  Descriptor("NUM_BICICLETAS","Integer", 
    label="_Num_bicicletas_implicadas",
    shortlabel="_Num_bicicletas"),

  Descriptor("NUM_OTROS_VEHI","Integer", 
    label="_Num_otros_vehiculos_implicados",
    shortlabel="_Num_otros_vehiculos"),


  Descriptor("TIPO_ACC_SALIDA","Integer", 
    label="_Tipo_accidente_Salida",
    shortlabel="_Tipo_acc_Sal")\
    .tag("dynform.readonly",True)\
    .set("indexed",True)\
    .set("allowIndexDuplicateds",True)\
    .set("relation","Collaboration")\
    .closedlistfk("ARENA2_DIC_TIPO_ACCIDENTE_SALIDA")\
    .tag("report.attr.label", "DESCRIPCION"),
  Descriptor("TIPO_ACC_COLISION","Integer", 
    label="_Tipo_accidente_Colision",
    shortlabel="_Tipo_acc_Col")\
    .tag("dynform.readonly",True)\
    .set("indexed",True)\
    .set("allowIndexDuplicateds",True)\
    .set("relation","Collaboration")\
    .closedlistfk("ARENA2_DIC_TIPO_ACCIDENTE_COLISION")\
    .tag("report.attr.label", "DESCRIPCION"),
  Descriptor("TIPO_ACC_ANIMAL","Integer", 
    label="_Especie_del_animal",
    shortlabel="_Especie_animal")\
    .tag("dynform.readonly",True)\
    .set("indexed",True)\
    .set("allowIndexDuplicateds",True)\
    .set("relation","Collaboration")\
    .closedlistfk("ARENA2_DIC_TIPO_ACCIDENTE_ANIMAL")\
    .tag("report.attr.label", "DESCRIPCION"),
  
  
  Descriptor("SENTIDO_CONTRARIO","Boolean", 
    label="_Circular_sentido_contrario")\
    .tag("dynform.readonly",True),
    
  Descriptor("CONDICION_NIVEL_CIRCULA","Integer", 
    label="_Nivel_circulacion")\
    .tag("dynform.readonly",True)\
    .set("relation","Collaboration")\
    .set("indexed",True)\
    .set("allowIndexDuplicateds",True)\
    .closedlistfk("ARENA2_DIC_NIVEL_CIRCULACION")\
    .tag("report.attr.label", "DESCRIPCION"),
  Descriptor("INFLU_NIVEL_CIRC","Boolean",  
    label="_Influye_nivel_circulacion")\
    .tag("dynform.readonly",True),
  Descriptor("CONDICION_FIRME","Integer",  
    label="_Condicion_del_firme")\
    .tag("dynform.readonly",True)\
    .set("indexed",True)\
    .set("allowIndexDuplicateds",True)\
    .set("relation","Collaboration")\
    .closedlistfk("ARENA2_DIC_CONDICION_FIRME")\
    .tag("report.attr.label", "DESCRIPCION"),
  Descriptor("INFLU_SUP_FIRME","Boolean",  
    label="_Influye_firme")\
    .tag("dynform.readonly",True),
  Descriptor("CONDICION_ILUMINACION","Integer",  
    label="_Iluminacion")\
    .tag("dynform.readonly",True)\
    .set("indexed",True)\
    .set("allowIndexDuplicateds",True)\
    .set("relation","Collaboration")\
    .closedlistfk("ARENA2_DIC_ILUMINACION")\
    .tag("report.attr.label", "DESCRIPCION"),
  Descriptor("INFLU_ILUMINACION","Boolean",  
    label="_Influye_iluminacion")\
    .tag("dynform.readonly",True),
  Descriptor("CONDICION_METEO","Integer",  
    label="_Meteorologia")\
    .tag("dynform.readonly",True)\
    .set("relation","Collaboration")\
    .set("indexed",True)\
    .set("allowIndexDuplicateds",True)\
    .closedlistfk("ARENA2_DIC_METEO")\
    .tag("report.attr.label", "DESCRIPCION"),
  Descriptor("INFLU_METEO","Boolean",  
    label="_Influye_meteorologia")\
    .tag("dynform.readonly",True),

  Descriptor("CONDICION_NIEBLA","Integer",  
    label="_Niebla")\
    .tag("dynform.readonly",True)\
    .set("relation","Collaboration")\
    .set("indexed",True)\
    .set("allowIndexDuplicateds",True)\
    .closedlistfk("ARENA2_DIC_NIEBLA")\
    .tag("report.attr.label", "DESCRIPCION"),
  Descriptor("CONDICION_VIENTO","Integer",  
    label="_Viento_fuerte")\
    .tag("dynform.readonly",True)\
    .set("relation","Collaboration")\
    .set("indexed",True)\
    .set("allowIndexDuplicateds",True)\
    .closedlistfk("ARENA2_DIC_VIENTO")\
    .tag("report.attr.label", "DESCRIPCION"),

  
  Descriptor("VISIB_RESTRINGIDA_POR","Integer",  
    label="_Visibilidad")\
    .tag("dynform.readonly",True)\
    .set("indexed",True)\
    .set("allowIndexDuplicateds",True)\
    .set("relation","Collaboration")\
    .closedlistfk("ARENA2_DIC_VISIBILIDAD_RESTRINGIDA_POR")\
    .tag("report.attr.label", "DESCRIPCION"),
  Descriptor("INFLU_VISIBILIDAD","Boolean",  
    label="_Influye visibilidad")\
    .tag("dynform.readonly",True),
    
  Descriptor("CARACT_FUNCIONAL_VIA","Integer", 
    label="_Caracteristicas_funcionales_de_la_via",
    shortLabel="_Caracteisticas_via")\
    .tag("dynform.readonly",True)\
    .set("relation","Collaboration")\
    .set("indexed",True)\
    .set("allowIndexDuplicateds",True)\
    .closedlistfk("ARENA2_DIC_CARACT_FUNCIONAL_VIA")\
    .tag("report.attr.label", "DESCRIPCION"),
  Descriptor("VEL_GENERICA_SENYALIZADA","Integer", 
    label="_Velocidad_generica")\
    .tag("dynform.readonly",True)\
    .set("relation","Collaboration")\
    .set("indexed",True)\
    .set("allowIndexDuplicateds",True)\
    .closedlistfk("ARENA2_DIC_VEL_GENERICA")\
    .tag("report.attr.label", "DESCRIPCION"),

  Descriptor("VELOCIDAD","Double", 
    label="_Velocidad")\
    .tag("dynform.readonly",True),
  Descriptor("SENTIDOS_VIA","Integer", 
    label="_Sentidos_via",
    shortlabel="_Sentidos")\
    .set("indexed",True)\
    .set("allowIndexDuplicateds",True)\
    .set("relation","Collaboration")\
    .closedlistfk("ARENA2_DIC_SENTIDOS_VIA")\
    .tag("dynform.readonly",True)\
    .tag("report.attr.label", "DESCRIPCION"),
  Descriptor("NUMERO_CALZADAS","Integer", 
    label="_Numero_de_calzadas",
    shortlabel="_Num_calzadas")\
    .tag("dynform.readonly",True)\
    .set("indexed",True)\
    .set("allowIndexDuplicateds",True)\
    .set("relation","Collaboration")\
    .closedlistfk("ARENA2_DIC_NUMERO_CALZADAS")\
    .tag("report.attr.label", "DESCRIPCION"),
  Descriptor("CARRILES_APTOS_CIRC_ASC","Integer", 
    label="_Carriles_aptos_circular_ascendente",
    shortlabel="_Carr_aptos_cir_asc")\
    .set("indexed",True)\
    .set("allowIndexDuplicateds",True)\
    .tag("dynform.readonly",True),
  Descriptor("CARRILES_APTOS_CIRC_DESC","Integer", 
    label="_Carriles_aptos_circular_descenente",
    shortlabel="_Carr_aptos_cir_desc")\
    .tag("dynform.readonly",True),
    
  Descriptor("ANCHURA_CARRIL","Integer", 
    label="_Anchura_de_carril",
    shortlabel="_Anchura_carril")\
    .tag("dynform.readonly",True)\
    .set("relation","Collaboration")\
    .set("indexed",True)\
    .set("allowIndexDuplicateds",True)\
    .closedlistfk("ARENA2_DIC_ANCHURA_CARRIL")\
    .tag("report.attr.label", "DESCRIPCION"),
  Descriptor("ARCEN","Integer", 
    label="_Arcen")\
    .tag("dynform.readonly",True)\
    .set("relation","Collaboration")\
    .set("indexed",True)\
    .set("allowIndexDuplicateds",True)\
    .closedlistfk("ARENA2_DIC_ANCHURA_ARCEN")\
    .tag("report.attr.label", "DESCRIPCION"),
  Descriptor("ACERA","Integer", 
    label="_Acera")\
    .tag("dynform.readonly",True)\
    .set("relation","Collaboration")\
    .set("indexed",True)\
    .set("allowIndexDuplicateds",True)\
    .closedlistfk("ARENA2_DIC_ACERA")\
    .tag("report.attr.label", "DESCRIPCION"),
  Descriptor("INFLU_ACERA","Boolean", 
    label="_Influye_la_acera",
    shortLabel="_Influye_acera")\
    .tag("dynform.readonly",True),
  Descriptor("ANCHURA_ACERA","Integer", 
    label="_Anchua_acera")\
    .tag("dynform.readonly",True),
    
  Descriptor("TRAZADO_PLANTA","Integer", 
    label="_Trazado_planta")\
    .tag("dynform.readonly",True)
    .set("relation","Collaboration")\
    .set("indexed",True)\
    .set("allowIndexDuplicateds",True)\
    .closedlistfk("ARENA2_DIC_TRAZADO_PLANTA")\
    .tag("report.attr.label", "DESCRIPCION"),
  Descriptor("TRAZADO_ALZADO","Integer", 
    label="_Trazado_alzado")\
    .tag("dynform.readonly",True)\
    .set("relation","Collaboration")\
    .set("indexed",True)\
    .set("allowIndexDuplicateds",True)\
    .closedlistfk("ARENA2_DIC_TRAZADO_ALZADO")\
    .tag("report.attr.label", "DESCRIPCION"),
  Descriptor("MARCAS_VIALES","Integer", 
    label="_Marcas_viales")\
    .tag("dynform.readonly",True)\
    .set("relation","Collaboration")\
    .set("indexed",True)\
    .set("allowIndexDuplicateds",True)\
    .closedlistfk("ARENA2_DIC_MARCAS_VIALES")\
    .tag("report.attr.label", "DESCRIPCION"),

  Descriptor("DESCRIPCION","String",5120,profile="Text")\
    .tag("dynform.readonly",True),
  Descriptor("OBSERVACIONES","String",5120,profile="Text")\
    .tag("dynform.readonly",True),


  # Regulacion de prioridad
  Descriptor("INFLU_PRIORIDAD","Boolean", 
    group="_Regulacion_prioridad",
    label="_Influye_la_regulacion_de_prioridad ",
    shortlabel="_Influye_RP")\
    .tag("dynform.readonly",True),
  Descriptor("PRIORI_NORMA","Boolean", 
    group="_Regulacion_prioridad",
    label="_RP_Norma_generica",
    shortlabel="_RP_Generica")\
    .tag("dynform.readonly",True),
  Descriptor("PRIORI_AGENTE","Boolean", 
    group="_Regulacion_prioridad",
    label="_RP_Agente",
    shortlabel="_RP_Agente")\
    .tag("dynform.readonly",True),
  Descriptor("PRIORI_SEMAFORO","Boolean", 
    group="_Regulacion_prioridad",
    label="_RP_Semaforo",
    shortlabel="_RP_Semaforo")\
    .tag("dynform.readonly",True),
  Descriptor("PRIORI_VERT_STOP","Boolean", 
    group="_Regulacion_prioridad",
    label="_RP_Senal_de_stop_vertical",
    shortlabel="_RP_Stop_vertical")\
    .tag("dynform.readonly",True),
  Descriptor("PRIORI_VERT_CEDA","Boolean", 
    group="_Regulacion_prioridad",
    label="_RP_Senal_ceda_el_paso_vertical",
    shortlabel="_RP_ceda_el_paso_vertical")\
    .tag("dynform.readonly",True),
  Descriptor("PRIORI_HORIZ_STOP","Boolean", 
    group="_Regulacion_prioridad",
    label="_RP_Senal_de_stop_horizontal",
    shortlabel="_RP_stop_horizontal")\
    .tag("dynform.readonly",True),
  Descriptor("PRIORI_HORIZ_CEDA","Boolean", 
    group="_Regulacion_prioridad",
    label="_RP_Senal_ceda_el_paso_horizontal",
    shortlabel="_RP_ceda_el_paso_horizontal")\
    .tag("dynform.readonly",True),
  Descriptor("PRIORI_MARCAS","Boolean", 
    group="_Regulacion_prioridad",
    label="_RP_Solo_marcas_viales",
    shortlabel="_RP_Marcas")\
    .tag("dynform.readonly",True),
  Descriptor("PRIORI_PEA_NO_ELEV","Boolean", 
    group="_Regulacion_prioridad",
    label="_RP_Paso_peatones_no_elevado",
    shortlabel="_RP_Paso_pea_no_elev")\
    .tag("dynform.readonly",True),
  Descriptor("PRIORI_PEA_ELEV","Boolean", 
    group="_Regulacion_prioridad",
    label="_RP_Paso_peatones_elevado",
    shortlabel="_RP_Paso_pea_elev")\
    .tag("dynform.readonly",True),
  Descriptor("PRIORI_MARCA_CICLOS","Boolean", 
    group="_Regulacion_prioridad",
    label="_RP_Paso_ciclistas",
    shortlabel="_RP_Paso_ciclistas")\
    .tag("dynform.readonly",True),
  Descriptor("PRIORI_CIRCUNSTANCIAL","Boolean", 
    group="_Regulacion_prioridad",
    label="_RP_Senalizacion_circunstancial",
    shortlabel="_RP_Circunstancial")\
    .tag("dynform.readonly",True),
  Descriptor("PRIORI_OTRA","Boolean", 
    group="_Regulacion_prioridad",
    label="_RP_Otra_senal",
    shortlabel="_RP_Otra")\
    .tag("dynform.readonly",True),

  # Elementos de Balizamiento
  Descriptor("EB_PANELES_DIRECCIONALES","Boolean",
    label="_EB_Panels_direccionales",
    shortlabel="_EB_Paneles")\
    .tag("dynform.readonly",True),
  Descriptor("EB_HITOS_ARISTA","Boolean",
    label="_EB_Hitos_arista",
    shortlabel="_EB_Hitos_arista")\
    .tag("dynform.readonly",True),
  Descriptor("EB_CAPTAFAROS","Boolean",
    label="_EB_Captafaros",
    shortlabel="_EB_Captafaros")\
    .tag("dynform.readonly",True),

  # Elementos de Separacion
  Descriptor("SEPARA_LINEA_LONG_SEPARACION","Boolean",
    label="_ES_Solo_linea_longitudinal",
    shortlabel="_ES_Linea_long")\
    .tag("dynform.readonly",True),
  Descriptor("SEPARA_CEBREADO","Boolean",
    label="_ES_Cebreado")\
    .tag("dynform.readonly",True),
  Descriptor("SEPARA_MEDIANA","Boolean",
    label="_ES_Mediana")\
    .tag("dynform.readonly",True),
  Descriptor("SEPARA_BARRERA_SEGURIDAD","Boolean",
    label="_ES_Barrera_de_seguridad",
    shortlabel="_ES_Barrera_seguridad")\
    .tag("dynform.readonly",True),
  Descriptor("SEPARA_ZONA_PEATONAL","Boolean",
    label="_ES_Zona_peatonal",
    shortlabel="_ES_Zona_peatonal")\
    .tag("dynform.readonly",True),
  Descriptor("SEPARA_OTRA_SEPARACION","Boolean",
    label="_ES_Otras")\
    .tag("dynform.readonly",True),
  Descriptor("SEPARA_NINGUNA_SEPARACION","Boolean",
    label="_ES_Ninguno")\
    .tag("dynform.readonly",True),

  # Barrera de seguridad
  Descriptor("BARRERA_SEG_LAT_ASC","Integer",
    label="_BS_Lateral_ascendente",
    shortlabel="_BS_Lateral_asc",
    group="_Barrera_seguridad")\
    .tag("dynform.readonly",True)\
    .set("indexed",True)\
    .set("allowIndexDuplicateds",True)\
    .set("relation","Collaboration")\
    .closedlistfk("ARENA2_DIC_TIPO_BARRERA"),
  Descriptor("BARRERA_SEG_LAT_ASC_MOTO","Boolean",
    label="_BS_Lateral_asc_proteccion_mototista",
    shortlabel="_BS_Lateral_asc_prot_moto",
    group="_Barrera_seguridad")\
    .tag("dynform.readonly",True),
  Descriptor("BARRERA_SEG_LAT_DESC","Integer",
    label="_BS_Lateral_descendente",
    shortlabel="_BS_Lateral_desc",
    group="_Barrera_seguridad")\
    .tag("dynform.readonly",True)\
    .set("indexed",True)\
    .set("allowIndexDuplicateds",True)\
    .set("relation","Collaboration")\
    .closedlistfk("ARENA2_DIC_TIPO_BARRERA"),
  Descriptor("BARRERA_SEG_LAT_DESC_MOTO","Boolean",
    label="_BS_Lateral_desc_proteccion_mototista",
    shortlabel="_BS_Lateral_desc_prot_moto",
    group="_Barrera_seguridad")\
    .tag("dynform.readonly",True),
  Descriptor("BARRERA_SEG_MEDIANA_ASC","Integer",
    label="_BS_en_mediana_ascendente",
    shortlabel="_BS_en_mediana_asc",
    group="_Barrera_seguridad")\
    .tag("dynform.readonly",True)\
    .set("indexed",True)\
    .set("allowIndexDuplicateds",True)\
    .set("relation","Collaboration")\
    .closedlistfk("ARENA2_DIC_TIPO_BARRERA"),
  Descriptor("BARRERA_SEG_MEDIANA_ASC_MOTO","Boolean",
    label="_BS_en_mediana_asc_proteccion_motorista",
    shortlabel="_BS_en_mediana_asc_prot_moto",
    group="_Barrera_seguridad")\
    .tag("dynform.readonly",True),
  Descriptor("BARRERA_SEG_MEDIANA_DESC","Integer",
    label="_BS_en_mediana_descendente",
    shortlabel="_BS_en_mediana_desc",
    group="_Barrera_seguridad")\
    .tag("dynform.readonly",True)\
    .set("indexed",True)\
    .set("allowIndexDuplicateds",True)\
    .set("relation","Collaboration")\
    .closedlistfk("ARENA2_DIC_TIPO_BARRERA"),
  Descriptor("BARRERA_SEG_MEDIANA_DESC_MOTO","Boolean",
    label="_BS_en_mediana_desc_proteccion_motorista",
    shortlabel="_BS_en_mediana_desc_prot_moto",
    group="_Barrera_seguridad")\
    .tag("dynform.readonly",True),

  # Elementos del tramo
  Descriptor("TRAMO_PUENTE","Boolean",
    label="_ET_puente_o_paso_superior",
    shortlabel="_ET_puente",
    group="_Elementos_tramo")\
    .tag("dynform.readonly",True),
  Descriptor("TRAMO_TUNEL","Boolean",
    label="_ET_tunel",
    shortlabel="_ET_tunel",
    group="_Elementos_tramo")\
    .tag("dynform.readonly",True),
  Descriptor("TRAMO_PASO","Boolean",
    label="_ET_paso_inferior",
    shortlabel="_ET_paso_inferior",
    group="_Elementos_tramo")\
    .tag("dynform.readonly",True),
  Descriptor("TRAMO_ESTRECHA","Boolean",
    label="_ET_Estrechamiento",
    shortlabel="_ET_Estrechamiento",
    group="_Elementos_tramo")\
    .tag("dynform.readonly",True),
  Descriptor("TRAMO_RESALTOS","Boolean",
    label="_ET_resaltos_reductores_velocidad",
    shortlabel="_ET_resaltos",
    group="_Elementos_tramo")\
    .tag("dynform.readonly",True),
  Descriptor("TRAMO_BADEN","Boolean",
    label="_ET_Baden",
    shortlabel="_ET_baden",
    group="_Elementos_tramo")\
    .tag("dynform.readonly",True),
  Descriptor("TRAMO_APARTADERO","Boolean",
    label="_ET_apartadero",
    shortlabel="_ET_apartedero",
    group="_Elementos_tramo")\
    .tag("dynform.readonly",True),
  Descriptor("TRAMO_NINGUNA","Boolean",
    label="_ET_ninguno",
    shortlabel="_ET_ninguno",
    group="_Elementos_tramo")\
    .tag("dynform.readonly",True),

  # Caracteristicas del margen
  Descriptor("INFLU_MARGEN","Boolean",
    label="_Influye_caracteristicas_margen",
    shortlabel="_Influye_margen",
    group="_Caracteristicas_margen")\
    .tag("dynform.readonly",True),
  Descriptor("MARGEN_DESPEJADO","Boolean",
    label="_CM_Despejado",
    shortlabel="_CM_Despejado",
    group="_Caracteristicas_margen")\
    .tag("dynform.readonly",True),
  Descriptor("MARGEN_ARBOLES","Boolean",
    label="_CM_Arboles",
    shortlabel="_CM_Arboles",
    group="_Caracteristicas_margen")\
    .tag("dynform.readonly",True),
  Descriptor("MARGEN_OTROS_NATURALES","Boolean",
    label="_CM_Otros_elementos_naturales",
    shortlabel="_CM_Otros_elem_naturales",
    group="_Caracteristicas_margen")\
    .tag("dynform.readonly",True),
  Descriptor("MARGEN_EDIFICIOS","Boolean",
    label="_CM_Edificions",
    shortlabel="_CM_Edificios",
    group="_Caracteristicas_margen")\
    .tag("dynform.readonly",True),
  Descriptor("MARGEN_POSTES","Boolean",
    label="_CM_Postes",
    shortlabel="_CM_Postes",
    group="_Caracteristicas_margen")\
    .tag("dynform.readonly",True),
  Descriptor("MARGEN_PUBLICIDAD","Boolean",
    label="_CM_Carteles_publicidad",
    shortlabel="_CM_Carteles",
    group="_Caracteristicas_margen")\
    .tag("dynform.readonly",True),
  Descriptor("MARGEN_OTROS_ARTIFICIALES","Boolean",
    label="_CM_Otros_elementos_artificiales",
    shortlabel="_CM_Otros_elem_artificiales",
    group="_Caracteristicas_margen")\
    .tag("dynform.readonly",True),
  Descriptor("MARGEN_OTROS_OBSTACULOS","Boolean",
    label="_CM_Otros_obstaculos",
    shortlabel="_CM_Otros_obstaculos",
    group="_Caracteristicas_margen")\
    .tag("dynform.readonly",True),
  Descriptor("MARGEN_DESC","Boolean",
    label="_CM_Se_desconoce",
    shortlabel="_CM_Se_desconoce",
    group="_Caracteristicas_margen")\
    .tag("dynform.readonly",True),

  # Circunstancias especiales
  Descriptor("INFLU_CIRCUNS_ESP","Boolean",
    label="_Influye_circustancias_especiales_via",
    shortlabel="_Influye_circus_esp_via",
    group="_Circunstancias_especiales_via")\
    .tag("dynform.readonly",True),
  Descriptor("CIRCUNS_ESP_NINGUNA","Boolean",
    label="_CE_Ninguna",
    shortlabel="_CE_Ninguna",
    group="_Circunstancias_especiales_via")\
    .tag("dynform.readonly",True),
  Descriptor("CIRCUNS_ESP_CONOS","Boolean",
    label="_CE_Conos_u_otras_balizas_moviles",
    shortlabel="_CE_Balizas_moviles",
    group="_Circunstancias_especiales_via")\
    .tag("dynform.readonly",True),
  Descriptor("CIRCUNS_ESP_ZANJA","Boolean",
    label="_CE_Zanja_o_surco",
    shortlabel="_CE_Zanja",
    group="_Circunstancias_especiales_via")\
    .tag("dynform.readonly",True),
  Descriptor("CIRCUNS_ESP_TAPA","Boolean",
    label="_CE_Tapa_registro_defectuosa",
    shortlabel="_CE_Tapa_defectuosa",
    group="_Circunstancias_especiales_via")\
    .tag("dynform.readonly",True),
  Descriptor("CIRCUNS_ESP_OBRAS","Boolean",
    label="_CE_Obras",
    shortlabel="_CE_Obras",
    group="_Circunstancias_especiales_via")\
    .tag("dynform.readonly",True),
  Descriptor("CIRCUNS_ESP_OBSTACULO","Boolean",
    label="_CE_Obstaculo_en_calzada",
    shortlabel="_CE_Obstaculo",
    group="_Circunstancias_especiales_via")\
    .tag("dynform.readonly",True),
  Descriptor("CIRCUNS_ESP_DESPREND","Boolean",
    label="_CE_Desprendimientos",
    shortlabel="_CE_Desprendimientos",
    group="_Circunstancias_especiales_via")\
    .tag("dynform.readonly",True),
  Descriptor("CIRCUNS_ESP_ESCALON","Boolean",
    label="_CE_Escalon",
    shortlabel="_CE_Escalon",
    group="_Circunstancias_especiales_via")\
    .tag("dynform.readonly",True),
  Descriptor("CIRCUNS_ESP_FBACHES","Boolean",
    label="_CE_Firme_con_baches",
    shortlabel="_CE_Baches",
    group="_Circunstancias_especiales_via")\
    .tag("dynform.readonly",True),
  Descriptor("CIRCUNS_ESP_FDETERIORADO","Boolean",
    label="_CE_Firme_deteriorado",
    shortlabel="_CE_Deteriorado",
    group="_Circunstancias_especiales_via")\
    .tag("dynform.readonly",True),
  Descriptor("CIRCUNS_ESP_OTRAS","Boolean",
    label="_CE_Otras",
    shortlabel="_CE_Otras",
    group="_Circunstancias_especiales_via")\
    .tag("dynform.readonly",True),
  Descriptor("CIRCUNS_ESP_DESC","Boolean",
    label="_CE_Se_desconoce",
    shortlabel="_CE_Se_desconoce",
    group="_Circunstancias_especiales_via")\
    .tag("dynform.readonly",True),

  # Delimitacion de la calzada
  Descriptor("INFLU_DELIM_CALZADA","Boolean",
    label="_Influye_delimitacion_calzada",
    shortlabel="_Influye_del_calzada",
    group="_Delimitacion_calzada")\
    .tag("dynform.readonly",True),
  Descriptor("DELIM_CALZADA_BORDILLO","Boolean",
    label="_DC_Bordillo",
    shortlabel="_DC_Bordillo",
    group="_Delimitacion_calzada")\
    .tag("dynform.readonly",True),
  Descriptor("DELIM_CALZADA_VALLAS","Boolean",
    label="_DC_Bolardos_o_vayas_seguridad",
    shortlabel="_DC_Bolardos",
    group="_Delimitacion_calzada")\
    .tag("dynform.readonly",True),
  Descriptor("DELIM_CALZADA_SETOS","Boolean",
    label="_DC_Setos",
    shortlabel="_DC_Setos",
    group="_Delimitacion_calzada")\
    .tag("dynform.readonly",True),
  Descriptor("DELIM_CALZADA_MARCAS","Boolean",
    label="_DC_Marcas_viales",
    shortlabel="_DC_Marcas",
    group="_Delimitacion_calzada")\
    .tag("dynform.readonly",True),
  Descriptor("DELIM_CALZADA_BARRERA","Boolean",
    label="_DC_Barrera_de_seguridad",
    shortlabel="_DC_Barrera",
    group="_Delimitacion_calzada")\
    .tag("dynform.readonly",True),
  Descriptor("DELIM_CALZADA_ISLETA","Boolean",
    label="_DC_Isleta_o_refugio",
    shortlabel="_DC_Isleta",
    group="_Delimitacion_calzada")\
    .tag("dynform.readonly",True),
  Descriptor("DELIM_CALZADA_PEATONAL","Boolean",
    label="_DC_Zona_peatonal_o_ajardinada",
    shortlabel="_DC_Zona_peatonal",
    group="_Delimitacion_calzada")\
    .tag("dynform.readonly",True),
  Descriptor("DELIM_CALZADA_OTRA","Boolean",
    label="_DC_Otras",
    shortlabel="_DC_Otras",
    group="_Delimitacion_calzada")\
    .tag("dynform.readonly",True),
  Descriptor("DELIM_CALZADA_SIN_DELIM","Boolean",
    label="_DC_Sin_delimitar",
    shortlabel="_DC_Sin_delimitar",
    group="_Delimitacion_calzada")\
    .tag("dynform.readonly",True),

  # factores concurrentes
  Descriptor("FC_CON_DISTRAIDA","Boolean",
    label="_FC_Conduccion_distraida",
    shortlabel="_FC_Cond_distraida",
    group="_Factores_concurrentes")\
    .tag("dynform.readonly",True),
  Descriptor("FC_VEL_INADECUADA","Boolean",
    label="_FC_Velocidad_inadecuada",
    shortlabel="_FC_Vel_inadecuada",
    group="_Factores_concurrentes")\
    .tag("dynform.readonly",True),
  Descriptor("FC_PRIORIDAD","Boolean",
    label="_FC_No_respetar_prioridad",
    shortlabel="_FC_Prioridad",
    group="_Factores_concurrentes")\
    .tag("dynform.readonly",True),
  Descriptor("FC_SEGURIDAD","Boolean",
    label="_FC_No_mantener_intervalo_seguridad",
    shortlabel="_FC_Seguridad",
    group="_Factores_concurrentes")\
    .tag("dynform.readonly",True),
  Descriptor("FC_ADELANTAMIENTO","Boolean",
    label="_FC_Adelantamiento_antireglamentario",
    shortlabel="_FC_Adelantamiento",
    group="_Factores_concurrentes")\
    .tag("dynform.readonly",True),
  Descriptor("FC_GIRO","Boolean",
    label="_FC_Giro_incorrecto",
    shortlabel="_FC_Giro",
    group="_Factores_concurrentes")\
    .tag("dynform.readonly",True),
  Descriptor("FC_CON_NEGLIGENTE","Boolean",
    label="_FC_Conduccion_negligente",
    shortlabel="_FC_Cond_negligente",
    group="_Factores_concurrentes")\
    .tag("dynform.readonly",True),
  Descriptor("FC_CON_TEMERARIA","Boolean",
    label="_FC_Conduccion_temeraria",
    shortlabel="_FC_Cond_temeraria",
    group="_Factores_concurrentes")\
    .tag("dynform.readonly",True),
  Descriptor("FC_IRRUPCION_ANIMAL","Boolean",
    label="_FC_Irrupcion_animal_en_calzada",
    shortlabel="_FC_Irrupcion_animal",
    group="_Factores_concurrentes")\
    .tag("dynform.readonly",True),
  Descriptor("FC_IRRUPCION_PEATON","Boolean",
    label="_FC_Irrupcion_peaton_en_calzada",
    shortlabel="_FC_Irrupcion_peaton",
    group="_Factores_concurrentes")\
    .tag("dynform.readonly",True),
  Descriptor("FC_ALCOHOL","Boolean",
    label="_FC_Alcohol",
    shortlabel="_FC_Alcohol",
    group="_Factores_concurrentes")\
    .tag("dynform.readonly",True),
  Descriptor("FC_DROGAS","Boolean",
    label="_FC_Drogas",
    shortlabel="_FC_Drogas",
    group="_Factores_concurrentes")\
    .tag("dynform.readonly",True),
  Descriptor("FC_ESTADO_VIA","Boolean",
    label="_FC_Estado_de_la_via",
    shortlabel="_FC_Estado_via",
    group="_Factores_concurrentes")\
    .tag("dynform.readonly",True),
  Descriptor("FC_METEORO","Boolean",
    label="_FC_Meteorologia_adversa",
    shortlabel="_FC_Meteorologia",
    group="_Factores_concurrentes")\
    .tag("dynform.readonly",True),
  Descriptor("FC_CANSANCIO","Boolean",
    label="_FC_Cansancio_o_sueno",
    shortlabel="_FC_Cansancio",
    group="_Factores_concurrentes")\
    .tag("dynform.readonly",True),
  Descriptor("FC_INEXPERIENCIA","Boolean",
    label="_FC_Inexperiencia",
    shortlabel="_FC_Inexperiencia",
    group="_Factores_concurrentes")\
    .tag("dynform.readonly",True),
  Descriptor("FC_AVERIA","Boolean",
    label="_FC_Averia_mecanica",
    shortlabel="_FC_Averia",
    group="_Factores_concurrentes")\
    .tag("dynform.readonly",True),
  Descriptor("FC_OBRAS","Boolean",
    label="_FC_Tramo_en_obras",
    shortlabel="_FC_Obras",
    group="_Factores_concurrentes")\
    .tag("dynform.readonly",True),
  Descriptor("FC_MAL_ESTADO_VEHI","Boolean",
    label="_FC_Mal_estado_del_vehiculo",
    shortlabel="_FC_Estado_vehiculo",
    group="_Factores_concurrentes")\
    .tag("dynform.readonly",True),
  Descriptor("FC_ENFERMEDAD","Boolean",
    label="_FC_Enfermedad",
    shortlabel="_FC_Enfermedad",
    group="_Factores_concurrentes")\
    .tag("dynform.readonly",True),
  Descriptor("FC_SENYALIZACION","Boolean",
    label="_FC_Estado_de_la_senalizacion",
    shortlabel="_FC_Senalizacion",
    group="_Factores_concurrentes")\
    .tag("dynform.readonly",True),
  Descriptor("FC_OBSTACULO","Boolean",
    label="_FC_Obstaculo_en_calzada",
    shortlabel="_FC_Obstaculo",
    group="_Factores_concurrentes")\
    .tag("dynform.readonly",True),
  Descriptor("FC_OTRO_FACTOR","Boolean",
    label="_FC_Otro_factor",
    shortlabel="_FC_Otro",
    group="_Factores_concurrentes")\
    .tag("dynform.readonly",True),
    
Descriptor("QUINCENA","String",8,
    group="_Importacion",
    label="_Quincena")\
    .tag("dynform.readonly",True), 
    
    
  Descriptor("VEHICULOS","List",
    label="_Vehiculos",
    group="_Vehiculos")\
    .set("relation","Aggregation")\
    .relatedFeatures(
      "ARENA2_VEHICULOS",
      "LID_VEHICULO",
      ("ID_VEHICULO","NACIONALIDAD","TIPO_VEHICULO","MARCA_NOMBRE","MODELO"),
      "SELECT * FROM ARENA2_VEHICULOS WHERE ARENA2_ACCIDENTES.ID_ACCIDENTE = ARENA2_VEHICULOS.ID_ACCIDENTE;"
    )\
    .tag("dynform.readonly",True)\
    .tag("dynform.label.empty",True),
  Descriptor("PEATONES","List",
    label="_Peatones",
    group="_Peatones")\
    .set("relation","Aggregation")\
    .relatedFeatures(
      "ARENA2_PEATONES",
      "LID_PEATON",
      ("ID_PEATON","FECHA_NACIMIENTO","SEXO","PAIS_RESIDENCIA","PROVINCIA_RESIDENCIA","MUNICIPIO_RESIDENCIA"),
      "SELECT * FROM ARENA2_PEATONES WHERE ARENA2_ACCIDENTES.ID_ACCIDENTE = ARENA2_PEATONES.ID_ACCIDENTE;"
    )\
    .tag("dynform.readonly",True)\
    .tag("dynform.label.empty",True),

  Descriptor("CROQUIS","List",
    label="_Croquis",
    group="_Croquis")\
    .set("relation","Aggregation")\
    .relatedFeatures(
      "ARENA2_CROQUIS",
      "LID_CROQUIS",
      ("ID_CROQUIS","IMAGEN"),
      "SELECT * FROM ARENA2_CROQUIS WHERE ARENA2_ACCIDENTES.ID_ACCIDENTE = ARENA2_CROQUIS.ID_ACCIDENTE;"
    )\
    .tag("dynform.readonly",True)\
    .tag("dynform.label.empty",True)

] 


class AccidentesParser(object):
  
  def __init__(self, fname, xml=None):
    self.fname = fname
    self.xml = xml
    self.informeCorriente = None
    self.accidenteCorriente = None
    self.tags = {}
    
  def getParserTags(self):
    return self.tags
    
  def close(self):
    self.xml = None
    self.informeCorriente = None
    self.accidenteCorriente = None
  
  def getXML(self):
    return self.xml
    
  def open(self):
    if self.xml == None:
      fileXml = open(self.fname,"r")
      data = fileXml.read()
      fileXml.close()
      self.xml = xmltodic.parse(data)
      #print self.xml
    
    self.informeCorriente = 0
    self.accidenteCorriente = 0
    self.rewind()

  def rewind(self):
    self.informeCorriente = 0
    self.accidenteCorriente = 0
  
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
  
  def getColumns(self):
    return COLUMNS_DEFINITION

  def getRowCount(self):
    self.rewind()
    rowCount = 0
    while True:
      informe, accidente = self.next()
      if accidente == None:
        return rowCount
      rowCount+=1
      
  def checkingNotSupportedKeys(self):
    informe, accidente = self.next()
    self.doCheckNotSupportedKeys(accidente)
    
  def doCheckNotSupportedKeys(self, accidente):
    # Optimizar: crear dos listas y restarlas
    notSupportedKeys = []
    for key in accidente.keys():
      found = False
      valueKey = key.replace("@","")
      for col in COLUMNS_DEFINITION:
        if col.name==valueKey or valueKey in GROUPS_DEFINITION:
            found = True
            break
      if not found:
        notSupportedKeys.append(key)
        
    if not notSupportedKeys:
      return None
    return notSupportedKeys
      
  def read(self):
    informe, accidente = self.next()
    
    #notSupportedKeys = self.doCheckNotSupportedKeys(accidente)
    #if notSupportedKeys != None:
    #    self.tags["notSupportedKeys"] = notSupportedKeys
        
    if accidente == None:
      return None

    accidente_id = None
    try:
      x = accidente.get("MAPAX", None)
      y = accidente.get("MAPAY", None)
      if x != None and y != None:
        geom = GeometryUtils.createPoint(float(y), float(x))
      else:
        geom = None
        
      accidente_id = accidente.get("@ID_ACCIDENTE", None)
      
      values = []

      values.append(parseToString(accidente_id))
      values.append(parseToString(informe.get("@COD_INFORME", None)))

      values.append(parseToString(accidente.get("@ID_ACCIDENTE", None)))

      values.append(parseToNumber(accidente.get("ESTADO_ACCIDENTE", None)))
      values.append(parseToString(accidente.get("OPERACION", None)))
      
      values.append(parseToString(accidente.get("FECHA_ACCIDENTE", None)))
      values.append(parseToString(accidente.get("HORA_ACCIDENTE", None)))
      values.append(parseToString(accidente.get("COD_PROVINCIA", None)))

      values.append(parseToString(accidente.get("COD_MUNICIPIO", None)))

      values.append(parseToString(accidente.get("COD_POBLACION", None)))
      values.append(parseToNull(accidente.get("ZONA", None)))
      values.append(parseToNull(accidente.get("TIPO_VIA", None)))

      values.append(parseToString(accidente.get("CARRETERA", None)))

      values.append(parseToNumber(accidente.get("KM", None)))

      values.append(parseToNull(accidente.get("TITULARIDAD_VIA", None)))

      values.append(parseToNull(accidente.get("SENTIDO", None)))


      values.append(parseToString(accidente.get("CALLE_CODIGO", None)))
      values.append(parseToString(accidente.get("CALLE_NOMBRE", None)))
      values.append(parseToString(accidente.get("CALLE_NUMERO", None)))

      values.append(parseToNumber(accidente.get("MAPAY", None)))
      values.append(parseToNumber(accidente.get("MAPAX", None)))
      values.append(geom) # Campo geometria calculado
      values.append(parseToNull(accidente.get("NUDO", None)))
      values.append(parseToNull(accidente.get("NUDO_INFO", None)))

      values.append(parseToString(accidente.get("CRUCE_CALLE", None)))
      values.append(parseToString(accidente.get("CRUCE_INE_CALLE", None)))

      values.append(parseToNumber(get2(accidente,"VICTIMAS","@TOTAL_VICTIMAS")))

      values.append(parseToNumber(get2(accidente,"VICTIMAS","TOTAL_MUERTOS")))

      values.append(parseToNumber(get2(accidente,"VICTIMAS","TOTAL_GRAVES")))

      values.append(parseToNumber(get2(accidente,"VICTIMAS","TOTAL_LEVES")))

      values.append(parseToNumber(get2(accidente,"VICTIMAS","TOTAL_ILESOS")))

      
      values.append(parseToNumber(accidente.get("TOTAL_VEHICULOS", None)))

      values.append(parseToNumber(accidente.get("TOTAL_CONDUCTORES", None)))

      values.append(parseToNumber(accidente.get("TOTAL_PASAJEROS", None)))

      values.append(parseToNumber(accidente.get("TOTAL_PEATONES", None)))

      values.append(parseToNumber(accidente.get("NUM_TURISMOS", None)))

      values.append(parseToNumber(accidente.get("NUM_FURGONETAS", None)))

      values.append(parseToNumber(accidente.get("NUM_CAMIONES", None)))

      values.append(parseToNumber(accidente.get("NUM_AUTOBUSES", None)))

      values.append(parseToNumber(accidente.get("NUM_CICLOMOTORES", None)))

      values.append(parseToNumber(accidente.get("NUM_MOTOCICLETAS", None)))

      values.append(parseToNumber(accidente.get("NUM_BICICLETAS", None)))

      values.append(parseToNumber(accidente.get("NUM_OTROS_VEHI", None)))

      
      values.append(parseToNull(get2(accidente,"TIPO_ACCIDENTE","TIPO_ACC_SALIDA")))
      values.append(parseToNull(get2(accidente,"TIPO_ACCIDENTE","TIPO_ACC_COLISION")))
      values.append(parseToNull(accidente.get("TIPO_ACC_ANIMAL", None)))

      values.append(parseToBool(accidente.get("SENTIDO_CONTRARIO", None)))

      values.append(parseToNull(get2(accidente,"CONDICION_NIVEL_CIRCULA","#text")))
      values.append(parseToBool(get2(accidente,"CONDICION_NIVEL_CIRCULA","@INFLU_NIVEL_CIRC")))
      values.append(parseToNull(get2(accidente,"CONDICION_FIRME","#text")))
      values.append(parseToBool(get2(accidente,"CONDICION_FIRME","@INFLU_SUP_FIRME")))
      values.append(parseToNull(get2(accidente,"CONDICION_ILUMINACION","#text")))
      values.append(parseToBool(get2(accidente,"CONDICION_ILUMINACION","@INFLU_ILUMINACION")))
      values.append(parseToNull(get2(accidente,"CONDICION_METEO","#text")))
      values.append(parseToBool(get2(accidente,"CONDICION_METEO","@INFLU_METEO")))
      values.append(parseToNull(get2(accidente,"CONDICION_NIEBLA","#text")))
      values.append(parseToNull(get2(accidente,"CONDICION_VIENTO","#text")))
      values.append(parseToNull(get2(accidente,"VISIB_RESTRINGIDA_POR","#text")))
      values.append(parseToBool(get2(accidente,"VISIB_RESTRINGIDA_POR","@INFLU_VISIBILIDAD")))

      values.append(parseToNull(accidente.get("CARACT_FUNCIONAL_VIA", None)))
      values.append(parseToNull(accidente.get("VEL_GENERICA_SENYALIZADA", None)))

      values.append(parseToNumber(accidente.get("VELOCIDAD", None)))
      values.append(parseToNull(accidente.get("SENTIDOS_VIA", None)))
      values.append(parseToNull(accidente.get("NUMERO_CALZADAS", None)))

      values.append(parseToNumber(get2(accidente,"NUM_CARRILES","@CARRILES_APTOS_CIRC_ASC")))
      values.append(parseToNumber(get2(accidente,"NUM_CARRILES","@CARRILES_APTOS_CIRC_DESC")))
      values.append(parseToNull(accidente.get("ANCHURA_CARRIL", None)))
      values.append(parseToNull(accidente.get("ARCEN", None)))

      values.append(parseToNull(get2(accidente,"ACERA","#text")))
      values.append(parseToBool(get2(accidente,"ACERA","@INFLU_ACERA")))
      values.append(parseToNumber(accidente.get("ANCHURA_ACERA", None)))

      values.append(parseToNull(accidente.get("TRAZADO_PLANTA", None)))
      values.append(parseToNull(accidente.get("TRAZADO_ALZADO", None)))
      values.append(parseToNull(accidente.get("MARCAS_VIALES", None)))
      values.append(parseToString(accidente.get("DESCRIPCION", None)))
      values.append(parseToString(accidente.get("OBSERVACIONES", None)))

      values.append(parseToBool(get2(accidente,"REGULACION_PRIORIDAD","@INFLU_PRIORIDAD")))
      values.append(parseToBool(get2(accidente,"REGULACION_PRIORIDAD","PRIORI_NORMA")))
      values.append(parseToBool(get2(accidente,"REGULACION_PRIORIDAD","PRIORI_AGENTE")))
      values.append(parseToBool(get2(accidente,"REGULACION_PRIORIDAD","PRIORI_SEMAFORO")))
      values.append(parseToBool(get2(accidente,"REGULACION_PRIORIDAD","PRIORI_VERT_STOP")))
      values.append(parseToBool(get2(accidente,"REGULACION_PRIORIDAD","PRIORI_VERT_CEDA")))
      values.append(parseToBool(get2(accidente,"REGULACION_PRIORIDAD","PRIORI_HORIZ_STOP")))
      values.append(parseToBool(get2(accidente,"REGULACION_PRIORIDAD","PRIORI_HORIZ_CEDA")))
      values.append(parseToBool(get2(accidente,"REGULACION_PRIORIDAD","PRIORI_MARCAS")))
      values.append(parseToBool(get2(accidente,"REGULACION_PRIORIDAD","PRIORI_PEA_NO_ELEV")))
      values.append(parseToBool(get2(accidente,"REGULACION_PRIORIDAD","PRIORI_PEA_ELEV")))
      values.append(parseToBool(get2(accidente,"REGULACION_PRIORIDAD","PRIORI_MARCA_CICLOS")))
      values.append(parseToBool(get2(accidente,"REGULACION_PRIORIDAD","PRIORI_CIRCUNSTANCIAL")))
      values.append(parseToBool(get2(accidente,"REGULACION_PRIORIDAD","PRIORI_OTRA")))

      values.append(parseToBool(get2(accidente,"ELEMENTOS_BALIZAMIENTO","PANELES_DIRECCIONALES")))
      values.append(parseToBool(get2(accidente,"ELEMENTOS_BALIZAMIENTO","HITOS_ARISTA")))
      values.append(parseToBool(get2(accidente,"ELEMENTOS_BALIZAMIENTO","CAPTAFAROS")))

      values.append(parseToBool(get2(accidente,"ELEMENTOS_SEPARACION_SENTIDO","SEPARA_LINEA_LONG_SEPARACION")))
      values.append(parseToBool(get2(accidente,"ELEMENTOS_SEPARACION_SENTIDO","SEPARA_CEBREADO")))
      values.append(parseToBool(get2(accidente,"ELEMENTOS_SEPARACION_SENTIDO","SEPARA_MEDIANA")))
      values.append(parseToBool(get2(accidente,"ELEMENTOS_SEPARACION_SENTIDO","SEPARA_BARRERA_SEGURIDAD")))
      values.append(parseToBool(get2(accidente,"ELEMENTOS_SEPARACION_SENTIDO","SEPARA_ZONA_PEATONAL")))
      values.append(parseToBool(get2(accidente,"ELEMENTOS_SEPARACION_SENTIDO","SEPARA_OTRA_SEPARACION")))
      values.append(parseToBool(get2(accidente,"ELEMENTOS_SEPARACION_SENTIDO","SEPARA_NINGUNA_SEPARACION")))

      values.append(parseToNull(get2(accidente,"BARRERA_SEGURIDAD","BARRERA_SEG_LAT_ASC")))
      values.append(parseToBool(get2(accidente,"BARRERA_SEGURIDAD","BARRERA_SEG_LAT_ASC_MOTO")))
      values.append(parseToNull(get2(accidente,"BARRERA_SEGURIDAD","BARRERA_SEG_LAT_DESC")))
      values.append(parseToBool(get2(accidente,"BARRERA_SEGURIDAD","BARRERA_SEG_LAT_DESC_MOTO")))
      values.append(parseToNull(get2(accidente,"BARRERA_SEGURIDAD","BARRERA_SEG_MEDIANA_ASC")))
      values.append(parseToBool(get2(accidente,"BARRERA_SEGURIDAD","BARRERA_SEG_MEDIANA_ASC_MOTO")))
      values.append(parseToNull(get2(accidente,"BARRERA_SEGURIDAD","BARRERA_SEG_MEDIANA_DESC")))
      values.append(parseToBool(get2(accidente,"BARRERA_SEGURIDAD","BARRERA_SEG_MEDIANA_DESC_MOTO")))

      values.append(parseToBool(get2(accidente,"ELEMENTOS_TRAMO","TRAMO_PUENTE")))
      values.append(parseToBool(get2(accidente,"ELEMENTOS_TRAMO","TRAMO_TUNEL")))
      values.append(parseToBool(get2(accidente,"ELEMENTOS_TRAMO","TRAMO_PASO")))
      values.append(parseToBool(get2(accidente,"ELEMENTOS_TRAMO","TRAMO_ESTRECHA")))
      values.append(parseToBool(get2(accidente,"ELEMENTOS_TRAMO","TRAMO_RESALTOS")))
      values.append(parseToBool(get2(accidente,"ELEMENTOS_TRAMO","TRAMO_BADEN")))
      values.append(parseToBool(get2(accidente,"ELEMENTOS_TRAMO","TRAMO_APARTADERO")))
      values.append(parseToBool(get2(accidente,"ELEMENTOS_TRAMO","TRAMO_NINGUNA")))

      values.append(parseToBool(get2(accidente,"CARACTERISTICAS_MARGEN","@INFLU_MARGEN")))
      values.append(parseToBool(get2(accidente,"CARACTERISTICAS_MARGEN","MARGEN_DESPEJADO")))
      values.append(parseToBool(get2(accidente,"CARACTERISTICAS_MARGEN","MARGEN_ARBOLES")))
      values.append(parseToBool(get2(accidente,"CARACTERISTICAS_MARGEN","MARGEN_OTROS_NATURALES")))
      values.append(parseToBool(get2(accidente,"CARACTERISTICAS_MARGEN","MARGEN_EDIFICIOS")))
      values.append(parseToBool(get2(accidente,"CARACTERISTICAS_MARGEN","MARGEN_POSTES")))
      values.append(parseToBool(get2(accidente,"CARACTERISTICAS_MARGEN","MARGEN_PUBLICIDAD")))
      values.append(parseToBool(get2(accidente,"CARACTERISTICAS_MARGEN","MARGEN_OTROS_ARTIFICIALES")))
      values.append(parseToBool(get2(accidente,"CARACTERISTICAS_MARGEN","MARGEN_OTROS_OBSTACULOS")))
      values.append(parseToBool(get2(accidente,"CARACTERISTICAS_MARGEN","MARGEN_DESC")))

      values.append(parseToBool(get2(accidente,"CIRCUNSTANCIAS_ESPECIALES_VIA","@INFLU_CIRCUNS_ESP")))
      values.append(parseToBool(get2(accidente,"CIRCUNSTANCIAS_ESPECIALES_VIA","CIRCUNS_ESP_NINGUNA")))
      values.append(parseToBool(get2(accidente,"notCIRCUNSTANCIAS_ESPECIALES_VIA","CIRCUNS_ESP_CONOS")))
      values.append(parseToBool(get2(accidente,"CIRCUNSTANCIAS_ESPECIALES_VIA","CIRCUNS_ESP_ZANJA")))
      values.append(parseToBool(get2(accidente,"CIRCUNSTANCIAS_ESPECIALES_VIA","CIRCUNS_ESP_TAPA")))
      values.append(parseToBool(get2(accidente,"CIRCUNSTANCIAS_ESPECIALES_VIA","CIRCUNS_ESP_OBRAS")))
      values.append(parseToBool(get2(accidente,"CIRCUNSTANCIAS_ESPECIALES_VIA","CIRCUNS_ESP_OBSTACULO")))
      values.append(parseToBool(get2(accidente,"CIRCUNSTANCIAS_ESPECIALES_VIA","CIRCUNS_ESP_DESPREND")))
      values.append(parseToBool(get2(accidente,"CIRCUNSTANCIAS_ESPECIALES_VIA","CIRCUNS_ESP_ESCALON")))
      values.append(parseToBool(get2(accidente,"CIRCUNSTANCIAS_ESPECIALES_VIA","CIRCUNS_ESP_FBACHES")))
      values.append(parseToBool(get2(accidente,"CIRCUNSTANCIAS_ESPECIALES_VIA","CIRCUNS_ESP_FDETERIORADO")))
      values.append(parseToBool(get2(accidente,"CIRCUNSTANCIAS_ESPECIALES_VIA","CIRCUNS_ESP_OTRAS")))
      values.append(parseToBool(get2(accidente,"CIRCUNSTANCIAS_ESPECIALES_VIA","CIRCUNS_ESP_DESC")))

      values.append(parseToBool(get2(accidente,"DELIMITACION_CALZADA","@INFLU_DELIM_CALZADA")))
      values.append(parseToBool(get2(accidente,"DELIMITACION_CALZADA","DELIM_CALZADA_BORDILLO")))
      values.append(parseToBool(get2(accidente,"DELIMITACION_CALZADA","DELIM_CALZADA_VALLAS")))
      values.append(parseToBool(get2(accidente,"DELIMITACION_CALZADA","DELIM_CALZADA_SETOS")))
      values.append(parseToBool(get2(accidente,"DELIMITACION_CALZADA","DELIM_CALZADA_MARCAS")))
      values.append(parseToBool(get2(accidente,"DELIMITACION_CALZADA","DELIM_CALZADA_BARRERA")))
      values.append(parseToBool(get2(accidente,"DELIMITACION_CALZADA","DELIM_CALZADA_ISLETA")))
      values.append(parseToBool(get2(accidente,"DELIMITACION_CALZADA","DELIM_CALZADA_PEATONAL")))
      values.append(parseToBool(get2(accidente,"DELIMITACION_CALZADA","DELIM_CALZADA_OTRA")))
      values.append(parseToBool(get2(accidente,"DELIMITACION_CALZADA","DELIM_CALZADA_SIN_DELIM")))

      values.append(parseToBool(get2(accidente,"FACTORES_CONCURRENTES","FC_CON_DISTRAIDA")))
      values.append(parseToBool(get2(accidente,"FACTORES_CONCURRENTES","FC_VEL_INADECUADA")))
      values.append(parseToBool(get2(accidente,"FACTORES_CONCURRENTES","FC_PRIORIDAD")))
      values.append(parseToBool(get2(accidente,"FACTORES_CONCURRENTES","FC_SEGURIDAD")))
      values.append(parseToBool(get2(accidente,"FACTORES_CONCURRENTES","FC_ADELANTAMIENTO")))
      values.append(parseToBool(get2(accidente,"FACTORES_CONCURRENTES","FC_GIRO")))
      values.append(parseToBool(get2(accidente,"FACTORES_CONCURRENTES","FC_CON_NEGLIGENTE")))
      values.append(parseToBool(get2(accidente,"FACTORES_CONCURRENTES","FC_CON_TEMERARIA")))
      values.append(parseToBool(get2(accidente,"FACTORES_CONCURRENTES","FC_IRRUPCION_ANIMAL")))
      values.append(parseToBool(get2(accidente,"FACTORES_CONCURRENTES","FC_IRRUPCION_PEATON")))
      values.append(parseToBool(get2(accidente,"FACTORES_CONCURRENTES","FC_ALCOHOL")))
      values.append(parseToBool(get2(accidente,"FACTORES_CONCURRENTES","FC_DROGAS")))
      values.append(parseToBool(get2(accidente,"FACTORES_CONCURRENTES","FC_ESTADO_VIA")))
      values.append(parseToBool(get2(accidente,"FACTORES_CONCURRENTES","FC_METEORO")))
      values.append(parseToBool(get2(accidente,"FACTORES_CONCURRENTES","FC_CANSANCIO")))
      values.append(parseToBool(get2(accidente,"FACTORES_CONCURRENTES","FC_INEXPERIENCIA")))
      values.append(parseToBool(get2(accidente,"FACTORES_CONCURRENTES","FC_AVERIA")))
      values.append(parseToBool(get2(accidente,"FACTORES_CONCURRENTES","FC_OBRAS")))
      values.append(parseToBool(get2(accidente,"FACTORES_CONCURRENTES","FC_MAL_ESTADO_VEHI")))
      values.append(parseToBool(get2(accidente,"FACTORES_CONCURRENTES","FC_ENFERMEDAD")))
      values.append(parseToBool(get2(accidente,"FACTORES_CONCURRENTES","FC_SENYALIZACION")))
      values.append(parseToBool(get2(accidente,"FACTORES_CONCURRENTES","FC_OBSTACULO")))
      values.append(parseToBool(get2(accidente,"FACTORES_CONCURRENTES","FC_OTRO_FACTOR")))

      values.append(self.getQuincenaFromCodInforme(parseToString(informe.get("@COD_INFORME", None)))) # Quincena

      values.append(None) # VEHICULOS
      values.append(None) # Peatones
      values.append(None) # Croquis

    except:
      ex = sys.exc_info()[1]
      gvsig.logger("No se puede leer el accidente %s/%s. %s" % (self.accidenteCorriente,accidente_id,str(ex)), gvsig.LOGGER_WARN, ex)
      raise
      
    return values
    
  def getQuincenaFromCodInforme(self, cod):
      if cod == None:
        return None
      return cod.replace('_', '')[-8:]
      
  def next(self):
    if self.informeCorriente == None:
      return None, None
    
    informes = self.getInformes()
    while self.informeCorriente < len(informes):
      informe = informes[self.informeCorriente]
      #print "Informe: ", get1(informe,"@COD_INFORME"), self.informeCorriente
      accidentes = self.getAccidentes(informe)
      if self.accidenteCorriente < len(accidentes):
        accidente = accidentes[self.accidenteCorriente]
        #print "Accidente: ", get1(accidente,"@ID_ACCIDENTE"), self.accidenteCorriente
        self.accidenteCorriente += 1
        return informe, accidente

      self.informeCorriente += 1
      self.accidenteCorriente = 0

    self.informeCorriente = None
    return None, None
  
def test1():
  fname = '/home/osc/gva_arena2/test/TV_12_2020_07_Q1/victimas.xml'  
  p = AccidentesParser(fname)
  p.open()
  print "Num accidentes: ", p.getRowCount()
  p.rewind()
  while True:
    line = p.read()
    if line == None:
      break
    print p.accidenteCorriente, line[0]
    #print len(line)
    return
      
def test2():
  fname = '/home/osc/gva_arena2/test/TV_12_2020_07_Q1/victimas.xml'  
  p = AccidentesParser(fname)
  p.open()
  columns_not_dgt = []
  for c in COLUMNS_DEFINITION:
    if not c.name.endswith("_DGT"):
      columns_not_dgt.append(c.name)
  

  p.rewind()
  while True:
    line = p.read()
    if line == None:
      break
    print p.accidenteCorriente, line[0]
    print "Len of values: ", len(line)
    print "NOT DGT COlS: ", len(columns_not_dgt)
    return

def test3():
  #fname = '/home/osc/gva_arena2/test/TV_12_2020_07_Q1/victimas.xml'  
  fname = '/home/osc/gva_arena2/XML_test/victor_005/XML-CastellAleixandre/danyos-prueba-10001.xml'
  p = AccidentesParser(fname)
  p.open()
  print "Num accidentes: ", p.getRowCount()
  p.rewind()
  while True:
    print "In"
    line = p.read()
    if line == None:
      break
    print p.accidenteCorriente, line[0]
    for i in range(0, len(line)):
      print COLUMNS_DEFINITION[i].name, ": ", line[i]
    print len(line)
    return

def test5(fname=None):
  if fname == None:
    fname = '/home/osc/gva_arena2/test/TV_12_2020_07_Q1/victimas.xml'  
  p = AccidentesParser(fname)
  p.open()
  print "\t Num accidentes: ", p.getRowCount()
  p.rewind()
  while True:
    notValidKeys = p.checkingNotSupportedKeys()
    if notValidKeys!=None:
      print "Not valid keys: ", notValidKeys
    return

def test4(): #TestAllKeys

    import os
    path = "/home/osc/gva_arena2/CV_xml_por_anyo/2020/"
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if '.xml' in file:
                files.append(os.path.join(r, file))
    n = 0
    print "TOTAL FICHEROS: ", len(files)
    for f in files:
        print(f)
        test5(f)
        n+=1
        if (n>1000):
           break
        
        
def main(*args):
  #test1()
  test3()
  #generate_translations(COLUMNS_DEFINITION)
