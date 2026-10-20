"""Materials page of the wiki: a hand-written intro plus the list of every GTNA material, in three languages.

    python3 tools/wiki/material_pages.py   -> docs/gameplay/materials/index.md, index.pt.md, index.zh.md

Names come from the mod's lang files (material.gtna.*); materials without a translation show the English name.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import zh_punct  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
OUT = os.path.join(ROOT, 'docs/gameplay/materials')


def lang(code):
    merged = {}
    for d in ('src/generated/resources', 'src/main/resources'):
        p = os.path.join(ROOT, d, f'assets/gtna/lang/{code}.json')
        if os.path.exists(p): merged.update(json.load(open(p, encoding='utf-8-sig')))
    return merged


EN, PT, ZH = lang('en_us'), lang('pt_br'), lang('zh_cn')
IDS = sorted(k[len('material.gtna.'):] for k in EN if k.startswith('material.gtna.') and k.count('.') == 2)

INTRO = {
    'en': ('# Materials\n\nGTNA registers **{n} materials** as GTCEu materials in the `gtna` namespace. Their items, blocks and fluids '
           'work like any GTCEu material, and JEI/EMI shows every form and recipe.\n\n'
           '## Steam-age materials\n\n| Material | Made of | Notes |\n|---|---|---|\n'
           '| Stronze | 1 Bronze + 2 Steel | blast furnace at 1,123 K; casings and pipes of the steam machines |\n'
           '| Breel | 2 Bronze + 1 Steel | no blast furnace: mixed by hand and smelted, as in GT: Not Leisure |\n'
           '| Clay Compound | Flint + Clay + Stone | plates and gears of the first hydraulic parts |\n'
           '| Compressed Steam | steam | solid steam for steam-age recipes |\n\n'
           'The supercritical steams that boost the [Void Miner SteamGate Aged](../systems/void-mining.md) are GTNA fluids too.\n\n'
           'Endgame materials (SpaceTime, Universium, MagMatter, White and Black Dwarf Matter…) have animated icons; '
           'see [Item effects](../systems/item-effects.md).\n\n## All materials\n\n| Material | ID |\n|---|---|\n'),
    'pt': ('# Materiais\n\nO GTNA registra **{n} materiais** como materiais do GTCEu no namespace `gtna`. Os itens, blocos e fluidos '
           'deles funcionam como qualquer material do GTCEu, e o JEI/EMI mostra todas as formas e receitas.\n\n'
           '## Materiais da era do vapor\n\n| Material | Feito de | Observações |\n|---|---|---|\n'
           '| Stronze | 1 Bronze + 2 Aço | alto-forno a 1.123 K; casings e canos das máquinas a vapor |\n'
           '| Breel | 2 Bronze + 1 Aço | sem alto-forno: misturado à mão e fundido, como no GT: Not Leisure |\n'
           '| Composto de Argila | Sílex + Argila + Pedra | placas e engrenagens das primeiras peças hidráulicas |\n'
           '| Vapor Comprimido | vapor | vapor sólido para receitas da era do vapor |\n\n'
           'Os vapores supercríticos que aceleram o [Portão a Vapor Envelhecido do Minerador do Vazio](../systems/void-mining.md) também são fluidos do GTNA.\n\n'
           'Os materiais de fim de jogo (Espaço-Tempo, Universium, Magmatéria, Matéria de Anã Branca e Negra…) têm ícones animados; '
           'veja [Efeitos de item](../systems/item-effects.md).\n\n## Todos os materiais\n\n| Material | ID |\n|---|---|\n'),
    'zh': ('# 材料\n\nGTNA 在 `gtna` 命名空间中注册了 **{n} 种材料**，它们都是 GTCEu 材料。其物品、方块和流体与任何 GTCEu 材料一样使用，'
           'JEI/EMI 会显示所有形态和配方。\n\n'
           '## 蒸汽时代材料\n\n| 材料 | 组成 | 说明 |\n|---|---|---|\n'
           '| 强铜 | 1 青铜 + 2 钢 | 1,123 K 高炉冶炼；蒸汽机器的外壳和管道 |\n'
           '| 布雷尔合金 | 2 青铜 + 1 钢 | 不需要高炉：手工混合后熔炼，与 GT: Not Leisure 相同 |\n'
           '| 粘土化合物 | 燧石 + 黏土 + 石头 | 最初液压部件的板和齿轮 |\n'
           '| 压缩蒸汽 | 蒸汽 | 用于蒸汽时代配方的固态蒸汽 |\n\n'
           '为[古旧蒸汽门虚空采矿机](../systems/void-mining.md)提供加成的超临界蒸汽也是 GTNA 流体。\n\n'
           '终局材料（时空、宇宙素、磁物质、白矮星与黑矮星物质……）拥有动态图标；见[物品特效](../systems/item-effects.md)。\n\n'
           '## 全部材料\n\n| 材料 | ID |\n|---|---|\n'),
}


def strip(s): return re.sub(r'§.', '', s)


def main():
    for code, table, suffix in (('en', EN, '.md'), ('pt', PT, '.pt.md'), ('zh', ZH, '.zh.md')):
        rows = sorted(((strip(table.get('material.gtna.' + m) or EN['material.gtna.' + m]), m) for m in IDS), key=lambda r: r[0].lower())
        md = INTRO[code].format(n=f'{len(IDS):,}'.replace(',', '.') if code == 'pt' else len(IDS))
        md += ''.join(f'| {name} | `gtna:{mid}` |\n' for name, mid in rows)
        if code == 'zh': md = zh_punct.fix(md)
        open(os.path.join(OUT, 'index' + suffix), 'w', encoding='utf-8').write(md)
    print('materials', len(IDS))


if __name__ == '__main__':
    main()
