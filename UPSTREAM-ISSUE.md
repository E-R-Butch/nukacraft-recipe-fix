# [NukaCraft] 74 broken recipes & tags in 1.19.10-alpha (1.21.1 NeoForge) — full analysis + working datapack

Hi NukaCraft team — love the mod, we run it on our community server. While deploying
`1.19.10-alpha` on a dedicated NeoForge 1.21.1 server we hit **74 recipe/tag load
errors on every boot**. We did a full forensic pass on the published jar and built a
datapack that fixes all of them, so this issue is equal parts bug report, root-cause
analysis, and a ready-made patch source.

**TL;DR**: boot ERROR lines 78 → 3, loaded recipes 10577 → 10651 with our datapack.
Fixing the data files upstream should be mostly mechanical — details below.

## Root causes (verified against the 1.19.10-alpha jar)

1. **Recipes still use the pre-1.20.5 format.** In 1.21.1, `result` must be
   `{"id": "..."}` (ItemStack codec), but ~46 recipes still say `{"item": "..."}`;
   stone-cutting recipes still use a bare string result.
2. **`ntgl:workbench` materials need the new ingredient wrapper.** Entries like
   `{"item": "nukacraft:scrap", "count": 10}` must become
   `{"ingredient": {"item": "nukacraft:scrap"}, "count": 10}` — 5 recipes affected
   (pipepistol, piperevolver, shiv, wrench, combatknife).
3. **Renamed ids never updated in data.** The joshua set was renamed in code but not
   in the recipe JSONs:
   - `joshua_planks` → `joshua_tree_planks`
   - `joshua_planks_slab` → `joshua_tree_planks_slab`
   - `joshua_planks_stairs` → `joshua_tree_planks_stairs`
   - `joshua_fence` → `joshua_tree_planks_fence`
   - `joshua_fence_gate` → `joshua_tree_planks_gate`
   - `joshua_pressure_plate` → `joshua_tree_pressure_plate`
   - `joshua_trapdoor` → `joshua_tree_trapdoor`
   - `joshua_door` → `joshua_tree_door`
   - `joshuatree_log` → `joshua_tree_log`, `joshuatree_block` → `joshua_tree_wood`
   - `stripped_joshuatree_log` → `stripped_joshua_tree_log` (same for `_wood`)
4. **Colored steels lost their underscores in data.** Recipes reference
   `whitesteel`, `greensteelslab`, `blacksteel_stairs` … but the registry has
   `white_steel`, `green_steel_slab`, `black_steel_stairs`, etc. (~20 refs)
5. **Recipes for content that no longer exists** (result item registered nowhere in
   the jar): `wrench`, `threads`, `combatknife`, `slicetile`, `vis_mas` (wants
   `scrapmetall`), `fertilizer` (wants `brahmin_goo`), `blacksteel2`,
   `recycle_rustedredsteel`, `recycle_rustedgreensteel`, `recycle_platedgreensteel`
   (`rustedred_steel`/`rustedgreen_steel`/`platedgreensteel` are all unregistered).
   We **disable** these with an always-empty tag ingredient rather than remap.
6. **Ghost-only tag**: `data/nukacraft/tags/banner_pattern/pattern_item/bos.json`
   references `nukacraft:bos`, registered nowhere.
7. **`minecraft:placeable`** gets 3 ghost refs (`nukacola`, `quantcola`,
   `sugar_bomb_promo`). This one can't be fixed from a datapack (vanilla tags are
   additive-only); the data files need to stop referencing deleted items.

One tiny extra: `cooking/aster_tea` defines key symbol `3` that the pattern never
uses — the strict parser rejects it.

## The datapack

We published the working fix (world datapack, overrides data only, no code changes,
removable any time) plus the generator script that produced it:
https://github.com/E-R-Butch/nukacraft-recipe-fix

Feel free to lift any of the fixed JSONs directly into the mod's
`src/main/resources/data/` — that's the whole point of publishing it.

## Repro

Fresh 1.21.1 NeoForge 21.1.248 dedicated server, NukaCraft 1.19.10-alpha + NTGL
3.2.0 + GeckoLib 4.9.3, boot, then `grep -c 'Parsing error loading recipe'
logs/latest.log` → 74. Full signature list available on request.

Thanks for the great mod — happy to test a fixed build on our server any time.
