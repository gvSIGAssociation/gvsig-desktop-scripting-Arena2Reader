# encoding: utf-8

import gvsig

from java.lang import Object 

class Descriptor(Object):
  def __init__(self, name, type, size=None, sep=None, **args):
    self.name = name
    self.type = type
    self.size = size
    self.sep = sep
    self.args = args

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
      if self.isTag(name):
        desc = desc + "%stag%s%s=%s" % (self.sep,self.sep,name, value)
      else:
        desc = desc + "%sset%s%s=%s" % (self.sep,self.sep,name, value)
    return desc

  def set(self,name, value):
    self.args[name] = value
    return self
    
  def isTag(self, name):
    name = name.lower()
    if name.startswith("dynform."):
      return True
    if name.startswith("dal."):
      return True
    return False
  
  def foreingkey(self, table, code, label):
    self.args["foreingkey"]=True
    self.args["foreingkey.table"]=table
    self.args["foreingkey.code"]=code
    self.args["foreingKey.Label"]=label
    return self
  
  def selectablefk(self, table, code="ID", label="FORMAT('%02d - %s',ID,DESCRIPCION)"):
    self.args["foreingkey"]=True
    self.args["foreingkey.selectable"]=True
    self.args["foreingkey.table"]=table
    self.args["foreingkey.code"]=code
    self.args["foreingKey.Label"]=label
    return self
      
  def relatedFeatures(self, table, tablekey, tablecolumns, expression):
    self.args["expression"]=expression
    self.args["dynform.label.empty"]=True
    self.args["DAL.RelatedFeatures.Columns"]="/".join(tablecolumns)
    self.args["RelatedFeatures.table"]=table
    self.args["DAL.RelatedFeatures.Unique.Field"]=tablekey
    return self

  

def get2(x, key1, key2):
  v = x.get(key1,None)
  if v == None:
    return None
  return v.get(key2, None)

def get1(x, key1):
  return x.get(key1,None)
  
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

  