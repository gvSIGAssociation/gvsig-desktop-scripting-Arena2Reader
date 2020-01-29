# encoding: utf-8

import gvsig
from org.gvsig.fmap.dal.swing import DALSwingLocator
from addons.Arena2Reader.searchpanel.searchpanel import SearchArena2Factory

def main(*args):
    manager = DALSwingLocator.getDataSwingManager();
    factory = SearchArena2Factory()
    manager.registerSearchConditionPanel(factory) #SearchConditionPanelFactory
