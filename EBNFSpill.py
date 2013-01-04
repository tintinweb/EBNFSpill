'''
Created on 27.12.2012

@author: martin
'''
'''
Created on 27.12.2012

@author: martin
'''
from simpleparse.parser import Parser


class StopRecursionException(Exception):
    def __init__(self,obj):
        self.obj=obj
    def getObj(self):
        return self.obj
    
class Tdef(object):
    # special one :)
    MATCH_RECURSION = 0xFEED0           #custom
    MATCH_RECURSION_EXCEPTION = 0xFEED1 #custom

    # taken from mxTextTools.h
    MATCH_ALLIN = 11
    MATCH_ALLNOTIN = 12
    MATCH_IS = 13
    MATCH_ISIN = 14
    MATCH_ISNOTIN = 15
    
    MATCH_WORD = 21
    MATCH_WORDSTART = 22
    MATCH_WORDEND = 23
    
    MATCH_ALLINSET = 31
    MATCH_ISINSET = 32
    
    MATCH_ALLINCHARSET = 41
    MATCH_ISINCHARSET = 42
    
    MATCH_MAX_LOWLEVEL = 99
    
    #/* Jumps and other low-level special commands */
    
    MATCH_FAIL = 100
    MATCH_JUMP = MATCH_FAIL
    
    MATCH_EOF = 101
    MATCH_SKIP = 102
    MATCH_MOVE = 103
    
    MATCH_JUMPTARGET = 104
    
    MATCH_MAX_SPECIALS = 199
    
    #/* Higher-level string matching */
    
    MATCH_SWORDSTART = 211
    MATCH_SWORDEND = 212
    MATCH_SFINDWORD = 213
    MATCH_NOWORD = MATCH_SWORDSTART
    
    #/* Higher-level special commands */
    MATCH_CALL = 201
    MATCH_CALLARG = 202
    MATCH_TABLE = 203
    MATCH_SUBTABLE = 207
    MATCH_TABLEINLIST = 204
    MATCH_SUBTABLEINLIST = 208
    MATCH_LOOP = 205
    MATCH_LOOPCONTROL = 206
    
    #/* Special argument integers */
    MATCH_JUMP_TO = 0
    MATCH_JUMP_MATCHOK = 1000000
    MATCH_JUMP_MATCHFAIL = -1000000
    MATCH_MOVE_EOF = -1
    MATCH_MOVE_BOF = 0
    MATCH_FAIL_HERE = 1
    MATCH_THISTABLE = 999
    MATCH_LOOPCONTROL_BREAK = 0
    MATCH_LOOPCONTROL_RESET = -1
    
    def toName(self):
        r = {}
        for defname in [x for x in dir(self) if x.startswith("MATCH_")]:
            r[getattr(self,defname)]=defname
        return r

import random
import collections

class EBNFSpill(object):
    DEFAULT_MAX_TIMES_CHAR = 35
    DEFAULT_MAX_TIMES_FUNC = 10
    DEFAULT_MAX_SELF_RECURSION = 25
    DEFAULT_MAX_WALK_RECURSION = 100

    def __init__(self,showTags=False,showTagsRecursive=False,recursionLevel=0):
        self._reset()
        self.showTags=showTags
        self.showTagsRecursive=showTagsRecursive
        self.recursionLevelObj=recursionLevel
        
        if self.recursionLevelObj>self.DEFAULT_MAX_SELF_RECURSION: raise Exception("a")
        #print "INIT",recursionLevel
        pass
    
    def __del__(self):
        self.recursionLevelObj-=1
        pass
    
    def validate(self,data):
        return self.parser.parse(data)
    
    def setDeclaration(self,declaration,production):
        self.parser = Parser(declaration, production)
        self.table =  self.parser.buildTagger(production=production)
    
    def setTable(self,table,nodes=None):
        self.table = table
        self.nodes=nodes or self.nodes
    
    def _reset(self):
        self.nodes = {}
        self.ctx = []       # context (infos like recurion for table2)
        #self.recursionLevelObj=0
        self.recursionLevelWalk=0
        random.seed()
        
    def setDefaults(self,**kwargs):
        valid_defaults = [i for i in dir(self) if i.startswith("DEFAULT_")]
        for k,v in kwargs.iteritems():
            if k in valid_defaults:
                setattr(self,k,v)
            else:
                raise Exception("Not allowed to change %s to %s (valid options: %s)"%(k,v,valid_defaults))
    
    def getTable(self):
        return self.table

    def getTagName(self,node):
        if self.showTags and node[0]:
            return "<%s>"%node[0]
        return ""
    
    def checkTypeIterable(self,l):
        return isinstance(l, collections.Iterable) and not isinstance(l, basestring)
    def checkTypeIterableRecursive(self,l):
        return isinstance(l, collections.Iterable) and not isinstance(l, basestring) and isinstance(l,tuple) and isinstance(l[0],list) and isinstance(l[1],int)

    def checkTypeNodeBase(self,l):
        #checks ( None|str, int, *)
        return self.checkTypeIterable(l) and len(l)>=2 and (l[0]==None or isinstance(l[0],basestring)) and isinstance(l[1],int)
    def checkTypeNodeWithChilds(self,l):
        #print "check_",str(l)[:50]
        try:
            #print "check_metric",checkTypeNodeBase(l),len(l)>=3 , checkTypeIterable(l[2])
            pass
        except:
            pass
        return self.checkTypeNodeBase(l) and len(l)>=3 and self.checkTypeIterable(l[2])
    
    def next(self):
        return

    def rndTimesFunc(self,sample_func,args,minlen=0,maxlen=None):
        maxlen = maxlen or self.DEFAULT_MAX_TIMES_FUNC
        maxlen+=1
        out = ""
        for i in range(random.randrange(minlen,maxlen)):
            out+=sample_func(args)
        return out   

    def rndTimes(self,sample,minlen=0,maxlen=None):
        maxlen = maxlen or self.DEFAULT_MAX_TIMES_CHAR
        maxlen+=1
        out = ""
        for i in range(random.randrange(minlen,maxlen)):
            out+=sample
        return out
    
    def rndSelect(self,haystack,sample_len=1,minlen=0,maxlen=None):
        maxlen = maxlen or self.DEFAULT_MAX_TIMES_CHAR
        maxlen+=1
        out = ""
        for i in range(random.randrange(minlen,maxlen)):
            out += "".join(random.sample(haystack,sample_len))
        
        return out

    def eval(self,node):
        # different lenght commandos
        #print node
        #print id(node),node
        #if self.recursionLevelObj>self.DEFAULT_MAX_SELF_RECURSION or self.recursionLevelWalk>self.DEFAULT_MAX_WALK_RECURSION:
        #    return "<recursion_exception>"
        
        if not node:
            return ""
        
        if len(node)<3:
            raise Exception( "<3 - %s"%repr(node) )          #this is an error!
        
        elif node[1]==Tdef.MATCH_RECURSION_EXCEPTION:
            return "<<"
        
        elif node[1]==Tdef.MATCH_RECURSION:
            # create a new EBNFSpill object, and resolv this one?
            #print node[2],self.nodes[node[2]]
            self.recursionLevelObj+=1
            try:
                x = EBNFSpill(showTags=self.showTagsRecursive,recursionLevel=self.recursionLevelObj)
                x.setTable(self.table)
                recr_node=self.nodes[node[2]]
            except:
                return ""
            
            #
            #print "REKR",node
            #print "REKR2",self.nodes
            #print "<DAMN_RECURSION %s wild=%s>"%(node[2],self.ctx)
            #return "<RECURSION"
            
            #print "EXCEPT:",node[2],self.nodes
            #return self.rndTimes(x.generate(recr_node['obj']), 0, 3)
            return self.getTagName(node)+x.generate(recr_node)
        
        # single words/selections
        elif len(node)==3:
            if node[1]==Tdef.MATCH_WORD or node[1]==Tdef.MATCH_IS:
                return self.getTagName(node)+node[2]
            elif node[1]==Tdef.MATCH_ALLIN or node[1]==Tdef.MATCH_ISIN:
                return self.getTagName(node)+self.rndSelect(node[2],minlen=1,maxlen=1)
            elif node[1]==Tdef.MATCH_TABLE:
                # (xyz,MATCH_TABLE, <table>, 1)  == exact 1
                # (xyz,MATCH_TABLE, <table>, 2,1)  == *
                return self.getTagName(node)+""
                #return "<TABLE: %s>"%node[0]
        
        # mostly recursive ones
        elif len(node)>3:
            # recursions and stuff
            if node[1]==Tdef.MATCH_IS or node[1]==Tdef.MATCH_IS:
                # like (none,"MATCH_IS",'c',1,0) - choose zero or xx times
                return self.getTagName(node)+self.rndTimes(node[2])
            elif node[1]==Tdef.MATCH_ALLIN or node[1]==Tdef.MATCH_ISIN:
                return self.getTagName(node)+self.rndSelect(node[2])
            
            elif node[1]>=Tdef.MATCH_CALL and node[1]<=Tdef.MATCH_SUBTABLEINLIST:
                # (xyz,MATCH_TABLE, <table>, 1)  == exact 1
                # (xyz,MATCH_TABLE, <table>, 2,1)  == *
                self.recursionLevelObj+=1
                try:
                    x = EBNFSpill(showTags=self.showTagsRecursive,recursionLevel=self.recursionLevelObj)
                except:
                    return ""
                x.setTable(self.table)
                #print "<TABLE: %s | %s  || %s || nodeid:%s>"%(node[0:1],node[3],self.ctx,id(node[3]))
                #print node[2]
                #return self.getTagName(node)+""
                return self.getTagName(node)+self.rndTimesFunc(x.generate,(node[2]))            
        
        
        return self.getTagName(node)

    def generate(self,node=None):
        out = ""
        for n in self.walk(node):
            #print n
            #print self.recursionLevelObj,self.recursionLevelWalk

            out+= self.eval(n)

        return out

    def process(self,l):
        if self.checkTypeNodeBase(l):
            return (l[0],Tdef().toName()[l[1]])+l[2:]
        return l

    def _checkRecursion(self,node):
        # return boolean if boolean=True
        nID = id(node)

        #print "-->",nID, " NODE ",node
        if self.nodes.has_key(nID):
            raise StopRecursionException(('[RECURSION of Node=%s]'%nID,Tdef.MATCH_RECURSION,nID))
        #self.nodeIDs.append(nID)
        #print nID,node
        return node
    
    def _trackNode(self,node,nodeID=None):
        nID = nodeID or id(node)
        #print node
        if self.checkTypeNodeBase(node):
            #print "ISIN1",Tdef.MATCH_CALL,Tdef.MATCH_SUBTABLEINLIST,node[1],node[1]>=Tdef.MATCH_CALL and node[1]<=Tdef.MATCH_SUBTABLEINLIST
            
            if node[1]>=Tdef.MATCH_CALL and node[1]<=Tdef.MATCH_SUBTABLEINLIST:
                #print "ISIN2"
                #print "--- add BASE",id(node),node
                self.nodes[nID]=node
        elif self.checkTypeIterable(node):
            #print "--- add LIST",id(node),node
            self.nodes[nID]=node
        return node 
    
    def _pushLevel(self,node):
        # add one level. . to check recursion space
        if node[1]>=Tdef.MATCH_CALL and node[1]<=Tdef.MATCH_SUBTABLEINLIST  \
          and len(node)>3 and node[3]==2:  
            #print "push__"
            self.ctx.append(id(node))
        return node
    
    def _popLevel(self,node):
        if node[1]>=Tdef.MATCH_CALL and node[1]<=Tdef.MATCH_SUBTABLEINLIST  \
          and len(node)>3 and node[3]==2:
            #print "pop___"
            return self.ctx.pop()
        return node
    
    def walk(self,table=None):
        table=table or self.table
        if not table: raise Exception("EBNF TagTable not set, please generate [.setDeclaration()] or set one [.setTable()]")       #must not be !NONE!, please .setDeclaration() first!
        
        retn =  self._walk(table)
        self._reset()
        return retn

    def _walk(self,l):
        # check if (None|basestring, int, ... ) > 2
        #import time
        #time.sleep(0.8)
        #print "BEGIN",str(l)[:50]
        #recursion check
        if self.recursionLevelObj>self.DEFAULT_MAX_SELF_RECURSION or self.recursionLevelWalk>self.DEFAULT_MAX_WALK_RECURSION:
            #print self.recursionLevelWalk
            #print self.recursionLevelObj
            #nID=
            #raise StopRecursionException(('[RECURSION of Node=%s]'%nID,Tdef.MATCH_RECURSION,nID))
            #print self.nodes
            #yield l
            #print "StopIter",l
            #print self.recursionLevelObj,self.recursionLevelWalk
            raise StopIteration("HMM")
            #yield (None,Tdef.MATCH_RECURSION_EXCEPTION,())
            #raise StopRecursionException(("[RECURSION_EXCEPTION_LEVEL_REACHED]",Tdef.MATCH_RECURSION_EXCEPTION,None))
        self.recursionLevelWalk+=1
        #print id(l),len(l),l
        

        try:  
            if self.checkTypeNodeWithChilds(l):
                #print "Childs"
                self._checkRecursion(l)
                yield self._trackNode(l)
                self._pushLevel(l)
                for e in self._walk(l[2]):
                    yield e
                self._popLevel(l)
                    
            elif self.checkTypeNodeBase(l):
                #print "Base"
                self._checkRecursion(l)
                yield self._trackNode(l)
       
            elif self.checkTypeIterableRecursive(l):
                #print "xxx",l[0][0]
                nID=id(l[0][0])
                #print "IterReck"
                #print '[RECURSION of Node=%s]'%nID
                #TODO: does not work
                #fixme: does not work - recurses too much
                raise StopRecursionException(('[RECURSION of Node=%s]'%nID,Tdef.MATCH_RECURSION,nID))
                    
            elif self.checkTypeIterable(l):
                #print "list"
                self._checkRecursion(l)
                self._trackNode(l)              # checkTypeIterableRecursive refs one of these nodes :( // damn need to reparse if this doesnt work out
                #self._pushLevel(l)
                for e in l:
                    self._pushLevel(e)
                    for x in self._walk(e):
                        yield x             #do not check recursion here.. this is not what we want
                    self._popLevel(e)
                #self._popLevel(l)
            else:
                self._checkRecursion(l)
                print "Elem? - ",l
                #print self.checkTypeNodeWithChilds(l),self.checkTypeNodeBase(l),self.checkTypeIterable(l)
                yield self._trackNode(l)
        
        except StopRecursionException, e:
            #print self.nodes[e.getObj()[2]]
            #print "Except:",e.getObj()
            yield e.getObj()

    
        self.recursionLevelWalk-=1


         
if __name__=="__main__":
    x = EBNFSpill(showTags=True)
    x.setDefaults(DEFAULT_MAX_TIMES_CHAR=9)
    print x.rndTimes("a", 0,1)   
    print x.rndTimes("b", 1,2)  
    print x.rndTimes("c", 1,2) 
    print x.rndTimes("c")  
    
    print x.rndSelect("abcdefghijklmnopqrstuvwxyz", 10, 0, 5)