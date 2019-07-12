# encoding: utf-8

import gvsig

from org.gvsig.fmap.geom.aggregate import MultiPolygon
from org.gvsig.scripting.app.extension import ScriptingUtils
import xmltodic
from org.gvsig.fmap.geom import GeometryUtils

from util import sino2bool, null2empty, null2zero, get1, get2, Descriptor

COLUMNS_DEFINITION = [
  Descriptor("LID_ACCIDENTE","String",20,hidden=True, pk=True)\
    .tag("dynform.readonly",True),
  Descriptor("COD_INFORME","String",20,
    label="_Codigo_informe",
    shortLabel="_Cod_informe")\
    .tag("dynform.readonly",True)\
    .foreingkey("ARENA2_INFORMES","COD_INFORME","FORMAT('%s',COD_INFORME)"),
  Descriptor("ID_ACCIDENTE","String",20, 
    label="_Codigo_accidente",
    shortLabel="_Cod_accidente")\
    .tag("dynform.readonly",True)\
    .tag("DAL.Search.Attribute.Priority",1),
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
    .tag("dynform.readonly",True)\
    .tag("DAL.Search.Attribute.Priority",2),
  Descriptor("COD_MUNICIPIO","String",100,  
    label="_Municipio")\
    .tag("dynform.readonly",True),
  Descriptor("COD_POBLACION","String",100,  
    label="_Poblacion")\
    .tag("dynform.readonly",True),
  Descriptor("ZONA","Integer",  
    label="_Zona")\
    .tag("dynform.readonly",True)\
    .selectablefk("ARENA2_DIC_ZONA"),
  Descriptor("TIPO_VIA","Integer",
    label="_Tipo_de_via",
    shortLabel="_Tipo_via")\
    .selectablefk("ARENA2_DIC_TIPO_VIA"),
  Descriptor("TIPO_VIA_DGT","Integer",  
    label="_Tipo_de_via_original",
    shortLabel="_Tipo_via_orig")\
    .tag("dynform.readonly",True)\
    .selectablefk("ARENA2_DIC_TIPO_VIA"),

  Descriptor("CARRETERA","String",
    label="_Carretera")\
    .tag("DAL.Search.Attribute.Priority",3),
  Descriptor("CARRETERA_DGT","String",  
    label="_Carretera_original",
    shortLabel="_Carretera_orig")\
    .tag("dynform.readonly",True)\
    .tag("DAL.Search.Attribute.Priority",3),
  Descriptor("KM","Double", 
    label="_Punto_kilometrico",
    shortLabel="_Pk")\
    .tag("dynform.readonly",True)\
    .tag("DAL.Search.Attribute.Priority",4),
  Descriptor("TITULARIDAD_VIA","Integer",
    label="_Titularidad_de_la_via",
    shortLabel="_Titularidad_via")\
    .selectablefk("ARENA2_DIC_TITULARIDAD_VIA"),

  Descriptor("TITULARIDAD_VIA_DGT","Integer",  
    label="_Titularidad_de_la_via_original",
    shortlabel="_Titularidad_via_orig")\
    .tag("dynform.readonly",True)\
    .selectablefk("ARENA2_DIC_TITULARIDAD_VIA"),
  Descriptor("SENTIDO","Integer",  
    label="_Sentido")\
    .tag("dynform.readonly",True)\
    .selectablefk("ARENA2_DIC_SENTIDO")\
    .tag("DAL.Search.Attribute.Priority",5),
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
    .selectablefk("ARENA2_DIC_NUDO"),
  Descriptor("NUDO_INFO","Integer", 
    label="_Informacion_nudo",
    shortLabel="_Inf_nudo")\
    .tag("dynform.readonly",True)\
    .selectablefk("ARENA2_DIC_NUDO_INFORMACION"),
  Descriptor("CRUCE_CALLE","String",150, 
    label="_Cruce"),
  Descriptor("CRUCE_INE_CALLE","String",10, 
    label="_Cruce_INE")\
    .tag("dynform.readonly",True),
  
  Descriptor("TOTAL_VICTIMAS","Integer",
    label="_Total_victimas",
    shortlabel="_Victimas")\
    .tag("dynform.readonly",True),
  Descriptor("TOTAL_MUERTOS","Integer",
    label="_Total_muertos",
    shortlabel="_Muertos")\
    .tag("dynform.readonly",True)\
    .tag("DAL.Search.Attribute.Priority",10),
  Descriptor("TOTAL_GRAVES","Integer",
    label="_Total_graves",
    shortlabel="_Graves")\
    .tag("dynform.readonly",True)\
    .tag("DAL.Search.Attribute.Priority",11),
  Descriptor("TOTAL_LEVES","Integer",
    label="_Total_Leves",
    shortlabel="_Leves")\
    .tag("dynform.readonly",True)\
    .tag("DAL.Search.Attribute.Priority",12),
  Descriptor("TOTAL_ILESOS","Integer",
    label="_Total_ilesos",
    shortlabel="_Ilesos")\
    .tag("dynform.readonly",True),

  Descriptor("TOTAL_VEHICULOS","Integer", 
    label="_Total_vehiculos_implicados",
    shortlabel="_Tot_vehiculos")\
    .tag("dynform.readonly",True)\
    .tag("DAL.Search.Attribute.Priority",13),
  Descriptor("TOTAL_CONDUCTORES","Integer", 
    label="_Total_conductores_implicados",
    shortlabel="_Tot_conductores")\
    .tag("dynform.readonly",True),
  Descriptor("TOTAL_PASAJEROS","Integer", 
    label="_Total_pasajeros_implicados",
    shortlabel="_Tot_pasajeros")\
    .tag("dynform.readonly",True),
  Descriptor("TOTAL_PEATONES","Integer", 
    label="_Total_peatones_implicados",
    shortlabel="_Tot_peatones")\
    .tag("dynform.readonly",True),
  Descriptor("NUM_TURISMOS","Integer", 
    label="_Num_turismos_implicados",
    shortlabel="_Num_turismos")\
    .tag("dynform.readonly",True),
  Descriptor("NUM_FURGONETAS","Integer", 
    label="_Num_furgonetas_implicadas",
    shortlabel="_Num_furgonetas")\
    .tag("dynform.readonly",True),
  Descriptor("NUM_CAMIONES","Integer", 
    label="_Num_camiones_implicados",
    shortlabel="_Num_camiones")\
    .tag("dynform.readonly",True),
  Descriptor("NUM_AUTOBUSES","Integer", 
    label="_Num_autobuses_implicados",
    shortlabel="_Num_autobuses")\
    .tag("dynform.readonly",True),
  Descriptor("NUM_CICLOMOTORES","Integer", 
    label="_Num_ciclomotores_implicados",
    shortlabel="_Num_ciclomotores")\
    .tag("dynform.readonly",True),
  Descriptor("NUM_MOTOCICLETAS","Integer", 
    label="_Num_motocicletas_implicadas",
    shortlabel="_Num_motocicletas")\
    .tag("dynform.readonly",True),
  Descriptor("NUM_BICICLETAS","Integer", 
    label="_Num_bicicletas_implicadas",
    shortlabel="_Num_bicicletas")\
    .tag("dynform.readonly",True),
  Descriptor("NUM_OTROS_VEHI","Integer", 
    label="_Num_otros_vehiculos_implicados",
    shortlabel="_Num_otros_vehiculos")\
    .tag("dynform.readonly",True),

  Descriptor("TIPO_ACC_SALIDA","Integer", 
    label="_Tipo_accidente_Salida")\
    .tag("dynform.readonly",True)\
    .selectablefk("ARENA2_DIC_TIPO_ACCIDENTE_SALIDA"),
  Descriptor("TIPO_ACC_COLISION","Integer", 
    label="_Tipo_accidente_Colision")\
    .tag("dynform.readonly",True)\
    .selectablefk("ARENA2_DIC_TIPO_ACCIDENTE_COLISION"),
  Descriptor("TIPO_ACC_ANIMAL","Integer", 
    label="_Especie_del_animal")\
    .tag("dynform.readonly",True)\
    .selectablefk("ARENA2_DIC_TIPO_ACCIDENTE_ANIMAL"),
  
  
  Descriptor("SENTIDO_CONTRARIO","Boolean", 
    label="_Circular_sentido_contrario")\
    .tag("dynform.readonly",True),
    
  Descriptor("CONDICION_NIVEL_CIRCULA","Integer", 
    label="_Nivel_circulacion")\
    .tag("dynform.readonly",True)\
    .selectablefk("ARENA2_DIC_NIVEL_CIRCULACION"),
  Descriptor("INFLU_NIVEL_CIRC","Boolean",  
    label="_Influye_nivel_circulacion")\
    .tag("dynform.readonly",True),
  Descriptor("CONDICION_FIRME","Integer",  
    label="_Condicion_del_firme")\
    .tag("dynform.readonly",True)\
    .selectablefk("ARENA2_DIC_CONDICION_FIRME"),
  Descriptor("INFLU_SUP_FIRME","Boolean",  
    label="_Influye_firme")\
    .tag("dynform.readonly",True),
  Descriptor("CONDICION_ILUMINACION","Integer",  
    label="_Iluminacion")\
    .tag("dynform.readonly",True)\
    .selectablefk("ARENA2_DIC_ILUMINACION"),
  Descriptor("INFLU_ILUMINACION","Boolean",  
    label="_Influye_iluminacion")\
    .tag("dynform.readonly",True),
  Descriptor("CONDICION_METEO","Integer",  
    label="_Meteorologia")\
    .tag("dynform.readonly",True)\
    .selectablefk("ARENA2_DIC_METEO"),
  Descriptor("INFLU_METEO","Boolean",  
    label="_Influye_meteorologia")\
    .tag("dynform.readonly",True),

  Descriptor("CONDICION_NIEBLA","Integer",  
    label="_Niebla")\
    .tag("dynform.readonly",True)\
    .selectablefk("ARENA2_DIC_NIEBLA"),
  Descriptor("CONDICION_VIENTO","Integer",  
    label="_Viento_fuerte")\
    .tag("dynform.readonly",True)\
    .selectablefk("ARENA2_DIC_VIENTO"),

  
  Descriptor("VISIB_RESTRINGIDA_POR","Integer",  
    label="_Visibilidad")\
    .tag("dynform.readonly",True)\
    .selectablefk("ARENA2_DIC_VISIBILIDAD_RESTRINGIDA_POR"),
  Descriptor("INFLU_VISIBILIDAD","Boolean",  
    label="_Influye visibilidad")\
    .tag("dynform.readonly",True),
    
  Descriptor("CARACT_FUNCIONAL_VIA","Integer", 
    label="_Caracteristicas_funcionales_de_la_via",
    shortLabel="_Caracteisticas_via")\
    .tag("dynform.readonly",True)\
    .selectablefk("ARENA2_DIC_CARACT_FUNCIONAL_VIA"),
  Descriptor("VEL_GENERICA_SENYALIZADA","Integer", 
    label="_Velocidad_generica")\
    .tag("dynform.readonly",True)\
    .selectablefk("ARENA2_DIC_VEL_GENERICA"),

  Descriptor("VELOCIDAD","Double", 
    label="_Velocidad")\
    .tag("dynform.readonly",True),
  Descriptor("SENTIDOS_VIA","Integer", 
    label="_Sentidos_via",
    shortlabel="_Sentidos")\
    .selectablefk("ARENA2_DIC_SENTIDOS_VIA")\
    .tag("dynform.readonly",True),
  Descriptor("NUMERO_CALZADAS","Integer", 
    label="_Numero_de_calzadas",
    shortlabel="_Num_calzadas")\
    .tag("dynform.readonly",True)\
    .selectablefk("ARENA2_DIC_NUMERO_CALZADAS"),
  Descriptor("CARRILES_APTOS_CIRC_ASC","Integer", 
    label="_Carriles_aptos_circular_ascendente",
    shortlabel="_Carr_aptos_cir_asc")\
    .tag("dynform.readonly",True),
  Descriptor("CARRILES_APTOS_CIRC_DESC","Integer", 
    label="_Carriles_aptos_circular_descenente",
    shortlabel="_Carr_aptos_cir_desc")\
    .tag("dynform.readonly",True),
    
  Descriptor("ANCHURA_CARRIL","Integer", 
    label="_Anchura_de_carril",
    shortlabel="_Anchura_carril")\
    .tag("dynform.readonly",True)\
    .selectablefk("ARENA2_DIC_ANCHURA_CARRIL"),
  Descriptor("ARCEN","Integer", 
    label="_Arcen")\
    .tag("dynform.readonly",True)\
    .selectablefk("ARENA2_DIC_ANCHURA_ARCEN"),
  Descriptor("ACERA","Integer", 
    label="_Acera")\
    .tag("dynform.readonly",True)\
    .selectablefk("ARENA2_DIC_ACERA"),
  Descriptor("INFU_ACERA","Boolean", 
    label="_Influye_la_acera",
    shortLabel="_Influye_acera")\
    .tag("dynform.readonly",True),
  Descriptor("ANCHURA_ACERA","Integer", 
    label="_Anchua_acera")\
    .tag("dynform.readonly",True),
    
  Descriptor("TRAZADO_PLANTA","Integer", 
    label="_Trazado_planta")\
    .tag("dynform.readonly",True)
    .selectablefk("ARENA2_DIC_TRAZADO_PLANTA"),
  Descriptor("TRAZADO_ALZADO","Integer", 
    label="_Trazado_alzado")\
    .tag("dynform.readonly",True)\
    .selectablefk("ARENA2_DIC_TRAZADO_ALZADO"),
  Descriptor("MARCAS_VIALES","Integer", 
    label="_Marcas_viales")\
    .tag("dynform.readonly",True)\
    .selectablefk("ARENA2_DIC_MARCAS_VIALES"),

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
    .selectablefk("ARENA2_DIC_TIPO_BARRERA"),
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
    .selectablefk("ARENA2_DIC_TIPO_BARRERA"),
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
    .selectablefk("ARENA2_DIC_TIPO_BARRERA"),
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
    .selectablefk("ARENA2_DIC_TIPO_BARRERA"),
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

  Descriptor("VEHICULOS","List",
    label="_Vehiculos",
    group="_Vehiculos")\
    .relatedFeatures(
      "ARENA2_VEHICULOS",
      "LID_VEHICULO",
      ("ID_VEHICULO","NACIONALIDAD","TIPO_VEHICULO","MARCA_NOMBRE","MODELO"),
      "FEATURES('ARENA2_VEHICULOS',FORMAT('ID_ACCIDENTE = ''%s''',ID_ACCIDENTE))"
    )\
    .tag("dynform.readonly",True)\
    .set("dynform.label.empty",True),
  Descriptor("PEATONES","List",
    label="_Peatones",
    group="_Peatones")\
    .relatedFeatures(
      "ARENA2_PEATONES",
      "LID_PEATON",
      ("ID_PEATON","FECHA_NACIMIENTO","SEXO","PAIS_RESIDENCIA","PROVINCIA_RESIDENCIA","MUNICIPIO_RESIDENCIA"),
      "FEATURES('ARENA2_PEATONES',FORMAT('ID_ACCIDENTE = ''%s''',ID_ACCIDENTE))"
    )\
    .tag("dynform.readonly",True)\
    .set("dynform.label.empty",True),

  Descriptor("CROQUIS","List",
    label="_Croquis",
    group="_Croquis")\
    .relatedFeatures(
      "ARENA2_CROQUIS",
      "LID_CROQUIS",
      ("ID_CROQUIS","IMAGEN"),
      "FEATURES('ARENA2_CROQUIS',FORMAT('ID_ACCIDENTE = ''%s''',ID_ACCIDENTE))"
    )\
    .tag("dynform.readonly",True)\
    .set("dynform.label.empty",True)

] 


class AccidentesParser(object):
  
  def __init__(self, fname, xml=None):
    self.fname = fname
    self.xml = xml
    self.informeCorriente = None
    self.accidenteCorriente = None
    self.columns = None

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
    accidentes = informe["ACCIDENTES"]['ACCIDENTE']
    if not isinstance(accidentes,list):
      accidentes = [ accidentes ]
    return accidentes
  
  def getColumns(self):
    if self.columns!=None:
      return self.columns
    self.columns = COLUMNS_DEFINITION
    return self.columns

  def getRowCount(self):
    self.rewind()
    rowCount = 0
    while True:
      informe, accidente = self.next()
      if accidente == None:
        return rowCount
      rowCount+=1
      
   
  def read(self):
    informe, accidente = self.next()
    if accidente == None:
      return None

    
    x = accidente.get("MAPAX", None)
    y = accidente.get("MAPAY", None)
    if x != None and y != None:
      geom = GeometryUtils.createPoint(float(x), float(y))
    else:
      geom = None
    
    values = [
      null2empty(accidente.get("@ID_ACCIDENTE", None)),
      null2empty(informe.get("@COD_INFORME", None)),

      null2empty(accidente.get("@ID_ACCIDENTE", None)),
      null2empty(accidente.get("FECHA_ACCIDENTE", None)),
      null2empty(accidente.get("HORA_ACCIDENTE", None)),
      null2empty(accidente.get("COD_PROVINCIA", None)),
      null2empty(accidente.get("COD_MUNICIPIO", None)),
      null2empty(accidente.get("COD_POBLACION", None)),
      null2zero(accidente.get("ZONA", None)),
      null2zero(accidente.get("TIPO_VIA", None)),
      null2zero(accidente.get("TIPO_VIA", None)),
      null2empty(accidente.get("CARRETERA", None)),
      null2empty(accidente.get("CARRETERA", None)),
      null2zero(accidente.get("KM", None)),
      null2zero(accidente.get("TITULARIDAD_VIA", None)),
      null2zero(accidente.get("TITULARIDAD_VIA", None)),
      null2zero(accidente.get("SENTIDO", None)),

      null2empty(accidente.get("CALLE_CODIGO", None)),
      null2empty(accidente.get("CALLE_NOMBRE", None)),
      null2empty(accidente.get("CALLE_NUMERO", None)),

      null2zero(accidente.get("MAPAY", None)),
      null2zero(accidente.get("MAPAX", None)),
      geom, # Campo geometria calculado
      null2zero(accidente.get("NUDO", None)),
      null2zero(accidente.get("NUDO_INFO", None)),
      
      null2empty(accidente.get("CRUCE_CALLE", None)),
      null2empty(accidente.get("CRUCE_INE_CALLE", None)),
      
      null2zero(get2(accidente,"VICTIMAS","@TOTAL_VICTIMAS")),
      null2zero(get2(accidente,"VICTIMAS","TOTAL_MUERTOS")),
      null2zero(get2(accidente,"VICTIMAS","TOTAL_GRAVES")),
      null2zero(get2(accidente,"VICTIMAS","TOTAL_LEVES")),
      null2zero(get2(accidente,"VICTIMAS","TOTAL_ILESOS")),

      null2zero(accidente.get("TOTAL_VEHICULOS", None)),
      null2zero(accidente.get("TOTAL_CONDUCTORES", None)),
      null2zero(accidente.get("TOTAL_PASAJEROS", None)),
      null2zero(accidente.get("TOTAL_PEATONES", None)),
      null2zero(accidente.get("NUM_TURISMOS", None)),
      null2zero(accidente.get("NUM_FURGONETAS", None)),
      null2zero(accidente.get("NUM_CAMIONES", None)),
      null2zero(accidente.get("NUM_AUTOBUSES", None)),
      null2zero(accidente.get("NUM_CICLOMOTORES", None)),
      null2zero(accidente.get("NUM_MOTOCICLETAS", None)),
      null2zero(accidente.get("NUM_BICICLETAS", None)),
      null2zero(accidente.get("NUM_OTROS_VEHI", None)),
      
      null2zero(get2(accidente,"TIPO_ACCIDENTE","TIPO_ACC_SALIDA")),
      null2zero(get2(accidente,"TIPO_ACCIDENTE","TIPO_ACC_COLISION")),
      null2zero(get2(accidente,"TIPO_ACCIDENTE","TIPO_ACC_ANIMAL")),
      
      sino2bool(accidente.get("SENTIDO_CONTRARIO", None)),

      null2zero(get2(accidente,"CONDICION_NIVEL_CIRCULA","#text")),
      sino2bool(get2(accidente,"CONDICION_NIVEL_CIRCULA","@INFLU_NIVEL_CIRC")),
      null2zero(get2(accidente,"CONDICION_FIRME","#text")),
      sino2bool(get2(accidente,"CONDICION_FIRME","@INFLU_SUP_FIRME")),
      null2zero(get2(accidente,"CONDICION_ILUMINACION","#text")),
      sino2bool(get2(accidente,"CONDICION_ILUMINACION","@INFLU_ILUMINACION")),
      null2zero(get2(accidente,"CONDICION_METEO","#text")),
      sino2bool(get2(accidente,"CONDICION_METEO","@INFLU_METEO")),
      null2zero(get2(accidente,"CONDICION_NIEBLA","#text")),
      null2zero(get2(accidente,"CONDICION_VIENTO","#text")),
      null2zero(get2(accidente,"VISIB_RESTRINGIDA_POR","#text")),
      sino2bool(get2(accidente,"VISIB_RESTRINGIDA_POR","@INFLU_VISIBILIDAD")),

      null2zero(accidente.get("CARACT_FUNCIONAL_VIA", None)),
      null2zero(accidente.get("VEL_GENERICA_SENYALIZADA", None)),

      null2zero(accidente.get("VELOCIDAD", None)),
      null2zero(accidente.get("SENTIDOS_VIA", None)),
      null2zero(accidente.get("NUMERO_CALZADAS", None)),

      null2zero(get2(accidente,"NUM_CARRILES","@CARRILES_APTOS_CIRC_ASC")),
      null2zero(get2(accidente,"NUM_CARRILES","@CARRILES_APTOS_CIRC_DESC")),
      null2zero(accidente.get("ANCHURA_CARRIL", None)),
      null2zero(accidente.get("ARCEN", None)),

      null2zero(get2(accidente,"ACERA","#text")),
      sino2bool(get2(accidente,"ACERA","@INFU_ACERA")),
      null2zero(accidente.get("ANCHURA_ACERA", None)),
      
      null2zero(accidente.get("TRAZADO_PLANTA", None)),
      null2zero(accidente.get("TRAZADO_ALZADO", None)),
      null2zero(accidente.get("MARCAS_VIALES", None)),
      null2empty(accidente.get("DESCRIPCION", None)),
      null2empty(accidente.get("OBSERVACIONES", None)),

      sino2bool(get2(accidente,"REGULACION_PRIORIDAD","@INFLU_PRIORIDAD")),
      sino2bool(get2(accidente,"REGULACION_PRIORIDAD","PRIORI_NORMA")),
      sino2bool(get2(accidente,"REGULACION_PRIORIDAD","PRIORI_AGENTE")),
      sino2bool(get2(accidente,"REGULACION_PRIORIDAD","PRIORI_SEMAFORO")),
      sino2bool(get2(accidente,"REGULACION_PRIORIDAD","PRIORI_VERT_STOP")),
      sino2bool(get2(accidente,"REGULACION_PRIORIDAD","PRIORI_VERT_CEDA")),
      sino2bool(get2(accidente,"REGULACION_PRIORIDAD","PRIORI_HORIZ_STOP")),
      sino2bool(get2(accidente,"REGULACION_PRIORIDAD","PRIORI_HORIZ_CEDA")),
      sino2bool(get2(accidente,"REGULACION_PRIORIDAD","PRIORI_MARCAS")),
      sino2bool(get2(accidente,"REGULACION_PRIORIDAD","PRIORI_PEA_NO_ELEV")),
      sino2bool(get2(accidente,"REGULACION_PRIORIDAD","PRIORI_PEA_ELEV")),
      sino2bool(get2(accidente,"REGULACION_PRIORIDAD","PRIORI_MARCA_CICLOS")),
      sino2bool(get2(accidente,"REGULACION_PRIORIDAD","PRIORI_CIRCUNSTANCIAL")),
      sino2bool(get2(accidente,"REGULACION_PRIORIDAD","PRIORI_OTRA")),

      sino2bool(get2(accidente,"ELEMENTOS_BALIZAMIENTO","PANELES_DIRECCIONALES")),
      sino2bool(get2(accidente,"ELEMENTOS_BALIZAMIENTO","HITOS_ARISTA")),
      sino2bool(get2(accidente,"ELEMENTOS_BALIZAMIENTO","CAPTAFAROS")),

      sino2bool(get2(accidente,"ELEMENTOS_SEPARACION_SENTIDO","SEPARA_LINEA_LONG_SEPARACION")),
      sino2bool(get2(accidente,"ELEMENTOS_SEPARACION_SENTIDO","SEPARA_CEBREADO")),
      sino2bool(get2(accidente,"ELEMENTOS_SEPARACION_SENTIDO","SEPARA_MEDIANA")),
      sino2bool(get2(accidente,"ELEMENTOS_SEPARACION_SENTIDO","SEPARA_BARRERA_SEGURIDAD")),
      sino2bool(get2(accidente,"ELEMENTOS_SEPARACION_SENTIDO","SEPARA_ZONA_PEATONAL")),
      sino2bool(get2(accidente,"ELEMENTOS_SEPARACION_SENTIDO","SEPARA_OTRA_SEPARACION")),
      sino2bool(get2(accidente,"ELEMENTOS_SEPARACION_SENTIDO","SEPARA_NINGUNA_SEPARACION")),

      null2zero(get2(accidente,"BARRERA_SEGURIDAD","BARRERA_SEG_LAT_ASC")),
      sino2bool(get2(accidente,"BARRERA_SEGURIDAD","BARRERA_SEG_LAT_ASC_MOTO")),
      null2zero(get2(accidente,"BARRERA_SEGURIDAD","BARRERA_SEG_LAT_DESC")),
      sino2bool(get2(accidente,"BARRERA_SEGURIDAD","BARRERA_SEG_LAT_DESC_MOTO")),
      null2zero(get2(accidente,"BARRERA_SEGURIDAD","BARRERA_SEG_MEDIANA_ASC")),
      sino2bool(get2(accidente,"BARRERA_SEGURIDAD","BARRERA_SEG_MEDIANA_ASC_MOTO")),
      null2zero(get2(accidente,"BARRERA_SEGURIDAD","BARRERA_SEG_MEDIANA_DESC")),
      sino2bool(get2(accidente,"BARRERA_SEGURIDAD","BARRERA_SEG_MEDIANA_DESC_MOTO")),

      sino2bool(get2(accidente,"ELEMENTOS_TRAMO","TRAMO_PUENTE")),
      sino2bool(get2(accidente,"ELEMENTOS_TRAMO","TRAMO_TUNEL")),
      sino2bool(get2(accidente,"ELEMENTOS_TRAMO","TRAMO_PASO")),
      sino2bool(get2(accidente,"ELEMENTOS_TRAMO","TRAMO_ESTRECHA")),
      sino2bool(get2(accidente,"ELEMENTOS_TRAMO","TRAMO_RESALTOS")),
      sino2bool(get2(accidente,"ELEMENTOS_TRAMO","TRAMO_BADEN")),
      sino2bool(get2(accidente,"ELEMENTOS_TRAMO","TRAMO_APARTADERO")),
      sino2bool(get2(accidente,"ELEMENTOS_TRAMO","TRAMO_NINGUNA")),
      
      sino2bool(get2(accidente,"CARACTERISTICAS_MARGEN","@INFLU_MARGEN")),
      sino2bool(get2(accidente,"CARACTERISTICAS_MARGEN","MARGEN_DESPEJADO")),
      sino2bool(get2(accidente,"CARACTERISTICAS_MARGEN","MARGEN_ARBOLES")),
      sino2bool(get2(accidente,"CARACTERISTICAS_MARGEN","MARGEN_OTROS_NATURALES")),
      sino2bool(get2(accidente,"CARACTERISTICAS_MARGEN","MARGEN_EDIFICIOS")),
      sino2bool(get2(accidente,"CARACTERISTICAS_MARGEN","MARGEN_POSTES")),
      sino2bool(get2(accidente,"CARACTERISTICAS_MARGEN","MARGEN_PUBLICIDAD")),
      sino2bool(get2(accidente,"CARACTERISTICAS_MARGEN","MARGEN_OTROS_ARTIFICIALES")),
      sino2bool(get2(accidente,"CARACTERISTICAS_MARGEN","MARGEN_OTROS_OBSTACULOS")),
      sino2bool(get2(accidente,"CARACTERISTICAS_MARGEN","MARGEN_DESC")),

      sino2bool(get2(accidente,"CIRCUNSTANCIAS_ESPECIALES_VIA","@INFLU_CIRCUNS_ESP")),
      sino2bool(get2(accidente,"CIRCUNSTANCIAS_ESPECIALES_VIA","CIRCUNS_ESP_NINGUNA")),
      sino2bool(get2(accidente,"CIRCUNSTANCIAS_ESPECIALES_VIA","CIRCUNS_ESP_CONOS")),
      sino2bool(get2(accidente,"CIRCUNSTANCIAS_ESPECIALES_VIA","CIRCUNS_ESP_ZANJA")),
      sino2bool(get2(accidente,"CIRCUNSTANCIAS_ESPECIALES_VIA","CIRCUNS_ESP_TAPA")),
      sino2bool(get2(accidente,"CIRCUNSTANCIAS_ESPECIALES_VIA","CIRCUNS_ESP_OBRAS")),
      sino2bool(get2(accidente,"CIRCUNSTANCIAS_ESPECIALES_VIA","CIRCUNS_ESP_OBSTACULO")),
      sino2bool(get2(accidente,"CIRCUNSTANCIAS_ESPECIALES_VIA","CIRCUNS_ESP_DESPREND")),
      sino2bool(get2(accidente,"CIRCUNSTANCIAS_ESPECIALES_VIA","CIRCUNS_ESP_ESCALON")),
      sino2bool(get2(accidente,"CIRCUNSTANCIAS_ESPECIALES_VIA","CIRCUNS_ESP_FBACHES")),
      sino2bool(get2(accidente,"CIRCUNSTANCIAS_ESPECIALES_VIA","CIRCUNS_ESP_FDETERIORADO")),
      sino2bool(get2(accidente,"CIRCUNSTANCIAS_ESPECIALES_VIA","CIRCUNS_ESP_OTRAS")),
      sino2bool(get2(accidente,"CIRCUNSTANCIAS_ESPECIALES_VIA","CIRCUNS_ESP_DESC")),

      sino2bool(get2(accidente,"DELIMITACION_CALZADA","@INFLU_DELIM_CALZADA")),
      sino2bool(get2(accidente,"DELIMITACION_CALZADA","DELIM_CALZADA_BORDILLO")),
      sino2bool(get2(accidente,"DELIMITACION_CALZADA","DELIM_CALZADA_VALLAS")),
      sino2bool(get2(accidente,"DELIMITACION_CALZADA","DELIM_CALZADA_SETOS")),
      sino2bool(get2(accidente,"DELIMITACION_CALZADA","DELIM_CALZADA_MARCAS")),
      sino2bool(get2(accidente,"DELIMITACION_CALZADA","DELIM_CALZADA_BARRERA")),
      sino2bool(get2(accidente,"DELIMITACION_CALZADA","DELIM_CALZADA_ISLETA")),
      sino2bool(get2(accidente,"DELIMITACION_CALZADA","DELIM_CALZADA_PEATONAL")),
      sino2bool(get2(accidente,"DELIMITACION_CALZADA","DELIM_CALZADA_OTRA")),
      sino2bool(get2(accidente,"DELIMITACION_CALZADA","DELIM_CALZADA_SIN_DELIM")),

      sino2bool(get2(accidente,"FACTORES_CONCURRENTES","FC_CON_DISTRAIDA")),
      sino2bool(get2(accidente,"FACTORES_CONCURRENTES","FC_VEL_INADECUADA")),
      sino2bool(get2(accidente,"FACTORES_CONCURRENTES","FC_PRIORIDAD")),
      sino2bool(get2(accidente,"FACTORES_CONCURRENTES","FC_SEGURIDAD")),
      sino2bool(get2(accidente,"FACTORES_CONCURRENTES","FC_ADELANTAMIENTO")),
      sino2bool(get2(accidente,"FACTORES_CONCURRENTES","FC_GIRO")),
      sino2bool(get2(accidente,"FACTORES_CONCURRENTES","FC_CON_NEGLIGENTE")),
      sino2bool(get2(accidente,"FACTORES_CONCURRENTES","FC_CON_TEMERARIA")),
      sino2bool(get2(accidente,"FACTORES_CONCURRENTES","FC_IRRUPCION_ANIMAL")),
      sino2bool(get2(accidente,"FACTORES_CONCURRENTES","FC_IRRUPCION_PEATON")),
      sino2bool(get2(accidente,"FACTORES_CONCURRENTES","FC_ALCOHOL")),
      sino2bool(get2(accidente,"FACTORES_CONCURRENTES","FC_DROGAS")),
      sino2bool(get2(accidente,"FACTORES_CONCURRENTES","FC_ESTADO_VIA")),
      sino2bool(get2(accidente,"FACTORES_CONCURRENTES","FC_METEORO")),
      sino2bool(get2(accidente,"FACTORES_CONCURRENTES","FC_CANSANCIO")),
      sino2bool(get2(accidente,"FACTORES_CONCURRENTES","FC_INEXPERIENCIA")),
      sino2bool(get2(accidente,"FACTORES_CONCURRENTES","FC_AVERIA")),
      sino2bool(get2(accidente,"FACTORES_CONCURRENTES","FC_OBRAS")),
      sino2bool(get2(accidente,"FACTORES_CONCURRENTES","FC_MAL_ESTADO_VEHI")),
      sino2bool(get2(accidente,"FACTORES_CONCURRENTES","FC_ENFERMEDAD")),
      sino2bool(get2(accidente,"FACTORES_CONCURRENTES","FC_SENYALIZACION")),
      sino2bool(get2(accidente,"FACTORES_CONCURRENTES","FC_OBSTACULO")),
      sino2bool(get2(accidente,"FACTORES_CONCURRENTES","FC_OTRO_FACTOR")),
      None, # VEHICULOS
      None, # Peatones
      None # Croquis
    ]
    return values

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

def generate_translations():
  translations = dict()
  for columdef in COLUMNS_DEFINITION:
    for prop in ("label", "shortlabel", "group"):
      s=columdef.args.get(prop,None)
      if s != None:
        translations[s]=s.strip()
  l = list()
  l.extend(translations.keys())
  l.sort()
  for s in l:
    print "%s=%s" % (s,s.replace("_"," ").strip())
  
def test1():
  print Descriptor("FECHA_ACCIDENTE","Date",label="Accidente")
  print Descriptor("LID_ACCIDENTE","String",20,hidden=True, pk=True)
  print Descriptor("COD_INFORME","String",20,label="Informe")\
          .foreingkey("ARENA2_INFORMES","COD_INFORME","FORMAT('%s',COD_INFORME)")\
          .tag("dynform.readonly",True)
        
  print Descriptor("TIPO_VIA","Integer", label="Tipo de via")\
          .selectablefk("ARENA2_DIC_TIPO_VIA")\
          
  print Descriptor("MAPA", "Geometry", hidden=True, 
        geomtype="Point:2D", 
        SRS="EPSG:4326", 
        expression="TRY ST_SetSRID(ST_Point(MAPAX,MAPAY),4326) EXCEPT NULL"
      )
  
def main(*args):
  test1()
  #generate_translations()
  