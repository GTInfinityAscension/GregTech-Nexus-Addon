import re,glob,os
gtna=open('/home/raishxn/MineProjects/GregTech-Nexus-Addon/src/main/java/com/raishxn/gtna/common/data/GTNABlocks.java').read()
have=set(re.findall(r'BlockEntry<[^>]*>\s+([A-Z0-9_]+)\s*=',gtna))
gtnaids=set()
for f in glob.glob('/home/raishxn/MineProjects/GregTech-Nexus-Addon/src/main/java/com/raishxn/gtna/**/*.java',recursive=True):
    gtnaids|=set(re.findall(r'multiblock\("([a-z0-9_]+)"',open(f).read()))
rows=[]
for f in glob.glob('*.java'):
    t=open(f).read()
    for m in re.finditer(r'MultiblockMachineDefinition\s+([A-Z0-9_]+)\s*=\s*multiblock\("([a-z0-9_]+)",\s*"[^"]*",\s*([^\n]+)',t):
        start=m.start(); end=t.find('.register();',start); body=t[start:end]
        mid=m.group(2)
        if mid in gtnaids: continue
        ctor=m.group(3).strip()
        ctor=re.sub(r'\).*','',ctor.split('::')[0] if '::' in ctor else ctor)[:45]
        blocks=set(re.findall(r'GTOBlocks\.([A-Z0-9_]+)',body))
        missing=sorted(b for b in blocks if b not in have)
        types=re.findall(r'recipeTypes?\(([^)]*)\)',body)
        types=','.join(types).replace('GTRecipeTypes.','gt:').replace('GTORecipeTypes.','')
        mbs='mbs' if 'MultiBlockFileReader' in body else ('inline' if 'FactoryBlockPattern' in body else '?')
        other=len(re.findall(r'GTOMachines\.|ExResearchMachines\.|ManaMachine',body))
        rows.append((len(missing),mid,ctor,mbs,types[:70],' '.join(missing)[:90],other,f))
rows.sort()
for r in rows: print(f"{r[0]:2d} {r[1]:42s} {r[3]:6s} {r[2][:40]:40s} | {r[4]} | {r[5]} {'(+gto machines)' if r[6] else ''}")
print(len(rows))
