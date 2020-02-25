# encoding: utf-8
from org.gvsig.tools.swing.api import ToolsSwingLocator
from java.awt.image import BufferedImage
from java.awt import Color
from java.awt.event import ActionListener
from javax.swing.event import DocumentListener
from javax.swing import ImageIcon, DefaultComboBoxModel
from org.gvsig.expressionevaluator import ExpressionEvaluatorLocator
from javax.swing import ImageIcon, DefaultComboBoxModel
from org.gvsig.tools.swing.api import ListElement
import gvsig
  
class TabControllerCarretera(ActionListener, DocumentListener):
  TAB_INDEX_PANEL = 1
  def __init__(self, store, tabPanel, provincia, titularidad, carretera, pki,pkiu, pkf, pkfu, sentido):
    self.store = store
    self.tabPanel = tabPanel
    self.provincia = provincia
    self.titularidad = titularidad
    self.carretera = carretera
    self.pki = pki
    self.pkiu = pkiu
    self.pkf = pkf
    self.pkfu = pkfu
    self.sentido = sentido
    self.initComponents()
    #default values
    self.titularidad.setSelectedIndex(2)
    
  def initComponents(self):
    self.provincia.addActionListener(self)
    self.titularidad.addActionListener(self)
    self.carretera.getDocument().addDocumentListener(self)
    self.pki.getDocument().addDocumentListener(self)
    self.pkiu.getDocument().addDocumentListener(self)
    self.pkf.getDocument().addDocumentListener(self)
    self.pkfu.getDocument().addDocumentListener(self)
    self.sentido.addActionListener(self)

      
    sentidoModel = DefaultComboBoxModel()
    attr = self.store.getDefaultFeatureType().get("SENTIDO")
    values = attr.getAvailableValues()
    sentidoModel.addElement(ListElement(u' ',u''))
    for value in values:
      element = ListElement(value.getLabel(), value.getValue())
      sentidoModel.addElement(element)
    self.sentido.setModel(sentidoModel)
    
    provinciaModel = DefaultComboBoxModel()
    self.addAllProvinciaToModel(provinciaModel)
    self.provincia.setModel(provinciaModel)

    titularidadModel = DefaultComboBoxModel()
    attr = self.store.getDefaultFeatureType().get("TITULARIDAD_VIA")
    values = attr.getAvailableValues()
    titularidadModel.addElement(ListElement(u' ',u''))
    for value in values:
      element = ListElement(value.getLabel(), value.getValue())
      titularidadModel.addElement(element)
    self.titularidad.setModel(titularidadModel)

    
  def clear(self):
    self.provincia.setSelectedIndex(0)
    self.titularidad.setSelectedIndex(0)
    self.carretera.setText("")
    self.pki.setText("")
    self.pkiu.setText("")
    self.pkf.setText("")
    self.pkfu.setText("")
    self.sentido.setSelectedIndex(0)
    
  def checkModify(self):
    iconTheme = ToolsSwingLocator.getIconThemeManager().getDefault()
    if (self.provincia.getSelectedItem().getValue()=="" and
        self.titularidad.getSelectedItem().getValue()=="" and
        self.carretera.getText()=="" and
        self.pki.getText()=="" and
        self.pkiu.getText()=="" and
        self.pkf.getText()=="" and
        self.pkfu.getText()=="" and
        self.sentido.getSelectedItem().getValue()==""):
          icon = iconTheme.get("accidentcondition-tabtick-disabled")
          self.tabPanel.setIconAt(self.TAB_INDEX_PANEL, icon)
          return False
    else:
      icon = iconTheme.get("accidentcondition-tabtick-enabled")
      self.tabPanel.setIconAt(self.TAB_INDEX_PANEL, icon)
      return True
      
  def actionPerformed(self, e):
    self.checkModify()
  def insertUpdate(self, e):
    self.checkModify()
  def removeUpdate(self, e):
    self.checkModify()
  def changedUpdate(self, e):
    self.checkModify()
  def getFilter(self): #getFilter
    if (self.checkModify()==False):
      return None
    provincia = self.provincia.getSelectedItem().getValue()
    titularidad = self.titularidad.getSelectedItem().getValue()
    carretera = self.carretera.getText()
    pkInicio = self.pki.getText()
    pkInicioUmbral = self.pkiu.getText()
    pkFin = self.pkf.getText()
    pkFinUmbral = self.pkfu.getText()
    sentido = self.sentido.getSelectedItem().getValue()
    
    expManager= ExpressionEvaluatorLocator.getManager()
    exp = expManager.createExpression()
    builder = expManager.createExpressionBuilder()

    if (provincia!=""):
      builder.and(builder.eq(
        builder.variable("COD_PROVINCIA"), 
        builder.constant(provincia)
        )
      )
    if (titularidad!=""):
      builder.and(builder.eq(
        builder.variable("TITULARIDAD_VIA"), 
        builder.constant(titularidad)
        )
      )
      
    if (carretera!=""):
      builder.and(builder.eq(
        builder.variable("CARRETERA"), 
        builder.constant(carretera)
        )
      )
    if pkInicio!="":
      pkInicioTotal = float(pkInicio)
      if pkInicioUmbral!="":
        pkInicioTotal += float("0."+pkInicioUmbral)
    
    if pkFin!="":
      pkFinTotal = float(pkFin)
      if pkFinUmbral!="":
        pkFinTotal += float("0."+pkFinUmbral)
    
    if pkInicio != "" and pkFin != "":
      builder.and(
        builder.and(
          builder.ge(
            builder.variable("KM"), 
            builder.constant(pkInicioTotal)
          ),
          builder.le(
            builder.variable("KM"), 
            builder.constant(pkFinTotal)
          )
        )
      )
    elif pkInicio != "":
      builder.and(
          builder.ge(
            builder.variable("KM"), 
            builder.constant(pkInicioTotal)
          )
        )
    elif pkFin != "":
      builder.and(
          builder.le(
            builder.variable("KM"), 
            builder.constant(pkFinTotal)
          )
        )
    if (sentido!=""):
      builder.and(builder.eq(
        builder.variable("SENTIDO"), 
        builder.constant(sentido)
        )
      )
    return builder.value()
  
  def addAllProvinciaToModel(self, provinciaModel):
      provinciaModel.addElement(ListElement(u' ',u''))
      provinciaModel.addElement(ListElement(u'A Coruña',u'A Coruña'))
      provinciaModel.addElement(ListElement(u'Álava',u'Álava'))
      provinciaModel.addElement(ListElement(u'Albacete',u'Albacete'))
      provinciaModel.addElement(ListElement(u'Alicante',u'Alicante/Alacant'))
      provinciaModel.addElement(ListElement(u'Almería',u'Almería'))
      provinciaModel.addElement(ListElement(u'Asturias',u'Asturias'))
      provinciaModel.addElement(ListElement(u'Ávila',u'Ávila'))
      provinciaModel.addElement(ListElement(u'Badajoz',u'Badajoz'))
      provinciaModel.addElement(ListElement(u'Baleares',u'Baleares'))
      provinciaModel.addElement(ListElement(u'Barcelona',u'Barcelona'))
      provinciaModel.addElement(ListElement(u'Burgos',u'Burgos'))
      provinciaModel.addElement(ListElement(u'Cáceres',u'Cáceres'))
      provinciaModel.addElement(ListElement(u'Cádiz',u'Cádiz'))
      provinciaModel.addElement(ListElement(u'Cantabria',u'Cantabria'))
      provinciaModel.addElement(ListElement(u'Castellón',u'Castellón/Castello'))
      provinciaModel.addElement(ListElement(u'Ceuta',u'Ceuta'))
      provinciaModel.addElement(ListElement(u'Ciudad Real',u'Ciudad Real'))
      provinciaModel.addElement(ListElement(u'Córdoba',u'Córdoba'))
      provinciaModel.addElement(ListElement(u'Cuenca',u'Cuenca'))
      provinciaModel.addElement(ListElement(u'Girona',u'Girona'))
      provinciaModel.addElement(ListElement(u'Granada',u'Granada'))
      provinciaModel.addElement(ListElement(u'Guadalajara',u'Guadalajara'))
      provinciaModel.addElement(ListElement(u'Gipuzkoa',u'Gipuzkoa'))
      provinciaModel.addElement(ListElement(u'Huelva',u'Huelva'))
      provinciaModel.addElement(ListElement(u'Huesca',u'Huesca'))
      provinciaModel.addElement(ListElement(u'Jaén',u'Jaén'))
      provinciaModel.addElement(ListElement(u'La Rioja',u'La Rioja'))
      provinciaModel.addElement(ListElement(u'Las Palmas',u'Las Palmas'))
      provinciaModel.addElement(ListElement(u'León',u'León'))
      provinciaModel.addElement(ListElement(u'Lérida',u'Lérida'))
      provinciaModel.addElement(ListElement(u'Lugo',u'Lugo'))
      provinciaModel.addElement(ListElement(u'Madrid',u'Madrid'))
      provinciaModel.addElement(ListElement(u'Málaga',u'Málaga'))
      provinciaModel.addElement(ListElement(u'Melilla',u'Melilla'))
      provinciaModel.addElement(ListElement(u'Murcia',u'Murcia'))
      provinciaModel.addElement(ListElement(u'Navarra',u'Navarra'))
      provinciaModel.addElement(ListElement(u'Ourense',u'Ourense'))
      provinciaModel.addElement(ListElement(u'Palencia',u'Palencia'))
      provinciaModel.addElement(ListElement(u'Pontevedra',u'Pontevedra'))
      provinciaModel.addElement(ListElement(u'Salamanca',u'Salamanca'))
      provinciaModel.addElement(ListElement(u'Segovia',u'Segovia'))
      provinciaModel.addElement(ListElement(u'Sevilla',u'Sevilla'))
      provinciaModel.addElement(ListElement(u'Soria',u'Soria'))
      provinciaModel.addElement(ListElement(u'Tarragona',u'Tarragona'))
      provinciaModel.addElement(ListElement(u'Santa Cruz de Tenerife',u'Santa Cruz de Tenerife'))
      provinciaModel.addElement(ListElement(u'Teruel',u'Teruel'))
      provinciaModel.addElement(ListElement(u'Toledo',u'Toledo'))
      provinciaModel.addElement(ListElement(u'Valencia',u'Valencia/Valencia'))
      provinciaModel.addElement(ListElement(u'Valladolid',u'Valladolid'))
      provinciaModel.addElement(ListElement(u'Vizcaya',u'Vizcaya'))
      provinciaModel.addElement(ListElement(u'Zamora',u'Zamora'))
      provinciaModel.addElement(ListElement(u'Zaragoza',u'Zaragoza'))
def main(*args):

    #Remove this lines and add here your code

    print "hola mundo"
    pass
