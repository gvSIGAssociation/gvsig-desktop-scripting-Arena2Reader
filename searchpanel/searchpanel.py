# encoding: utf-8

import gvsig
from org.gvsig.fmap.dal.swing import DALSwingLocator
#from org.gvsig.fmap.dal.swing.searchpanel import SearchConditionPanelFactory
from gvsig.libs.formpanel import FormPanel
from gvsig import getResource
from org.gvsig.fmap.dal.swing.searchpanel import SearchConditionPanel
from org.gvsig.tools import ToolsLocator

class SearchArena2Panel(FormPanel, SearchConditionPanel):
  def __init__(self):
    FormPanel.__init__(self,getResource(__file__,"searchpanel.xml"))
    i18n = ToolsLocator.getI18nManager()
  def clear(self):
    return None

  def get(self):
    return None

  def set(self, fil):
    pass

  def setEnabled(self, enabled):
    pass
  
  def getFactory(self):
    return SearchArena2Factory()
    
class SearchArena2Factory(SearchConditionPanel.SearchConditionPanelFactory):
  def isApplicable(self, store):
    if "ARENA2_ACCIDENTES" in str(store.getName()):
      return True
    return False
  def create(self, os): #SearchConditionPanel
    return SearchArena2Panel()
  def getName(self):
    return "Accidentes"
    
def main(*args):

    manager = DALSwingLocator.getDataSwingManager();
    factory = SearchArena2Factory()
    panel = factory.create(None)
    panel.showTool("Centrar Coordenadas")
    manager.registerSearchConditionPanel(factory) #SearchConditionPanelFactory
