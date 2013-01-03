declaration = """
file           := content*

content        := (section / condition / comment / node), ts, '\n'*

condition      := '#!',[cobf], ts, node
comment        := '#', anychar* ,'\n'
section        := '[', word, ']', ts,'\n', node*, '\n'*
node           := word, option+, ts, '\n'

option         := option_type/options

options        := ts, ('sub'/'num'),'=',word
option_type    := ts, 'type=',('String'/'Num'/'List'/'bool'/'Section'),ts


string         := '"', word*, '"'
word           := ([a-zA-Z0-9-_()/\~.<>?;:])+
anychar        := ([a-zA-Z0-9-_()/\~.<>?;: \t])+
ts             := [ \t]*
"""

declaration = """
file              := (section, entry+, '\n\n')+

section           := '[', wordspecial, ']','\n'
entry             := word, '\t=', '"', wordspecial , '"', '\n'
alpha             := [a-zA-Z]
alphanum          := [a-zA-Z0-9]
alphanumspecial   := [a-zA-Z0-9_-]
word              := alpha,alphanum*
wordspecial       := alpha,alphanumspecial*
"""

dseclaration = """
file              :=  'n',file+
"""
from EBNFSpill import EBNFSpill
from pprint import pprint

#b = BNFSpill(declaration,production="file")
#table = b.getTable()
b = EBNFSpill(showTags=False)
b.setDeclaration(declaration,production="file")
table = b.getTable()
#pprint (table)

print b.generate(table)
#exit()
exit()
#b = BNFSpill(declaration,production="file")
table = b.getTable()

import time
x= 0        
for i in b.walk(table):
    x+=1
    #time.sleep(0.5)

    print x,id(i),b.process(i)


exit()