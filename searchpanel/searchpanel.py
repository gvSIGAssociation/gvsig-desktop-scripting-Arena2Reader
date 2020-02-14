# encoding: utf-8

import gvsig
from org.gvsig.fmap.dal.swing import DALSwingLocator
#from org.gvsig.fmap.dal.swing.searchpanel import SearchConditionPanelFactory
from gvsig.libs.formpanel import FormPanel
from gvsig import getResource
from org.gvsig.fmap.dal.swing.searchpanel import SearchConditionPanel
from org.gvsig.tools import ToolsLocator
from java.io import File
from org.gvsig.tools.swing.api import ToolsSwingLocator
from org.gvsig.expressionevaluator import ExpressionEvaluatorLocator
from java.awt.image import BufferedImage
from java.awt import Color
from javax.swing import ImageIcon, DefaultComboBoxModel
from org.gvsig.tools.swing.api import ListElement
from java.awt.event import ActionListener
from javax.swing.event import DocumentListener
from javax.swing.event import ChangeListener
from org.gvsig.tools.swing.api import ToolsSwingLocator

from controller.controllerCarretera import TabControllerCarretera
from controller.controllerFecha import TabControllerFecha

from controller.controllerVictimas import TabControllerVictimas

def createIcon(color):
  width = 16
  height = 16
  type = BufferedImage.TYPE_INT_ARGB
  image = BufferedImage(width, height, type)
  g2d = image.createGraphics()
  g2d.setColor(color)
  g2d.fillRect(0, 0, width, height)
  g2d.dispose()
  icon = ImageIcon(image)
  return icon

class SearchConditionPanelAccidente(FormPanel, SearchConditionPanel):
  def __init__(self, store):
    FormPanel.__init__(self,getResource(__file__,"SearchConditionPanelAccidente.xml"))
    self.store = store
    i18n = ToolsLocator.getI18nManager()
    self.initComponents()

  def initComponents(self):
    iconTheme = ToolsSwingLocator.getIconThemeManager().getDefault()
    icon = iconTheme.get("accidentcondition-tabtick-disabled")
    self.tabPanel.setIconAt(0, icon)
    self.tabPanel.setIconAt(1, icon)
    self.tabPanel.setIconAt(2, icon)
    self.tabPanel.setIconAt(3, icon)

    icon1 = iconTheme.get("search-simplifiedcondition-add-accumulate")
    icon2 = iconTheme.get("search-simplifiedcondition-clear-accumulate")
    icon3 = iconTheme.get("search-simplifiedcondition-edit-accumulate")
    
    self.btnClearAccumulate.setIcon(icon2)
    self.btnEditAccumulate.setIcon(icon3)
    self.btnAddAccumulate.setIcon(icon1)
    
    self.tabControllerCarretera = TabControllerCarretera(
        self.tabPanel,
        self.cboProvincia,
        self.txtCarretera,
        self.txtPkInicio,
        self.txtPkInicioUmbral,
        self.txtPkFin,
        self.txtPkFinUmbral,
        self.cboSentido)

    self.tabControllerFecha = TabControllerFecha(
      self.store,
      self.tabPanel,
      self.txtFechaDesde,
      self.btnFechaDesde,
      self.txtFechaHasta,
      self.btnFechaHasta,
      self.cboTipoAccidente)

    self.tabControllerVictimas = TabControllerVictimas( 
      self.store,
      self.tabPanel,
      self.cboCategoria,
      self.chkPeligrosas,
      self.cboMortalesOperador,
      self.txtMortales,
      self.cboOperator1,
      self.cboGravesOperador,
      self.txtGraves,
      self.cboOperator2,
      self.cboLevesOperador,
      self.txtLeves)
      
    
      
    sentidoModel = DefaultComboBoxModel()
    attr = self.store.getDefaultFeatureType().get("SENTIDO")
    values = attr.getAvailableValues()
    sentidoModel.addElement(ListElement(u' ',u''))
    for value in values:
      element = ListElement(value.getLabel(), value.getValue())
      sentidoModel.addElement(element)
    self.cboSentido.setModel(sentidoModel)
    
    provinciaModel = DefaultComboBoxModel()
    addAllProvinciaToModel(provinciaModel)
    self.cboProvincia.setModel(provinciaModel)

    
    
  def clear(self):
    self.txtCodAccidente.setText("")
    self.tabControllerCarretera.clear()
    self.tabControllerFecha.clear()
    self.tabControllerVictimas.clear()
    return None

  def get(self):
    #Accidente
    codAccidente = self.txtCodAccidente.getText()
    exp = self.createExpression(
                  codAccidente
                  )
    return exp

  def createExpression(self, codAccidente):
    expManager= ExpressionEvaluatorLocator.getManager()
    exp = expManager.createExpression()
    builder = expManager.createExpressionBuilder()
    #Codigo
    if (codAccidente!=""):
      builder.set(
        builder.like(
            builder.variable("ID_ACCIDENTE"), 
            builder.constant(codAccidente)
          )
      )
    # Carretera
    carreteraValue = self.tabControllerCarretera.getFilter()
    if (carreteraValue!=None):
      builder.and(carreteraValue)

    # Fecha y tipo
    fechaValue = self.tabControllerFecha.getFilter()
    if (fechaValue!=None):
      builder.and(fechaValue)
    # Victimas
    victimasValue = self.tabControllerVictimas.getFilter()
    if (victimasValue!=None):
      print "Builder victimas:", victimasValue
      builder.and(victimasValue)
    
    try:
      print "Final: ", builder
      print "Final builder:", builder.toString()
      exp.setPhrase(builder.toString())
    except:
      exp.setPhrase("")
    print "Expresion final del Accidentes panel:", exp
    return exp
    
  def set(self, fil):
    pass

  def setEnabled(self, enabled):
    pass
  
  def getFactory(self):
    return SearchArena2Factory()

  def btnAddAccumulate_click(self, *args):
    exp = self.get()
    self.addToAccumulatedFilter(exp)
    pass
  def btnEditAccumulate_click(self, *args):
    pass
  def btnClearAccumulate_click(self, *args):
    self.clearAccumulatedFilter()
    pass
    
  def txtCodAccidente_change(self, *args):
    print "txtcod:", self.txtCodAccidente.getText()
    iconTheme = ToolsSwingLocator.getIconThemeManager().getCurrent()
    if self.txtCodAccidente.getText()=="":
      print "null"
      icon = iconTheme.get("accidentcondition-tabtick-disabled")
      #icon = createIcon(Color.RED)
      print icon, type(icon)
      self.tabPanel.setIconAt(0, icon)
    else:
      icon = iconTheme.get("accidentcondition-tabtick-enabled")
      #icon = createIcon(Color.GREEN)
      self.tabPanel.setIconAt(0, icon)
    
    
class SearchArena2Factory(SearchConditionPanel.SearchConditionPanelFactory):
  def isApplicable(self, store):
    if "ARENA2_ACCIDENTES" in str(store.getName()):
      return True
    return False
  def create(self, os): #SearchConditionPanel
    try:
      store = os[0].getStore()
    except:
      print "store is none"
      store = None
    return SearchConditionPanelAccidente(store)
  def getName(self):
    return "Accidentes"

def selfRegister():
  iconTheme = ToolsSwingLocator.getIconThemeManager().getDefault()
  icon1 = File(getResource(__file__,"imagenes","accidentcondition-tabtick-enabled.png")).toURI().toURL()
  icon2 = File(getResource(__file__,"imagenes","accidentcondition-tabtick-disabled.png")).toURI().toURL()
  icon3 = File(getResource(__file__,"imagenes","search-simplifiedcondition-add-accumulate.png")).toURI().toURL()
  icon4 = File(getResource(__file__,"imagenes","search-simplifiedcondition-clear-accumulate.png")).toURI().toURL()
  icon5 = File(getResource(__file__,"imagenes","search-simplifiedcondition-edit-accumulate.png")).toURI().toURL()
  
  iconTheme.registerDefault("scripting.arena2reader", "action", "accidentcondition-tabtick-enabled", None, icon1)
  iconTheme.registerDefault("scripting.arena2reader", "action", "accidentcondition-tabtick-disabled", None, icon2)
  iconTheme.registerDefault("scripting.arena2reader", "action", "search-simplifiedcondition-add-accumulate", None, icon3)
  iconTheme.registerDefault("scripting.arena2reader", "action", "search-simplifiedcondition-clear-accumulate", None, icon4)
  iconTheme.registerDefault("scripting.arena2reader", "action", "search-simplifiedcondition-edit-accumulate", None, icon5)
  
def addAllProvinciaToModel(provinciaModel):
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
    selfRegister()
    manager = DALSwingLocator.getDataSwingManager();
    factory = SearchArena2Factory()
    panel = factory.create([gvsig.currentDocument().getFeatureStore()])
    panel.showTool("SearchConditionPanelAccidente")
    manager.registerSearchConditionPanel(factory) #SearchConditionPanelFactory
