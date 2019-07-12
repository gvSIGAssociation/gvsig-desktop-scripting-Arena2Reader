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
    return self
  
  def selectablefk(self, table, code="ID", label="FORMAT('%02d - %s',ID,DESCRIPCION)"):
    self.set("foreingkey",True)
    self.set("foreingkey.selectable",True)
    self.set("foreingkey.table",table)
    self.set("foreingkey.code",code)
    self.set("foreingKey.Label",label)
    return self
      
  def relatedFeatures(self, table, tablekey, tablecolumns, expression):
    self.args["expression"]=expression
    self.tags["dynform.label.empty"]=True
    self.tags["DAL.RelatedFeatures.Columns"]="/".join(tablecolumns)
    self.tags["RelatedFeatures.table"]=table
    self.tags["DAL.RelatedFeatures.Unique.Field"]=tablekey
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

  