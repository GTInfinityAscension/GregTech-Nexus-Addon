import re,sys,gzip,struct
src,name,out=sys.argv[1:4]
t=open(src).read()
i=t.index(name+" = FactoryBlockPattern.start()")
j=t.index(";",i)
block=t[i:j]
aisles=[re.findall(r'"([^"]*)"',a) for a in re.findall(r'\.aisle\((.*?)\)\s*(?=\.aisle|$)',block,re.S)]
def vi(v):
    v&=0xffffffff;b=b''
    while True:
        x=v&0x7f;v>>=7
        if v:b+=bytes([x|0x80])
        else:return b+bytes([x])
d=vi(-1)+vi(1)+vi(2)+vi(0)+vi(4)+vi(len(aisles))
for a in aisles:
    d+=vi(len(a))
    for r in a:
        e=r.encode();d+=struct.pack('>H',len(e))+e
open(out,'wb').write(gzip.compress(d))
print(len(aisles),len(aisles[0]),len(aisles[0][0]),sorted(set(''.join(''.join(a) for a in aisles))))
