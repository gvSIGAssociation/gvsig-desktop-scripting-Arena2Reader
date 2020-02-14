# encoding: utf-8
from org.gvsig.tools.swing.api import ToolsSwingLocator
from java.awt.image import BufferedImage
from java.awt import Color
from java.awt.event import ActionListener
from javax.swing.event import DocumentListener
from javax.swing import ImageIcon, DefaultComboBoxModel
from org.gvsig.expressionevaluator import ExpressionEvaluatorLocator
import gvsig
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
class TabControllerCarretera(ActionListener, DocumentListener):
  TAB_INDEX_PANEL = 1
  def __init__(self, tabPanel, provincia, carretera, pki,pkiu, pkf, pkfu, sentido):
    self.tabPanel = tabPanel
    self.provincia = provincia
    self.carretera = carretera
    self.pki = pki
    self.pkiu = pkiu
    self.pkf = pkf
    self.pkfu = pkfu
    self.sentido = sentido
    self.initComponents()
    
  def initComponents(self):
    self.provincia.addActionListener(self)
    self.carretera.getDocument().addDocumentListener(self)
    self.pki.getDocument().addDocumentListener(self)
    self.pkiu.getDocument().addDocumentListener(self)
    self.pkf.getDocument().addDocumentListener(self)
    self.pkfu.getDocument().addDocumentListener(self)
    self.sentido.addActionListener(self)
    
  def clear(self):
    self.provincia.setSelectedIndex(0)
    self.carretera.setText("")
    self.pki.setText("")
    self.pkiu.setText("")
    self.pkf.setText("")
    self.pkfu.setText("")
    self.sentido.setSelectedIndex(0)
    
  def checkModify(self):
    iconTheme = ToolsSwingLocator.getIconThemeManager().getDefault()
    if (self.provincia.getSelectedItem().getValue()=="" and
        self.carretera.getText()=="" and
        self.pki.getText()=="" and
        self.pkiu.getText()=="" and
        self.pkf.getText()=="" and
        self.pkfu.getText()=="" and
        self.sentido.getSelectedItem().getValue()==""):
          #icon = createIcon(Color.RED)
          icon = iconTheme.get("accidentcondition-tabtick-disabled")
          self.tabPanel.setIconAt(self.TAB_INDEX_PANEL, icon)
          return False
    else:
      #icon = createIcon(Color.GREEN)
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
    #print "REturn tabCarretera:", builder.toString()
    return builder.value()
      
def main(*args):

    #Remove this lines and add here your code

    print "hola mundo"
    pass
