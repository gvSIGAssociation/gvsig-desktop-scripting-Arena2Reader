# encoding: utf-8

import gvsig
from org.gvsig.fmap.dal.swing import DALSwingLocator
from gvsig.libs.formpanel import FormPanel
from gvsig import getResource
from org.gvsig.fmap.dal.swing.searchpanel import SearchConditionPanel, AbstractSearchConditionPanel
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
from org.gvsig.expressionevaluator import ExpressionUtils
from javax.json import Json
from controller.controllerCarretera import TabControllerCarretera
from controller.controllerFecha import TabControllerFecha
from controller.controllerVictimas import TabControllerVictimas

class SearchConditionPanelAccident(AbstractSearchConditionPanel):
  PANEL_NAME = "SearchConditionPanelAccident"
  def __init__(self, factory, searchPanel, store, simplifiedPanel):
    SearchConditionPanel.__init__(self)
    self.__factory = factory
    self.__searchPanel = searchPanel
    self.__form = SearchConditionPanelAccidentForm( store, simplifiedPanel)

  def getFactory(self):
    return self.__factory
    
  def setEnabled(self, enabled):
    self.__form.setEnabled(enabled)

  def clear(self):
    self.__form.clear()
    
  def asJComponent(self):
    return self.__form.asJComponent()
    
  def get(self):
    return self.__form.get()
    
  def addChangeListener(self, listener):
    pass
   
  def getChangeListeners(self):
    pass
    
  def removeChangeListener(self, listener):
    pass
    
  def removeAllChangeListener(self):
    pass
    
  def hasChangeListeners(self):
    pass

  def isValid(self, messagebuilder):
    return True

  def put(self, params): #SearchParameters
    values = params.getValues()
    jsonState = values.get(self.PANEL_NAME)
    self.__form.fromJson(jsonState)
    pass

  def fetch(self, params):
    jsonState = self.__form.toJson()
    persistenceJson = params.getValues()
    persistenceJson.put(self.PANEL_NAME, jsonState)
    return params

  def getWarnings(self):
    return None
    
class SearchConditionPanelAccidentForm(FormPanel): 
  def __init__(self, store, simplifiedPanel):
    FormPanel.__init__(self,getResource(__file__,"SearchConditionPanelAccidente.xml"))
    self.store = store
    self.simplifiedPanel = simplifiedPanel
    i18n = ToolsLocator.getI18nManager()
    self.initComponents()
    
  def initComponents(self):

    swingManager = ToolsSwingLocator.getToolsSwingManager()
    swingManager.translate(self.tabPanel)
    swingManager.translate(self.btnClearAccumulate)
    swingManager.translate(self.btnEditAccumulate)
    swingManager.translate(self.btnAddAccumulate)
    swingManager.translate(self.lblCodAccidente)
    swingManager.translate(self.lblPuede_utilizar_porcentage_como_comodin)
    swingManager.translate(self.lblProvincia)
    swingManager.translate(self.lblTitularidad)
    swingManager.translate(self.lblCarretera)
    swingManager.translate(self.lblPkInicio)
    swingManager.translate(self.lblPkFin)
    swingManager.translate(self.lblSentido)
    swingManager.translate(self.lblFechaDesde)
    swingManager.translate(self.lblFechaHasta)
    swingManager.translate(self.lblTipoAccidente)
    swingManager.translate(self.lblCategoria)
    swingManager.translate(self.lblMortales)
    swingManager.translate(self.lblGraves)
    swingManager.translate(self.lblLeves)

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
        self.store,
        self.tabPanel,
        self.cboProvincia,
        self.cboTitularidad,
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
      
  def toJson(self):
    builder = Json.createObjectBuilder()

    codAccidente = self.txtCodAccidente.getText()
    if codAccidente!=None: builder.add("codAccidente", codAccidente)
      
    tabCarretera = self.tabControllerCarretera.toJson()
    if tabCarretera!=None: builder.add("tabCarretera", tabCarretera)
    
    tabFecha = self.tabControllerFecha.toJson()
    if tabFecha != None: builder.add("tabFecha", tabFecha)
    
    tabVictimas = self.tabControllerVictimas.toJson()
    if tabVictimas != None: builder.add("tabVictimas", tabVictimas)
      
    return builder.build()
    
    
  def fromJson(self, jsonObject):
      self.clear()
      if (jsonObject==None): return 
      
      if (jsonObject.containsKey("codAccidente")): 
          codAccidente = jsonObject.getString("codAccidente")
          self.txtCodAccidente.setText(codAccidente)

      if (jsonObject.containsKey("tabCarretera")): 
          jsonCarretera = jsonObject.getJsonObject("tabCarretera")
          self.tabControllerCarretera.fromJson(jsonCarretera)

      if (jsonObject.containsKey("tabFecha")):
          jsonFecha = jsonObject.getJsonObject("tabFecha")
          self.tabControllerFecha.fromJson(jsonFecha)

      if (jsonObject.containsKey("tabVictimas")):
          jsonVictimas = jsonObject.getJsonObject("tabVictimas")
          self.tabControllerVictimas.fromJson(jsonVictimas)
      
  def clear(self):
    self.txtCodAccidente.setText("")
    self.tabControllerCarretera.clear()
    self.tabControllerFecha.clear()
    self.tabControllerVictimas.clear()
    return None

  def get(self):
    exp = self.createExpression()
    return exp

  def createExpression(self):
    expManager= ExpressionEvaluatorLocator.getManager()
    exp = expManager.createExpression()
    builder = expManager.createExpressionBuilder()
    # Accidente
    codAccidente = self.txtCodAccidente.getText()
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
      builder.and(victimasValue)

    # Acumulada
    accumulatedFilter = self.simplifiedPanel.getAccumulatedFilter()
    if(accumulatedFilter!=None):
      builder.and(builder.toValue(accumulatedFilter))
    try:
      exp.setPhrase(builder.toString())
    except:
      exp.setPhrase("")
    return exp

  def set(self, fil):
    self.clear()

  def setEnabled(self, enabled):
    pass
  
  def btnAddAccumulate_click(self, *args):
    exp = self.get()
    self.simplifiedPanel.addToAccumulatedFilter(exp.getPhrase())
    
  def btnEditAccumulate_click(self, *args):
    self.simplifiedPanel.showAccumulatedFilter()
    
  def btnClearAccumulate_click(self, *args):
    self.simplifiedPanel.clearAccumulatedFilter()
    pass
  
  def txtCodAccidente_change(self, *args):
    iconTheme = ToolsSwingLocator.getIconThemeManager().getCurrent()
    if self.txtCodAccidente.getText()=="":
      icon = iconTheme.get("accidentcondition-tabtick-disabled")
      self.tabPanel.setIconAt(0, icon)
    else:
      icon = iconTheme.get("accidentcondition-tabtick-enabled")
      self.tabPanel.setIconAt(0, icon)
  
      
class SearchArena2Factory(SearchConditionPanel.SearchConditionPanelFactory):
  def __init__(self):
    pass

  def getName(self):
    return "Accidentes"

  def isApplicable(self, store):
    if "ARENA2_ACCIDENTES" in str(store.getName()):
      return True
    return False
    
  def create(self, os): #SearchConditionPanel
    try:
      searchPanel = os[0]
      store = searchPanel.getStore()
      simplifiedPanel = searchPanel.getConditionPanel("Simplified")
    except:
      print "store is none"
      store = None
      simplifiedPanel = None
    return SearchConditionPanelAccident(self, searchPanel, store, simplifiedPanel)
    
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

def main(*args):
    selfRegister()
    manager = DALSwingLocator.getDataSwingManager();
    factory = SearchArena2Factory()
    #panel = SearchConditionPanelAccidenteBase(gvsig.currentDocument().getFeatureStore(), None) #factory.create([gvsig.currentDocument().getFeatureStore()])
    #panel.showTool("SearchConditionPanelAccidente")
    #print dir(panel)
    manager.registerSearchConditionPanel(factory) #SearchConditionPanelFactory
    
