# encoding: utf-8

from org.gvsig.tools.swing.api import ToolsSwingLocator
from java.awt.image import BufferedImage
from java.awt import Color
from java.awt.event import ActionListener
from javax.swing.event import DocumentListener
from javax.swing import ImageIcon, DefaultComboBoxModel
import gvsig
from java.awt.event import ActionListener
from javax.swing.event import ChangeListener
from org.gvsig.tools.swing.api import ListElement
from java.text import SimpleDateFormat
from org.gvsig.expressionevaluator import ExpressionEvaluatorLocator
from org.gvsig.expressionevaluator import ExpressionBuilder
from org.gvsig.expressionevaluator.ExpressionBuilder import FUNCTION_DATE
from javax.swing.text import DefaultFormatterFactory, DateFormatter
from java.text import DateFormat
from java.util import Locale
from org.gvsig.tools.swing.api import ListElement
from javax.json import Json
from org.gvsig.tools.dataTypes import DataTypeUtils

class TabControllerFecha(ChangeListener, ActionListener):
  TAB_INDEX_PANEL = 2
  def __init__(self, store, tabPanel, txtFechaDesde, btnFechaDesde, txtFechaHasta, btnFechaHasta, cboTipoAccidente):
    self.store = store
    self.tabPanel = tabPanel
    self.fechaDesde = txtFechaDesde
    self.fechaDesdeBtn = btnFechaDesde
    self.fechaHasta = txtFechaHasta
    self.fechaHastaBtn = btnFechaHasta
    self.tipoAccidente = cboTipoAccidente
    self.initComponents()
    
  def initComponents(self):
    self.pickerFechaDesde = ToolsSwingLocator.getToolsSwingManager().createDatePickerController(self.fechaDesde, self.fechaDesdeBtn)
    self.pickerFechaHasta = ToolsSwingLocator.getToolsSwingManager().createDatePickerController(self.fechaHasta, self.fechaHastaBtn)
    
    
    tipoAccidenteModel = DefaultComboBoxModel()
    attr = self.store.getDefaultFeatureType().get("TIPO_ACC_COLISION")
    values = attr.getAvailableValues()
    tipoAccidenteModel.addElement(ListElement(u' ',u''))
    for value in values:
      element = ListElement(value.getLabel(), value.getValue())
      tipoAccidenteModel.addElement(element)
    self.tipoAccidente.setModel(tipoAccidenteModel)

    self.tipoAccidente.addActionListener(self)
    self.pickerFechaDesde.addChangeListener(self)
    self.pickerFechaHasta.addChangeListener(self)
    
    self.pickerFechaDesde.setEnabled(True)
    self.pickerFechaHasta.setEnabled(True)
    
  def toJson(self):
      tipoAccidente = self.tipoAccidente.getSelectedItem().getValue()
      dateDesde = self.pickerFechaDesde.get()
      if dateDesde != None:
          dateDesde = DataTypeUtils.toString(dateDesde, None)
      
      dateHasta = self.pickerFechaHasta.get()
      if dateHasta!=None:
          dateHasta = DataTypeUtils.toString(dateHasta, None)
      
      builder = Json.createObjectBuilder();
      if tipoAccidente!=None and not tipoAccidente=="": builder.add("tipoAccidente", tipoAccidente)
      
      if dateDesde != None: builder.add("dateDesde", dateDesde)
      if dateHasta != None: builder.add("dateHasta", dateHasta)
      finalJson = builder.build()
      return finalJson
  
  def fromJson(self, json):
      if (json==None):
          return
      tipoAccidenteValue = json.getInt("tipoAccidente") if json.containsKey("tipoAccidente") else None
      if json.containsKey("dateDesde"):
          dateDesdeValue = json.getString("dateDesde")  
      else:
          dateDesdeValue = None
      if json.containsKey("dateHasta"):    
          dateHastaValue = json.getString("dateHasta")  
      else:
        dateHastaValue= None
      self.setValues(tipoAccidenteValue, dateDesdeValue, dateHastaValue)
      
  def setValues(self, tipoAccidenteValue, dateDesdeValue, dateHastaValue):
      if tipoAccidenteValue!=None: ListElement.setSelected(self.tipoAccidente, tipoAccidenteValue)
      if dateDesdeValue!=None: 
          d = DataTypeUtils.toDate(dateDesdeValue)
          self.pickerFechaDesde.set(d)
      if dateHastaValue!=None: 
          d = DataTypeUtils.toDate(dateHastaValue)
          self.pickerFechaHasta.set(DataTypeUtils.toDate(d))
           
  def clear(self):
    self.tipoAccidente.setSelectedIndex(0)
    self.pickerFechaDesde.set(None)
    self.pickerFechaHasta.set(None)
  
  def checkModify(self):
    iconTheme = ToolsSwingLocator.getIconThemeManager().getDefault()
    if(self.pickerFechaDesde.isEmpty() and
      self.pickerFechaHasta.isEmpty() and
      self.tipoAccidente.getSelectedItem().getValue()==''):
        icon = iconTheme.get("accidentcondition-tabtick-disabled")
        self.tabPanel.setIconAt(self.TAB_INDEX_PANEL, icon)
        return False
    else:
        icon = iconTheme.get("accidentcondition-tabtick-enabled")
        self.tabPanel.setIconAt(self.TAB_INDEX_PANEL, icon)
        return True
  def stateChanged(self, e):
    self.checkModify()
  def actionPerformed(self, e):
    self.checkModify()

  def getFilter(self):
    if (self.checkModify()==False):
      return None
    tipoAccidente = self.tipoAccidente.getSelectedItem().getValue()
    dateDesde = self.pickerFechaDesde.get()
    dateHasta = self.pickerFechaHasta.get()
    
    expManager= ExpressionEvaluatorLocator.getManager()
    exp = expManager.createExpression()
    builder = expManager.createExpressionBuilder()

    if (tipoAccidente!=""):
      builder.and(builder.eq(
        builder.variable("TIPO_ACC_COLISION"), 
        builder.constant(tipoAccidente)
        )
      )

    if (dateDesde!=None and dateHasta != None):
      builder.and(
        builder.and(
          builder.ge(
            builder.variable("FECHA_ACCIDENTE"),
            builder.date(dateDesde)
          ),
          builder.le(
            builder.variable("FECHA_ACCIDENTE"), 
            builder.date(dateHasta) #builder.function(FUNCTION_DATE,dateFormat.format(dateHasta), dateFormat)
          )
        )
      )
    elif (dateDesde!=None):
      builder.and(builder.ge(
            builder.variable("FECHA_ACCIDENTE"), 
            builder.date(dateDesde)
          ))
    elif (dateHasta!=None):
      builder.and(builder.le(
              builder.variable("FECHA_ACCIDENTE"), 
              builder.date(dateHasta)
            ))
    return builder.value()
def main(*args):

    #Remove this lines and add here your code

    print "hola mundo"
    pass
