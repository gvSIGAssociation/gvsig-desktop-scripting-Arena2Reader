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
from org.gvsig.fmap.dal import DALLocator
from org.gvsig.tools.dataTypes import DataTypes
from javax.json import Json, JsonValue
from org.gvsig.tools.dataTypes import DataTypeUtils

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
      ListElement(i18n.getTranslation(u'_Con_victimas'),self.CATEGORIA_CON_VICTIMAS),
      ListElement(i18n.getTranslation(u'_Con_danos'),self.CATEGORIA_CON_DANOS)
      ]
    self.categoria.setModel(DefaultComboBoxModel(listCategoriaElements))
    
    listOperatorElements = [
        ListElement(i18n.getTranslation(u'_And'),ExpressionBuilder.OPERATOR_AND),
        ListElement(i18n.getTranslation(u'_Or'),ExpressionBuilder.OPERATOR_OR)
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
    self.peligrosas.addActionListener(self)
    self.mortalesOperador.addActionListener(self)
    self.operator1.addActionListener(self)
    self.gravesOperador.addActionListener(self)
    self.operator2.addActionListener(self)
    self.levesOperador.addActionListener(self)
    self.mortales.getDocument().addDocumentListener(self)
    self.graves.getDocument().addDocumentListener(self)
    self.leves.getDocument().addDocumentListener(self)
    
  def toJson(self):
    categoria = self.categoria.getSelectedItem().getValue()
    peligrosas = self.peligrosas.isSelected()
    mortalesOperador = self.mortalesOperador.getSelectedItem().getValue()
    operator1 = self.operator1.getSelectedItem().getValue()
    gravesOperador = self.gravesOperador.getSelectedItem().getValue()
    operator2 = self.operator2.getSelectedItem().getValue()
    levesOperador = self.levesOperador.getSelectedItem().getValue()

    mortales = self.mortales.getText()
    graves = self.graves.getText()
    leves = self.leves.getText()
    
    builder = Json.createObjectBuilder();
    if not categoria=="": builder.add("categoria", categoria)
    peligrosasJson = JsonValue.TRUE if peligrosas else JsonValue.FALSE
        
    builder.add("peligrosas", peligrosasJson)
    if not mortalesOperador=="": builder.add("mortalesOperador", mortalesOperador)
    if not operator1=="": builder.add("operator1", operator1)
    if not gravesOperador=="": builder.add("gravesOperador", gravesOperador)
    if not operator2=="": builder.add("operator2", operator2)
    if not levesOperador=="": builder.add("levesOperador", levesOperador)
    if not mortales=="": builder.add("mortales", mortales)
    if not graves=="": builder.add("graves", graves)
    if not leves=="": builder.add("leves", leves)
    finalJson = builder.build()
    return finalJson

  def fromJson(self, json):
        if (json==None):
            return json
        categoria = json.getInt("categoria") if json.containsKey("categoria") else None

        peligrosas = json.getBoolean("peligrosas") if json.containsKey("peligrosas") else None
        mortalesOperador = json.getString("mortalesOperador") if json.containsKey("mortalesOperador") else None
        operator1 = json.getString("operator1") if json.containsKey("operator1") else None
        gravesOperador =json.getString("gravesOperador") if json.containsKey("gravesOperador") else None
        operator2 = json.getString("operator2") if json.containsKey("operator2") else None
        levesOperador = json.getString("levesOperador") if json.containsKey("levesOperador") else None
        
        mortales = json.getString("mortales") if json.containsKey("mortales") else None
        graves = json.getString("graves") if json.containsKey("graves") else None
        leves = json.getString("leves") if json.containsKey("leves") else None
        
        
        self.setValues(categoria, peligrosas, mortalesOperador, operator1, gravesOperador, operator2, levesOperador, mortales, graves, leves)
        
  def setValues(self, categoriaValues, peligrosasValues, mortalesOperadorValues, operator1Values, gravesOperadorValues, operator2Values, levesOperadorValues, mortalesValues, gravesValues, levesValues):
      if categoriaValues!=None: 
          ListElement.setSelected(self.categoria, categoriaValues)
      if peligrosasValues!=None: 
          self.peligrosas.setSelected(peligrosasValues)
      if mortalesOperadorValues != None:
          ListElement.setSelected(self.mortalesOperador, mortalesOperadorValues)
      if operator1Values != None:
          ListElement.setSelected(self.operator1, operator1Values)
      if gravesOperadorValues != None:
          ListElement.setSelected(self.gravesOperador, gravesOperadorValues)
      if operator2Values != None:
          ListElement.setSelected(self.operator2, operator2Values)
      if levesOperadorValues != None:
          ListElement.setSelected(self.levesOperador, levesOperadorValues)
      if mortalesValues != None:
          self.mortales.setText(mortalesValues)
      if gravesValues != None:
          self.graves.setText(gravesValues)   
      if levesValues != None:
          self.leves.setText(levesValues)
  def clear(self):
    self.peligrosas.setSelected(False)
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
    if (self.checkModify()==False):
      return None
    expManager= ExpressionEvaluatorLocator.getManager()
    exp = expManager.createExpression()
    builder = expManager.createExpressionBuilder()
    
    categoria = self.categoria.getSelectedItem().getValue()
    peligrosas = self.peligrosas.isSelected()
    mortalesOperador = self.mortalesOperador.getSelectedItem().getValue()
    operator1 = self.operator1.getSelectedItem().getValue()
    gravesOperador = self.gravesOperador.getSelectedItem().getValue()
    operator2 = self.operator2.getSelectedItem().getValue()
    levesOperador = self.levesOperador.getSelectedItem().getValue()

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
        dataManager = DALLocator.getDataManager()
        #EXISTS(SELECT LID_VEHICULO FROM ARENA2_VEHICULOS WHERE ARENA2_ACCIDENTES.ID_ACCIDENTE = ARENA2_VEHICULOS.ID_ACCIDENTE AND  MP LIMIT 1)
        dalbuilder = dataManager.createDALExpressionBuilder() #DALExpressionBuilder
        peligrosasfilter = dalbuilder.exists(dalbuilder.select()
          .column("LID_VEHICULO")
          .from("ARENA2_VEHICULOS")
          .limit(1)
          .where(
          dalbuilder.expression().and(
            dalbuilder.expression().eq(
              dalbuilder.expression().getattr("ARENA2_ACCIDENTES","ID_ACCIDENTE"),
              dalbuilder.expression().getattr("ARENA2_VEHICULOS","ID_ACCIDENTE")
            ),
            dalbuilder.expression().column("MP")
          )).toValue())
        builder.and(peligrosasfilter)

    # TOTAL -> Juntos en allbuilder. como apoyo opbuilder
    opbuilder = expManager.createExpressionBuilder()
    allBuilder = expManager.createExpressionBuilder()
    valueMortales = None
    if (mortales!=""):
      valueMortales = opbuilder.binaryOperator(
        mortalesOperador,
        opbuilder.variable("TOTAL_MUERTOS"), 
        opbuilder.constant(mortales, DataTypes.INT)
        )
      
      allBuilder.and(valueMortales)

    valueGraves = None
    if (graves!=""):
      valueGraves = opbuilder.binaryOperator(
        gravesOperador,
        opbuilder.variable("TOTAL_GRAVES"), 
        opbuilder.constant(graves, DataTypes.INT)
        )
      if (valueMortales!=""):
        if (operator1 == ExpressionBuilder.OPERATOR_AND):
          allBuilder.and(valueGraves)
        elif (operator1 == ExpressionBuilder.OPERATOR_OR):
          allBuilder.or(valueGraves)
          

    valueLeves = None
    if (leves!=""):
      valueLeves = opbuilder.binaryOperator(
        levesOperador,
        opbuilder.variable("TOTAL_LEVES"), 
        opbuilder.constant(leves, DataTypes.INT)
        )
      
      if (valueMortales!="" or valueGraves!=""):
        if (operator2 == ExpressionBuilder.OPERATOR_AND):
          allBuilder.and(valueLeves)
        elif (operator2 == ExpressionBuilder.OPERATOR_OR):
          allBuilder.or(valueLeves)

    allValue = allBuilder.value()
    if (allValue!=None): # Unimos TOTAL_ con builder
      builder.and(allValue)
    
    return builder.value()


  def checkModify(self):
    iconTheme = ToolsSwingLocator.getIconThemeManager().getDefault()

    if (self.categoria.getSelectedItem().getValue() == "" and
        self.peligrosas.isSelected()==False and
        self.mortales.getText()=="" and
        self.graves.getText()=="" and
        self.leves.getText()==""):
          icon = iconTheme.get("accidentcondition-tabtick-disabled")
          self.tabPanel.setIconAt(self.TAB_INDEX_PANEL, icon)
          return False
    else:
        icon = iconTheme.get("accidentcondition-tabtick-enabled")
        self.tabPanel.setIconAt(self.TAB_INDEX_PANEL, icon)
        return True
        
def main(*args):
    print "hola mundo"
    pass
