
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


declaration = """
file              :=  line+
line              :=  a*,b*,'\n'
a    := [a-z]
b    := [A-Z]
"""

from EBNFSpill import EBNFSpill
from pprint import pprint


b = EBNFSpill(showTags=False)
b.setDeclaration(declaration,production="file")

print "----------[ #1 prettyprint AST ]----------"
table = b.getTable()
pprint (table)

print "----------[ #2 Generate Random Data ]----------"
# generate random Data
data= b.generate()
print data
print "----------[ #3 Validate generated Data ]----------"
success, children, nextcharacter = b.validate( data)
if not (success and nextcharacter==len(data)):
    print """Wasn't able to parse %s as a %s (%s chars parsed of %s), returned value was %s"""%( repr(data), "file", nextcharacter, len(data), (success, children, nextcharacter))
    print "success %s, nextchar==len(data)=%s"%(success,nextcharacter==len(data))
else:
    print "VALID"

# walk parsing / evaluation process
print "----------[ #4 walk / eval AST ]----------"
x= 0        
for i in b.walk():
    x+=1
    print x,id(i),b.process(i)


