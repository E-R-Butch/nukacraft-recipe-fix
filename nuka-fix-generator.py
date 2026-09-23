#!/usr/bin/env python3
"""Build the homelab NukaCraft/CreateDeco repair datapack (v2, registry-aware).

Sources of truth:
  - registry ids scraped from jar bytecode (class-file string scan)
  - lang-file ids as fallback
Fix strategies:
  REMAP   – item id spelling/rename fixes (joshua_* -> joshua_tree_*, [c]steel -> [c]_steel)
  DISABLE – recipes for content removed from the mod: overridden by a valid recipe
            whose only ingredient is an always-empty tag (parses, never craftable)
  FIX     – 1.20.5+ format migration (result.item -> result.id, ntgl materials wrap,
            ingredient.id -> ingredient.item, forge: -> c:)
  TAGS    – empty ghost-only tags (pattern_item/bos)
"""
import json, os, re, shutil, zipfile

JAR = '/tmp/nuka.jar'
BROKEN = '/tmp/broken_recipes.txt'
OUT = '/tmp/nuka-datapack'
EMPTY_TAG = 'homelab:never_matches'

z = zipfile.ZipFile(JAR)
names = set(z.namelist())

# ---- registry truth -------------------------------------------------------
lang = json.loads(z.read('assets/nukacraft/lang/en_us.json').decode())
valid = {'nukacraft:' + m.group(1) for k in lang
         if (m := re.match(r'(?:item|block)\.nukacraft\.([a-z0-9_]+)$', k))}
code = set()
for n in names:
    if n.endswith('.class'):
        for m in re.finditer(rb'[a-z][a-z0-9_]{2,44}', z.read(n)):
            code.add(m.group().decode())
valid |= {'nukacraft:' + s for s in code}
# vanilla/minecraft ids we rely on
valid |= {'minecraft:' + s for s in
          ('white_dye', 'item_frame', 'light_gray_concrete', 'scrap')}

# ---- fix tables -----------------------------------------------------------
JOSHUA_REMAP = {
    'joshua_planks': 'joshua_tree_planks',
    'joshua_planks_slab': 'joshua_tree_planks_slab',
    'joshua_planks_stairs': 'joshua_tree_planks_stairs',
    'joshua_planks_fence': 'joshua_tree_planks_fence',
    'joshua_fence': 'joshua_tree_planks_fence',
    'joshua_fence_gate': 'joshua_tree_planks_gate',
    'joshua_pressure_plate': 'joshua_tree_pressure_plate',
    'joshua_trapdoor': 'joshua_tree_trapdoor',
    'joshua_door': 'joshua_tree_door',
    'joshuatree_log': 'joshua_tree_log',
    'joshuatree_block': 'joshua_tree_wood',
    'stripped_joshuatree_log': 'stripped_joshua_tree_log',
    'stripped_joshuatree_block': 'stripped_joshua_tree_wood',
}
COLOR_STEEL = re.compile(r'^((?:white|black|blue|red|green|yellow|brown|cyan|gray|light_gray|orange|pink|purple)?)steel(.*)$')

def remap_id(iid):
    if not (isinstance(iid, str) and iid.startswith('nukacraft:')):
        return iid
    path = iid.split(':', 1)[1]
    if path in JOSHUA_REMAP:
        return 'nukacraft:' + JOSHUA_REMAP[path]
    m = COLOR_STEEL.match(path)
    if m and (m.group(1) or m.group(2)):
        cand = 'nukacraft:' + (m.group(1) + '_steel' if m.group(1) else 'steel') + m.group(2)
        if cand in valid:
            return cand
    if path == 'blacksteel2' and 'nukacraft:black_steel' in valid:
        return 'nukacraft:black_steel'
    return iid

DISABLE = {
    'nukacraft:wrench', 'nukacraft:vis_mas', 'nukacraft:slicetile',
    'nukacraft:fertilizer', 'nukacraft:combatknife', 'nukacraft:threads',
    'nukacraft:recycle/recycle_rustedredsteel',
    'nukacraft:recycle/recycle_rustedgreensteel',
    'nukacraft:recycle/recycle_platedgreensteel',
    'nukacraft:recycle/recycle_blacksteel2',
}

def walk_ids(obj):
    """Apply remap to every item/id value in the structure."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in ('item', 'id') and isinstance(v, str):
                obj[k] = remap_id(v)
            else:
                walk_ids(v)
    elif isinstance(obj, list):
        for v in obj:
            walk_ids(v)

def fix_recipe(rid, data):
    changes = []
    if isinstance(data, dict):
        if data.get('type') == 'ntgl:workbench' and isinstance(data.get('materials'), list):
            mats = []
            for mat in data['materials']:
                if isinstance(mat, dict) and 'ingredient' not in mat:
                    cnt = mat.get('count', 1)
                    ing = {k: v for k, v in mat.items() if k != 'count'}
                    mats.append({'ingredient': ing, 'count': cnt})
                    changes.append('materials-wrap')
                else:
                    mats.append(mat)
            data['materials'] = mats
        for field in ('key', 'ingredients', 'materials'):
            walk_ids(data.get(field)) if isinstance(data.get(field), (dict, list)) else None
        if isinstance(data.get('ingredient'), dict):
            walk_ids(data['ingredient'])
        walk_ids(data.get('result'))
        r = data.get('result')
        if isinstance(r, str):
            data['result'] = {'id': remap_id(r)}
            changes.append('result:str->obj')
        elif isinstance(r, dict) and 'item' in r and 'id' not in r:
            data['result'] = {'id': r['item'], **{k: v for k, v in r.items() if k != 'item'}}
            changes.append('result:item->id')
        for ing in data.get('ingredients', []) if isinstance(data.get('ingredients'), list) else []:
            if isinstance(ing, dict) and 'id' in ing and 'item' not in ing and 'tag' not in ing:
                ing['item'] = ing.pop('id')
                changes.append('ing:id->item')
        txt = json.dumps(data)
        if '"forge:' in txt:
            data = json.loads(txt.replace('"forge:', '"c:'))
            changes.append('forge->c')
    return data, changes

def disabled_recipe():
    return {
        'type': 'minecraft:crafting_shapeless',
        'ingredients': [{'tag': EMPTY_TAG}],
        'result': {'id': 'nukacraft:scrap', 'count': 1},
    }

broken = [l.strip() for l in open(BROKEN) if l.strip()]
shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(OUT + '/data', exist_ok=True)
json.dump({'pack': {'pack_format': 48,
            'description': 'Homelab fix: NukaCraft/CreateDeco 1.21.1 recipe+tag repair (registry-aware)'}},
          open(OUT + '/pack.mcmeta', 'w'))

report = []
for rid in broken:
    ns, _, path = rid.partition(':')
    cands = (f'data/{ns}/recipe/{path}.json', f'data/{ns}/recipes/{path}.json')
    src = next((p for p in cands if p in names), None)
    if rid in DISABLE or rid == 'nukacraft:combatknife' or rid == 'nukacraft:threads':
        data, changes = disabled_recipe(), ['DISABLED(empty-tag)']
    elif src is None:
        if ns == 'createdeco':
            zd = zipfile.ZipFile('/tmp/deco.jar')
            data = json.loads(zd.read(f'data/createdeco/recipe/{path}.json').decode())
            for ing in data.get('ingredients', []):
                if isinstance(ing, dict) and 'id' in ing and 'item' not in ing and 'tag' not in ing:
                    ing['item'] = ing.pop('id')
            changes = ['deco:ing:id->item']
        else:
            report.append((rid, 'SOURCE NOT FOUND', ''))
            continue
    else:
        data, changes = fix_recipe(rid, json.loads(z.read(src).decode()))
    # aster_tea: drop unused key symbols
    if isinstance(data, dict) and 'pattern' in data and 'key' in data:
        used = {s for row in data['pattern'] for s in row}
        unused = [k for k in data['key'] if k not in used]
        for k in unused:
            del data['key'][k]
        if unused:
            changes.append(f'dropped-unused-key:{"".join(unused)}')
    dst = f'{OUT}/data/{ns}/recipe/{path}.json'
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    json.dump(data, open(dst, 'w'), indent=1)
    report.append((rid, 'OK', ','.join(changes) or 'no-change'))

# empty tag used by disabled recipes + bos tag cleanup
tagdir = OUT + '/data/homelab/tags/item'
os.makedirs(tagdir, exist_ok=True)
json.dump({'replace': True, 'values': []}, open(tagdir + '/never_matches.json', 'w'))
bosdir = OUT + '/data/nukacraft/tags/banner_pattern/pattern_item'
os.makedirs(bosdir, exist_ok=True)
json.dump({'replace': True, 'values': []}, open(bosdir + '/bos.json', 'w'))

ok = sum(1 for r in report if r[1] == 'OK')
print(f'recipes written: {ok}/{len(broken)}')
for rid, st, ch in report:
    if st != 'OK' or not ch or 'DISABLED' in ch:
        print(f'{st:18s} {rid:46s} {ch}')
