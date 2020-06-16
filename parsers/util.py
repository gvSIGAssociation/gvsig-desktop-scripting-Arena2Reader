# encoding: utf-8

import gvsig
import sys

from java.lang import Object 

class Descriptor(Object):
  def __init__(self, name, type, size=None, sep=None, **args):
    self.name = name
    self.type = type
    self.size = size
    self.sep = sep
    self.args = args
    self.tags = dict()

  def toString(self):
    return self.build()
    
  def build(self):
    if self.sep == None:
      self.sep = ":"
      for value in self.args.itervalues():
        if isinstance(value,basestring) and ":" in value:
          self.sep = "/"
          break
    desc = "%s%s%s" % (self.name, self.sep, self.type)
    if self.size!=None:
      desc = desc + "%sset%ssize=%s" % (self.sep, self.sep, self.size)
    for name, value in self.args.iteritems():
        desc = desc + "%sset%s%s=%s" % (self.sep,self.sep,name, value)
    for name, value in self.tags.iteritems():
      desc = desc + "%stag%s%s=%s" % (self.sep,self.sep,name, value)
    return desc

  def set(self,name, value):
    self.args[name] = value
    return self
    
  def tag(self,name, value):
    self.tags[name] = value
    return self
    
  def foreingkey(self, table, code, label):
    self.set("foreingkey",True)
    self.set("foreingkey.table",table)
    self.set("foreingkey.code",code)
    self.set("foreingKey.Label",label)
    self.set("foreingkey.closedlist",False)
    return self
  
  def closedlistfk(self, table, code="ID", label="FORMAT('%02d - %s',ID,DESCRIPCION)"):
    self.set("foreingkey",True)
    self.set("foreingkey.closedlist",True)
    self.set("foreingkey.table",table)
    self.set("foreingkey.code",code)
    self.set("foreingKey.Label",label)
    return self
  
  selectablefk = closedlistfk
  
  def relatedFeatures(self, table, tablekey, tablecolumns, expression):
    self.set("expression",expression)
    self.tag("dynform.label.empty",True)
    self.tag("DAL.RelatedFeatures.Columns","/".join(tablecolumns))
    self.tag("DAL.RelatedFeatures.Table",table)
    self.tag("DAL.RelatedFeatures.Unique.Field.Name",tablekey)
    return self

def generate_translations(columns):
  translations = dict()
  for columdef in columns:
    for prop in ("label", "shortlabel", "group"):
      s=columdef.args.get(prop,None)
      if s != None:
        translations[s]=s.strip()
    for prop in ("dynform.separator",):
      s=columdef.tags.get(prop,None)
      if s != None:
        translations[s]=s.strip()
  l = list()
  l.extend(translations.keys())
  l.sort()
  for s in l:
    print "%s=%s" % (s,s.replace("_"," ").strip())
  
  

def get2(x, key1, key2):
  try:
    v = x.get(key1,None)
    if v == None:
      return None
    if key2=="#text" and isinstance(v,basestring):
      return v
    return v.get(key2, None)
  except:
    ex = sys.exc_info()[1]
    gvsig.logger("No se puede leer %s.%s. %s" % (key1,key2,str(ex)), gvsig.LOGGER_WARN, ex)
    raise
    
def get1(x, key1, defvalue=None):
  try:
    return x.get(key1,defvalue)
  except:
    ex = sys.exc_info()[1]
    gvsig.logger("No se puede leer %s. %s" % (key1,str(ex)), gvsig.LOGGER_WARN, ex)
    raise
  
def sino2bool(n):
  if n==None:
    return None
  if n.lower()=="no":
    return False
  return True

def null2empty(n):
  if n==None:
    return ""
  return n

def null2zero(n):
  if n==None:
    return 0
  return n

def main(*args):
  print "hola"
  
