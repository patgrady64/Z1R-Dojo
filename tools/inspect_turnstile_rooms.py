from pathlib import Path
from typing import Final

ROOM_COUNT: Final = 0x80
TABLE_COUNT: Final = 6
EXPECTED_SIZE: Final = ROOM_COUNT * TABLE_COUNT

TURNSTYLE_GEOMETRY: Final = 0x20
COMBAT_SLOT_ROOM: Final = 0x63

FILES = [
    ("1Q Levels 1-6", Path("bin/dat/LevelBlockUW1Q1.dat")),
    ("1Q Levels 7-9", Path("bin/dat/LevelBlockUW2Q1.dat")),
    ("2Q Levels 1-6", Path("bin/dat/LevelBlockUW1Q2.dat")),
    ("2Q Levels 7-9", Path("bin/dat/LevelBlockUW2Q2.dat")),
]

DOOR_NAMES = {
    0: "Open",
    1: "Wall",
    2: "Walk-through 1",
    3: "Walk-through 2",
    4: "Bombable",
    5: "Locked 1",
    6: "Locked 2",
    7: "Shutter",
}


def get_room_record(data: bytes, room_id: int) -> tuple[int, ...]:
    """Return attributes A-F for one room."""
    return tuple(
        data[(table_number * ROOM_COUNT) + room_id]
        for table_number in range(TABLE_COUNT)
    )


def describe_room(room_id: int, record: tuple[int, ...], prefix: str) -> str:
    a, b, c, d, e, f = record

    north = (a >> 5) & 0x07
    south = (a >> 2) & 0x07
    west = (b >> 5) & 0x07
    east = (b >> 2) & 0x07

    geometry = d & 0x3F
    push_block = bool(d & 0x40)

    enemy_id = c & 0x3F
    if d & 0x80:
        enemy_id |= 0x40

    enemy_count_index = (c >> 6) & 0x03
    room_item = e & 0x1F
    secret_trigger = f & 0x07

    return (
        f"{prefix} room ${room_id:02X}\n"
        f"  Raw: A=${a:02X} B=${b:02X} C=${c:02X} "
        f"D=${d:02X} E=${e:02X} F=${f:02X}\n"
        f"  Geometry:       ${geometry:02X}\n"
        f"  Push-block bit: {'YES' if push_block else 'no'}\n"
        f"  Enemy ID:       ${enemy_id:02X}\n"
        f"  Count index:    {enemy_count_index}\n"
        f"  Room item:      ${room_item:02X}\n"
        f"  Secret trigger: ${secret_trigger:02X}\n"
        f"  Doors:\n"
        f"    North: {DOOR_NAMES[north]}\n"
        f"    East:  {DOOR_NAMES[east]}\n"
        f"    South: {DOOR_NAMES[south]}\n"
        f"    West:  {DOOR_NAMES[west]}"
    )


def inspect_file(label: str, path: Path) -> None:
    print()
    print("=" * 72)
    print(label)
    print(path)
    print("=" * 72)

    if not path.exists():
        print("FILE NOT FOUND")
        print("Run the ROM build first so the extracted bin/dat files exist.")
        return

    data = path.read_bytes()

    if len(data) != EXPECTED_SIZE:
        print(
            f"Unexpected file size: {len(data)} bytes; "
            f"expected {EXPECTED_SIZE} bytes."
        )
        return

    turnstyle_rooms: list[int] = []

    for room_id in range(ROOM_COUNT):
        record = get_room_record(data, room_id)

        if (record[3] & 0x3F) == TURNSTYLE_GEOMETRY:
            turnstyle_rooms.append(room_id)
            print(describe_room(room_id, record, "TURNSTYLE SOURCE"))
            print()

    if not turnstyle_rooms:
        print("No rooms using Turnstyle geometry were found in this block.")
        print()

    combat_record = get_room_record(data, COMBAT_SLOT_ROOM)
    print(describe_room(COMBAT_SLOT_ROOM, combat_record, "COMBAT SLOT"))
    print()


def main() -> None:
    for label, path in FILES:
        inspect_file(label, path)


if __name__ == "__main__":
    main()