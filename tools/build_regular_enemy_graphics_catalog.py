"""Build the Z1 Dojo regular-enemy graphics research catalog.

This is a read-only research tool. It parses the current disassembly and writes:

    research/regular-enemy-graphics-catalog.csv
    research/regular-enemy-graphics-catalog.md

The report separates objects into four useful scopes:

- underworld specialized: uses the three level-specific enemy CHR packs and may
  require relocation into Z1 Dojo's unified bank;
- underworld common: uses the always-loaded common underworld sprite block and
  normally requires no unified-bank relocation;
- overworld: valid enemies, but outside the current dungeon-combat milestone;
- boss/helper/special: outside the regular-enemy milestone.

Automatically extracted fields:
- object type and update routine from UpdateObject_JumpTable;
- generic animation index (object type + 1);
- ObjAnimations heap offset;
- first frame tile from ObjAnimFrameHeap;
- an upper-bound heap window ending at the next animation start;
- unified-bank tile candidates when DojoRegularChrMap.inc exists.

The script preserves manually completed research columns from an existing CSV.
"""

from __future__ import annotations

import csv
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "src"
RESEARCH_DIR = ROOT / "research"

Z01_PATH = SRC_DIR / "Z_01.asm"
Z07_PATH = SRC_DIR / "Z_07.asm"
MAP_PATH = SRC_DIR / "DojoRegularChrMap.inc"

CSV_PATH = RESEARCH_DIR / "regular-enemy-graphics-catalog.csv"
MD_PATH = RESEARCH_DIR / "regular-enemy-graphics-catalog.md"

PACK_BASE_TILE = 0x9E

# Confirmed through Z1 Dojo in-game mixed-graphics tests.
CONFIRMED_PACKS: dict[int, str] = {
    0x17: "469",  # Like Like
    0x2A: "127",  # Stalfos
    0x30: "358",  # Gibdo
}

CONFIRMED_NAMES: dict[int, str] = {
    0x17: "Like Like",
    0x2A: "Stalfos",
    0x30: "Gibdo",
}

# Underworld enemies whose graphics come from one of the three specialized
# regular-enemy packs loaded at PPU tiles $9E-$BF in the stock game.
UNDERWORLD_SPECIALIZED_TYPES: set[int] = {
    0x05, 0x06,       # Goriya variants
    0x0B, 0x0C,       # Darknut variants
    0x12,             # Vire
    0x13,             # Zol
    0x16,             # Pols Voice
    0x17,             # Like Like
    0x23, 0x24,       # Wizzrobe variants
    0x27,             # Wallmaster
    0x28,             # Rope
    0x2A,             # Stalfos
    0x30,             # Gibdo
}

# Underworld enemies whose graphics live in the always-loaded common
# underworld sprite block at PPU tiles $8E-$9D.
UNDERWORLD_COMMON_TYPES: set[int] = {
    0x14, 0x15,       # Gel variants
    0x1B, 0x1C, 0x1D, # Keese variants
    0x2B, 0x2C, 0x2D, # Bubble variants
}

# Ordinary overworld enemy types. They remain in the catalog for completeness
# but are outside the current dungeon-combat graphics milestone.
OVERWORLD_ENEMY_TYPES: set[int] = {
    0x01, 0x02,       # Lynel variants
    0x03, 0x04,       # Moblin variants
    0x07, 0x08, 0x09, 0x0A,  # Octorock variants
    0x0D, 0x0E,       # Tektite / boulder variants
    0x0F, 0x10,       # Leever variants
    0x11,             # Zora
    0x1A,             # Peahat
    0x1E,             # Armos
    0x21, 0x22,       # Ghini variants
}

# Objects in the pre-boss range that are not ordinary selectable combat enemies.
NONREGULAR_PRE_BOSS_TYPES: dict[int, str] = {
    0x00: "empty/none",
    0x18: "Digdogger boss form",
    0x19: "unused/do-nothing",
    0x1F: "boulder-set controller",
    0x20: "boulder/environment object",
    0x25: "Patra child",
    0x26: "Patra child",
    0x29: "unused/do-nothing",
    0x2E: "whirlwind",
    0x2F: "pond fairy",
}

# Object type $31 begins the boss/special section in the stock table.
FIRST_BOSS_TYPE = 0x31

MANUAL_FIELDS = [
    "full_frame_count",
    "original_frame_tiles",
    "unified_frame_tiles",
    "projectile_or_child_dependencies",
    "palette_requirements",
    "special_draw_behavior",
    "verified_in_game",
    "notes",
]


@dataclass(frozen=True)
class CatalogRow:
    object_type: int
    update_routine: str
    display_name: str
    category: str
    status: str
    generic_animation_index: int | None
    animation_heap_offset: int | None
    first_frame_tile: int | None
    heap_window_length: int | None
    confirmed_pack: str
    unified_first_tile: int | None
    pack_127_candidate: int | None
    pack_358_candidate: int | None
    pack_469_candidate: int | None
    notes: str


def read_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Missing required source file: {path}")
    return path.read_text(encoding="utf-8")


def extract_table_lines(text: str, label: str, directive: str) -> list[str]:
    """Extract consecutive directive operands after a ca65 label."""
    lines = text.splitlines()
    label_pattern = re.compile(rf"^\s*{re.escape(label)}:\s*$")
    directive_pattern = re.compile(rf"^\s*\.{re.escape(directive)}\s+(.+?)\s*$", re.I)

    start_index: int | None = None
    for index, line in enumerate(lines):
        if label_pattern.match(line):
            start_index = index + 1
            break

    if start_index is None:
        raise ValueError(f"Could not find label {label}: in source")

    operands: list[str] = []
    for line in lines[start_index:]:
        stripped = line.strip()

        if not stripped or stripped.startswith(";"):
            if operands:
                continue
            continue

        match = directive_pattern.match(line)
        if match:
            operands.append(match.group(1))
            continue

        break

    if not operands:
        raise ValueError(f"No .{directive} entries found after {label}:")

    return operands


def parse_addr_table(text: str, label: str) -> list[str]:
    operands = extract_table_lines(text, label, "ADDR")
    values: list[str] = []

    for operand_line in operands:
        code = operand_line.split(";", 1)[0]
        for operand in code.split(","):
            value = operand.strip()
            if value:
                values.append(value)

    return values


def parse_byte_table(text: str, label: str) -> list[int]:
    operands = extract_table_lines(text, label, "BYTE")
    values: list[int] = []

    for operand_line in operands:
        code = operand_line.split(";", 1)[0]
        for operand in code.split(","):
            token = operand.strip()
            if not token:
                continue

            if token.startswith("$"):
                values.append(int(token[1:], 16))
            elif token.startswith("%"):
                values.append(int(token[1:], 2))
            elif token.isdigit():
                values.append(int(token, 10))
            else:
                raise ValueError(
                    f"Unsupported byte token {token!r} in table {label}"
                )

    return values


def parse_optional_maps(text: str | None) -> dict[str, list[int]]:
    if text is None:
        return {}

    maps: dict[str, list[int]] = {}
    for pack in ("127", "358", "469"):
        label = f"DojoRegularChrMap{pack}"
        try:
            maps[pack] = parse_byte_table(text, label)
        except ValueError:
            continue

    return maps


def split_camel_case(name: str) -> str:
    name = re.sub(r"^Update", "", name)
    name = name.replace("_", " ")
    name = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", name)
    name = re.sub(r"(?<=[A-Z])(?=[A-Z][a-z])", " ", name)
    return " ".join(name.split()) or "Unknown"


def build_display_names(routines: list[str]) -> list[str]:
    totals = Counter(routines)
    seen: Counter[str] = Counter()
    names: list[str] = []

    for object_type, routine in enumerate(routines):
        if object_type in CONFIRMED_NAMES:
            names.append(CONFIRMED_NAMES[object_type])
            seen[routine] += 1
            continue

        base = split_camel_case(routine)
        seen[routine] += 1

        if totals[routine] > 1:
            names.append(f"{base} variant {seen[routine]}")
        else:
            names.append(base)

    return names


def category_for(object_type: int) -> tuple[str, str, str]:
    if object_type in CONFIRMED_PACKS:
        return (
            "underworld specialized",
            "proven",
            "Graphics pack and unified rendering verified in-game.",
        )

    if object_type in UNDERWORLD_SPECIALIZED_TYPES:
        return (
            "underworld specialized",
            "relocation research needed",
            "Confirm original pack, full frame set, palette, and dependencies.",
        )

    if object_type in UNDERWORLD_COMMON_TYPES:
        return (
            "underworld common",
            "already compatible",
            "Uses the always-loaded common underworld sprite block; verify behavior and dependencies only.",
        )

    if object_type in OVERWORLD_ENEMY_TYPES:
        return (
            "overworld",
            "outside current scope",
            "Valid overworld enemy; retained for future expansion.",
        )

    if object_type in NONREGULAR_PRE_BOSS_TYPES:
        return (
            "boss/helper/special",
            "outside current scope",
            NONREGULAR_PRE_BOSS_TYPES[object_type],
        )

    if object_type >= FIRST_BOSS_TYPE:
        return (
            "boss/helper/special",
            "outside current scope",
            "Retained for dispatch-table completeness.",
        )

    return (
        "boss/helper/special",
        "needs classification",
        "Pre-boss object not yet classified.",
    )


def next_distinct_start(starts: list[int], current: int, heap_len: int) -> int:
    greater = [value for value in set(starts) if value > current]
    return min(greater) if greater else heap_len


def translate_candidate(
    original_tile: int | None,
    mapping: list[int] | None,
) -> int | None:
    if original_tile is None or mapping is None:
        return None

    source_index = original_tile - PACK_BASE_TILE
    if source_index < 0 or source_index >= len(mapping):
        return None

    return mapping[source_index]


def build_rows(
    routines: list[str],
    obj_animations: list[int],
    frame_heap: list[int],
    maps: dict[str, list[int]],
) -> list[CatalogRow]:
    display_names = build_display_names(routines)
    rows: list[CatalogRow] = []

    for object_type, routine in enumerate(routines):
        category, status, notes = category_for(object_type)

        animation_index = object_type + 1
        if animation_index >= len(obj_animations):
            animation_index_value: int | None = None
            heap_offset: int | None = None
            first_tile: int | None = None
            window_length: int | None = None
        else:
            animation_index_value = animation_index
            heap_offset = obj_animations[animation_index]

            if heap_offset >= len(frame_heap):
                first_tile = None
                window_length = None
                notes += " Animation heap offset is outside ObjAnimFrameHeap."
            else:
                first_tile = frame_heap[heap_offset]
                window_end = next_distinct_start(
                    obj_animations,
                    heap_offset,
                    len(frame_heap),
                )
                window_length = window_end - heap_offset

        candidates = {
            pack: translate_candidate(first_tile, maps.get(pack))
            for pack in ("127", "358", "469")
        }

        confirmed_pack = CONFIRMED_PACKS.get(object_type, "")
        unified_first = candidates.get(confirmed_pack) if confirmed_pack else None

        rows.append(
            CatalogRow(
                object_type=object_type,
                update_routine=routine,
                display_name=display_names[object_type],
                category=category,
                status=status,
                generic_animation_index=animation_index_value,
                animation_heap_offset=heap_offset,
                first_frame_tile=first_tile,
                heap_window_length=window_length,
                confirmed_pack=confirmed_pack,
                unified_first_tile=unified_first,
                pack_127_candidate=candidates["127"],
                pack_358_candidate=candidates["358"],
                pack_469_candidate=candidates["469"],
                notes=notes,
            )
        )

    return rows


def hex_or_blank(value: int | None, width: int = 2) -> str:
    return "" if value is None else f"${value:0{width}X}"


def md_code_or_dash(value: int | None, width: int = 2) -> str:
    return "—" if value is None else f"`{hex_or_blank(value, width)}`"


def load_manual_fields() -> dict[str, dict[str, str]]:
    if not CSV_PATH.exists():
        return {}

    preserved: dict[str, dict[str, str]] = {}

    with CSV_PATH.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for existing in reader:
            key = existing.get("object_type", "").strip().upper()
            if not key:
                continue
            preserved[key] = {
                field: existing.get(field, "")
                for field in MANUAL_FIELDS
            }

    return preserved


def write_csv(
    rows: list[CatalogRow],
    preserved_manual: dict[str, dict[str, str]],
) -> None:
    fields = [
        "object_type",
        "display_name",
        "update_routine",
        "category",
        "status",
        "generic_animation_index",
        "animation_heap_offset",
        "first_frame_tile",
        "heap_window_upper_bound",
        "confirmed_original_pack",
        "confirmed_unified_first_tile",
        "pack_127_first_tile_candidate",
        "pack_358_first_tile_candidate",
        "pack_469_first_tile_candidate",
        "full_frame_count",
        "original_frame_tiles",
        "unified_frame_tiles",
        "projectile_or_child_dependencies",
        "palette_requirements",
        "special_draw_behavior",
        "verified_in_game",
        "notes",
    ]

    with CSV_PATH.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fields)
        writer.writeheader()

        for row in rows:
            object_type_text = hex_or_blank(row.object_type)
            old = preserved_manual.get(object_type_text.upper(), {})

            verified = old.get("verified_in_game", "")
            if row.status == "proven":
                verified = "yes"

            old_notes = old.get("notes", "").strip()
            default_notes = row.notes.strip()
            notes = old_notes if old_notes and old_notes != default_notes else default_notes

            writer.writerow(
                {
                    "object_type": object_type_text,
                    "display_name": row.display_name,
                    "update_routine": row.update_routine,
                    "category": row.category,
                    "status": row.status,
                    "generic_animation_index": hex_or_blank(
                        row.generic_animation_index
                    ),
                    "animation_heap_offset": hex_or_blank(
                        row.animation_heap_offset
                    ),
                    "first_frame_tile": hex_or_blank(row.first_frame_tile),
                    "heap_window_upper_bound": (
                        ""
                        if row.heap_window_length is None
                        else str(row.heap_window_length)
                    ),
                    "confirmed_original_pack": row.confirmed_pack,
                    "confirmed_unified_first_tile": hex_or_blank(
                        row.unified_first_tile
                    ),
                    "pack_127_first_tile_candidate": hex_or_blank(
                        row.pack_127_candidate
                    ),
                    "pack_358_first_tile_candidate": hex_or_blank(
                        row.pack_358_candidate
                    ),
                    "pack_469_first_tile_candidate": hex_or_blank(
                        row.pack_469_candidate
                    ),
                    "full_frame_count": old.get("full_frame_count", ""),
                    "original_frame_tiles": old.get("original_frame_tiles", ""),
                    "unified_frame_tiles": old.get("unified_frame_tiles", ""),
                    "projectile_or_child_dependencies": old.get(
                        "projectile_or_child_dependencies", ""
                    ),
                    "palette_requirements": old.get("palette_requirements", ""),
                    "special_draw_behavior": old.get("special_draw_behavior", ""),
                    "verified_in_game": verified,
                    "notes": notes,
                }
            )


def append_table(lines: list[str], title: str, rows: list[CatalogRow]) -> None:
    lines.extend(
        [
            f"## {title}",
            "",
            "| Type | Enemy | Routine | Anim | Heap | First tile | Pack | Unified | Status |",
            "|---:|---|---|---:|---:|---:|---:|---:|---|",
        ]
    )

    for row in rows:
        lines.append(
            "| "
            f"`{hex_or_blank(row.object_type)}` | "
            f"{row.display_name} | "
            f"`{row.update_routine}` | "
            f"{md_code_or_dash(row.generic_animation_index)} | "
            f"{md_code_or_dash(row.animation_heap_offset)} | "
            f"{md_code_or_dash(row.first_frame_tile)} | "
            f"{row.confirmed_pack or '—'} | "
            f"{md_code_or_dash(row.unified_first_tile)} | "
            f"{row.status} |"
        )

    lines.append("")


def write_markdown(rows: list[CatalogRow], has_maps: bool) -> None:
    specialized_rows = [
        row for row in rows if row.category == "underworld specialized"
    ]
    common_rows = [row for row in rows if row.category == "underworld common"]
    overworld_rows = [row for row in rows if row.category == "overworld"]
    other_rows = [row for row in rows if row.category == "boss/helper/special"]
    proven_rows = [row for row in specialized_rows if row.status == "proven"]
    remaining_specialized = [
        row for row in specialized_rows if row.status != "proven"
    ]

    lines = [
        "# Z1 Dojo Regular Enemy Graphics Catalog",
        "",
        "Generated by `tools/build_regular_enemy_graphics_catalog.py`.",
        "",
        "## Summary",
        "",
        f"- Dispatch-table entries parsed: **{len(rows)}**",
        f"- Underworld specialized object types: **{len(specialized_rows)}**",
        f"- Underworld common object types: **{len(common_rows)}**",
        f"- Specialized entries proven in-game: **{len(proven_rows)}**",
        f"- Specialized entries still needing research: **{len(remaining_specialized)}**",
        f"- Overworld enemy object types outside current scope: **{len(overworld_rows)}**",
        f"- Boss/helper/special entries outside current scope: **{len(other_rows)}**",
        f"- Unified translation maps loaded: **{'yes' if has_maps else 'no'}**",
        "",
        "## Graphics Scope",
        "",
        "- **Underworld specialized:** original graphics are selected from one of the three level-specific regular-enemy packs. These entries may require relocation into the unified Z1 Dojo bank.",
        "- **Underworld common:** graphics use the always-loaded common underworld sprite block at PPU tiles `$8E-$9D`. These normally require no unified-bank relocation.",
        "- **Overworld:** valid enemies, retained for future expansion but excluded from the current dungeon-combat milestone.",
        "- **Boss/helper/special:** bosses, projectiles, controllers, environmental objects, and unused entries outside the regular-enemy milestone.",
        "",
        "## Important Interpretation Rule",
        "",
        "The generic renderer normally uses animation index `object type + 1`.",
        "The extracted heap offset and first frame tile are useful starting points, but they are not a complete dependency map. Some objects self-draw, select different animation indexes, spawn child objects, or use projectile graphics.",
        "",
        "The `heap window` is only the distance to the next distinct animation start. It is an upper bound, not a verified frame count.",
        "",
    ]

    append_table(lines, "Underworld Specialized — Relocation Scope", specialized_rows)
    append_table(lines, "Underworld Common — Already Compatible", common_rows)
    append_table(lines, "Overworld — Future Scope", overworld_rows)

    lines.extend(
        [
            "## Proven Mixed-Graphics Entries",
            "",
        ]
    )

    for row in proven_rows:
        lines.append(
            f"- `{hex_or_blank(row.object_type)}` **{row.display_name}**: "
            f"pack `{row.confirmed_pack}`, original first tile "
            f"{md_code_or_dash(row.first_frame_tile)}, unified first tile "
            f"{md_code_or_dash(row.unified_first_tile)}."
        )

    lines.extend(
        [
            "",
            "## Remaining Specialized Research",
            "",
            "The remaining relocation work is limited to these specialized entries:",
            "",
        ]
    )

    for row in remaining_specialized:
        lines.append(
            f"- `{hex_or_blank(row.object_type)}` **{row.display_name}**"
        )

    lines.extend(
        [
            "",
            "## Manual Research Fields",
            "",
            "For each underworld specialized entry, complete these CSV columns:",
            "",
            "1. `full_frame_count` and `original_frame_tiles`",
            "2. `confirmed_original_pack`",
            "3. `unified_frame_tiles`",
            "4. `projectile_or_child_dependencies`",
            "5. `palette_requirements`",
            "6. `special_draw_behavior`",
            "7. `verified_in_game`",
            "",
            "Existing values in these manual columns are preserved when the generator is rerun.",
            "",
        ]
    )

    MD_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    z01_text = read_text(Z01_PATH)
    z07_text = read_text(Z07_PATH)
    map_text = MAP_PATH.read_text(encoding="utf-8") if MAP_PATH.exists() else None

    routines = parse_addr_table(z07_text, "UpdateObject_JumpTable")
    obj_animations = parse_byte_table(z01_text, "ObjAnimations")
    frame_heap = parse_byte_table(z01_text, "ObjAnimFrameHeap")
    maps = parse_optional_maps(map_text)

    rows = build_rows(routines, obj_animations, frame_heap, maps)

    RESEARCH_DIR.mkdir(parents=True, exist_ok=True)
    preserved_manual = load_manual_fields()
    write_csv(rows, preserved_manual)
    write_markdown(rows, has_maps=bool(maps))

    specialized_count = sum(
        row.category == "underworld specialized" for row in rows
    )
    common_count = sum(row.category == "underworld common" for row in rows)
    remaining_count = sum(
        row.category == "underworld specialized" and row.status != "proven"
        for row in rows
    )

    print("Z1 Dojo regular-enemy graphics catalog generated.")
    print()
    print(f"Dispatch entries:               {len(routines)}")
    print(f"Underworld specialized entries: {specialized_count}")
    print(f"Underworld common entries:      {common_count}")
    print(f"Specialized entries remaining:  {remaining_count}")
    print(f"Translation maps found:         {len(maps)}")
    print()
    print(f"CSV:    {CSV_PATH.relative_to(ROOT)}")
    print(f"Report: {MD_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()