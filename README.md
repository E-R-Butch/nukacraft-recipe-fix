# NukaCraft 1.21.1 — Recipe & Tag Repair Datapack

Community fix for **NukaCraft: Fallout mod** `1.19.10-alpha` (NeoForge 1.21.1) plus one
**Create Deco** recipe. Repairs **74 broken recipes/tags** that spam the server log on
every boot and silently disable game content.

**Measured on our dedicated server: boot ERROR lines 78 → 3, loaded recipes 10577 → 10651.**

## What's broken upstream

NukaCraft 1.19.10-alpha shipped with data files that were never migrated to the
1.20.5+ recipe format, and a batch of item ids that were renamed in code but not in
data. Verified by inspecting the published jar:

| Root cause | Example | Count |
|---|---|---|
| Pre-1.20.5 result format | `"result": {"item": X}` must be `{"id": X}` in 1.21.1 | 46 |
| `ntgl:workbench` materials not wrapped | raw `{"item":...,"count":N}` entries instead of `{"ingredient":{...},"count":N}` | 5 |
| Renamed ids | `joshua_planks*` → `joshua_tree_planks*`, `joshuatree_log` → `joshua_tree_log` | 14 recipes |
| Mis-spelled ids (missing underscore) | `whitesteel` → `white_steel`, `whitesteel_slab` → `white_steel_slab`, etc. | ~20 ingredient refs |
| Recipes for content removed from the mod | `wrench`, `threads`, `combatknife`, `slicetile`, `vis_mas`, `fertilizer`, `blacksteel2`, `rusted*_steel`, `platedgreensteel` | 9 → disabled |
| Ghost-only banner-pattern tag | `nukacraft:pattern_item/bos` references `nukacraft:bos`, which is registered nowhere | 1 → emptied |
| Create Deco placard dye recipe | ingredient uses `{"id": "minecraft:white_dye"}` (1.21.1 ingredients want `item`/`tag`) | 1 |

Registry truth was established by scanning the mod jar's class-file string pool and
`assets/nukacraft/lang/en_us.json` — every remap in the datapack points at an id that
actually exists at runtime. Recipes whose *result* item no longer exists anywhere in
the jar (removed content) are **disabled** with an always-empty tag ingredient instead
of remapped, so they parse cleanly but can never be crafted.

The single remaining boot error, `Couldn't load tag minecraft:placeable ... missing
following references: nukacraft:nukacola, quantcola, sugar_bomb_promo`, is **not
fixable from data**: vanilla tags are merged additively and cannot be stripped without
shipping a full vanilla tag replacement, which would break on every MC update. The
upstream data files simply need to stop referencing deleted items.

## Using the datapack

1. Drop `nuka-fix-datapack.zip` into your world's `datapacks/` folder
   (server-side only; clients need nothing).
2. Run `/reload`, or restart the server.
3. Verify: `Loaded 10651 recipes` in the log and no `Parsing error loading recipe
   nukacraft:*` lines.

Remove the datapack any time to roll back — it only overrides data, never code, and
never touches your world save.

### What you get back

- Pipe revolver / pipe pistol, combat knife family, and every other NTGL workbench
  recipe that previously failed to parse
- Joshua tree wood set (planks, slab, stairs, fence, gate, door, trapdoor, pressure
  plate) and its crafting chain
- All colored-steel recycling recipes (`white_steel`, `green_steel`, `blue_steel`, ...)
- White-dye placard recipe from Create Deco

## Regenerating after a NukaCraft update

`nuka-fix-generator.py` rebuilds the datapack from whatever the current jar ships:

1. Pull the failing recipe list from your log:
   ```bash
   grep -oE 'Parsing error loading recipe [a-z_]+:[a-z0-9_/]+' logs/latest.log \
     | awk '{print $NF}' | sort -u > broken_recipes.txt
   ```
2. Point the script at the jars (`JAR` / deco jar path inside the script) and run it:
   `python3 nuka-fix-generator.py` → produces `nuka-datapack/`
3. Zip it, drop it in `world/datapacks/`, `/reload`.

The remap tables and the disable-list live at the top of the script and are easy to
extend when upstream adds new renames.

## Upstream status

- **Create Deco**: the identical fix is already open as
  [talrey/CreateDeco#271](https://github.com/talrey/CreateDeco/pull/271) (open since
  2026-06-05). Once merged, drop this datapack's `createdeco` entry.
- **NukaCraft**: the Modrinth-listed source repo (`DaytonCrips/nukacraft_mod`) is 404,
  so there is currently no PR channel — the issue text we prepared is in
  [`UPSTREAM-ISSUE.md`](UPSTREAM-ISSUE.md) for their Discord / Modrinth comments.

## License

CC0. Take it, fork it, ship it in your pack. No attribution required (but a link back
helps other server admins find the fix).
