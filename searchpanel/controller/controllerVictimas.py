# encoding: utf-8

from org.gvsig.tools.swing.api import ToolsSwingLocator
from java.awt.image import BufferedImage
from java.awt import Color
from java.awt.event import ActionListener
from javax.swing.event import DocumentListener
from javax.swing import ImageIcon, DefaultComboBoxModel
from org.gvsig.tools.swing.api import ListElement
import gvsig
from org.gvsig.expressionevaluator import ExpressionEvaluatorLocator
from org.gvsig.expressionevaluator import ExpressionBuilder
class TabControllerVictimas(DocumentListener, ActionListener):
  TAB_INDEX_PANEL = 3
  CATEGORIA_CON_VICTIMAS = 0
  CATEGORIA_CON_DANOS = 1

  
  def __init__(self, store, tabPanel, cboCategoria, chkPeligrosas, cboMortalesOperador, txtMortales,cboOperator1,cboGravesOperador,txtGraves,cboOperator2, cboLevesOperador, txtLeves):
    self.store = store
    self.tabPanel = tabPanel
    self.categoria = cboCategoria
    self.peligrosas = chkPeligrosas
    self.mortalesOperador = cboMortalesOperador
    self.mortales = txtMortales
    self.operator1 = cboOperator1
    self.gravesOperador = cboGravesOperador
    self.graves = txtGraves
    self.operator2 = cboOperator2
    self.levesOperador = cboLevesOperador
    self.leves = txtLeves
    self.initComponents()
  def initComponents(self):
    listCategoriaElements = [
      ListElement(u' ',u''), 
      ListElement(u'Con victimas',self.CATEGORIA_CON_VICTIMAS),
      ListElement(u'Con daños',self.CATEGORIA_CON_DANOS)
      ]
    self.categoria.setModel(DefaultComboBoxModel(listCategoriaElements))
    
    listOperatorElements = [
        ListElement(u'_And',ExpressionBuilder.OPERATOR_AND),
        ListElement(u'_Or',ExpressionBuilder.OPERATOR_OR)
        ]
    self.operator1.setModel(DefaultComboBoxModel(listOperatorElements))
    self.operator2.setModel(DefaultComboBoxModel(listOperatorElements))
    
    
    listOperatorFildElements = [
        ListElement(u'=',ExpressionBuilder.OPERATOR_EQ),
        ListElement(u'<>',ExpressionBuilder.OPERATOR_NE),
        ListElement(u'>',ExpressionBuilder.OPERATOR_GT),
        ListElement(u'>=',ExpressionBuilder.OPERATOR_GE),
        ListElement(u'<',ExpressionBuilder.OPERATOR_LT),
        ListElement(u'<=',ExpressionBuilder.OPERATOR_LE)
        ]
    self.mortalesOperador.setModel(DefaultComboBoxModel(listOperatorFildElements))
    self.gravesOperador.setModel(DefaultComboBoxModel(listOperatorFildElements))
    self.levesOperador.setModel(DefaultComboBoxModel(listOperatorFildElements))
    
    self.categoria.addActionListener(self)
    self.mortalesOperador.addActionListener(self)
    self.operator1.addActionListener(self)
    self.gravesOperador.addActionListener(self)
    self.operator2.addActionListener(self)
    self.levesOperador.addActionListener(self)
    self.mortales.getDocument().addDocumentListener(self)
    self.graves.getDocument().addDocumentListener(self)
    self.leves.getDocument().addDocumentListener(self)
    
  def clear(self):
    self.categoria.setSelectedIndex(0)
    self.mortalesOperador.setSelectedIndex(0)
    self.operator1.setSelectedIndex(0)
    self.gravesOperador.setSelectedIndex(0)
    self.operator2.setSelectedIndex(0)
    self.levesOperador.setSelectedIndex(0)
    self.mortales.setText("")
    self.graves.setText("")
    self.leves.setText("")
    
  def actionPerformed(self, e):
    self.checkModify()
  def insertUpdate(self, e):
    self.checkModify()
  def removeUpdate(self, e):
    self.checkModify()
  def changedUpdate(self, e):
    self.checkModify()
  def getFilter(self):
    print "controller victimas"
    if (self.checkModify()==False):
      return None
    expManager= ExpressionEvaluatorLocator.getManager()
    exp = expManager.createExpression()
    builder = expManager.createExpressionBuilder()
    
    categoria = self.categoria.getSelectedItem().getValue()
    peligrosas = self.peligrosas.isSelected()
    mortalesOperador = self.mortalesOperador.getSelectedItem().getValue()
    operator1 =           self.operator1.getSelectedItem().getValue()
    gravesOperador = self.gravesOperador.getSelectedItem().getValue()
    operator2 = self.operator2.getSelectedItem().getValue()
    levesOperador = self.levesOperador.getSelectedItem().getValue()
    print "Victimas values:", categoria, mortalesOperador,operator1,gravesOperador, operator2, levesOperador
    
    mortales = self.mortales.getText()
    graves = self.graves.getText()
    leves = self.leves.getText()
    
    if (categoria!=""):
      if (categoria==self.CATEGORIA_CON_VICTIMAS):
        builder.and(builder.gt(
          builder.variable("TOTAL_VICTIMAS"), 
          builder.constant(0)
          )
        )
      elif (categoria==self.CATEGORIA_CON_DANOS):
        builder.and(builder.eq(
          builder.variable("TOTAL_VICTIMAS"), 
          builder.constant(0)
          )
        )
    if (peligrosas):
        pass
    """
        builder.and(builder.eq(
          builder.variable("TOTAL_VICTIMAS"), 
          builder.constant(0)
          )
        )
    """
    opbuilder = expManager.createExpressionBuilder()
    allBuilder = expManager.createExpressionBuilder()
    valueMortales = None
    print "Mortales:", mortales
    if (mortales!=""):
      valueMortales = opbuilder.binaryOperator(
        mortalesOperador,
        opbuilder.variable("TOTAL_MUERTOS"), 
        opbuilder.constant(mortales)
        )
      
      allBuilder.and(valueMortales)

    valueGraves = None
    print "Graves:", graves
    if (graves!=""):
      valueGraves = opbuilder.binaryOperator(
        gravesOperador,
        opbuilder.variable("TOTAL_GRAVES"), 
        opbuilder.constant(graves)
        )
      if (valueMortales!=""):
        if (operator1 == ExpressionBuilder.OPERATOR_AND):
          allBuilder.and(valueGraves)
        elif (operator1 == ExpressionBuilder.OPERATOR_OR):
          allBuilder.or(valueGraves)
          

    valueLeves = None
    print "Leves: ", leves
    if (leves!=""):
      valueLeves = opbuilder.binaryOperator(
        levesOperador,
        opbuilder.variable("TOTAL_LEVES"), 
        opbuilder.constant(leves)
        )
      
      if (valueMortales!="" or valueGraves!=""):
        if (operator2 == ExpressionBuilder.OPERATOR_AND):
          allBuilder.and(valueLeves)
        elif (operator2 == ExpressionBuilder.OPERATOR_OR):
          allBuilder.or(valueLeves)

    allValue = allBuilder.value()
    if (allValue!=None):
      builder.and(allValue)
    
    return builder.value()


  def checkModify(self):
    iconTheme = ToolsSwingLocator.getIconThemeManager().getDefault()
    print (
        self.mortalesOperador.getSelectedIndex() == 0,
        self.operator1.getSelectedIndex() == 0,
        self.gravesOperador.getSelectedIndex() == 0,
        self.operator2.getSelectedIndex() == 0,
        self.levesOperador.getSelectedIndex()==0,
        self.mortales.getText()=="",
        self.graves.getText()=="",
        self.leves.getText()=="")

    if (self.categoria.getSelectedItem().getValue() == "" and
        self.peligrosas==False and
        self.mortales.getText()=="" and
        self.graves.getText()=="" and
        self.leves.getText()==""):
          #icon = createIcon(Color.RED)
          icon = iconTheme.get("accidentcondition-tabtick-disabled")
          self.tabPanel.setIconAt(self.TAB_INDEX_PANEL, icon)
          return False
    else:
        icon = iconTheme.get("accidentcondition-tabtick-enabled")
        #icon = createIcon(Color.GREEN)
        self.tabPanel.setIconAt(self.TAB_INDEX_PANEL, icon)
        return True
def main(*args):

    #Remove this lines and add here your code

    print "hola mundo"
    pass
