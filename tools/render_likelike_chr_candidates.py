#!/usr/bin/env python3
"""
Render Like Like's four animation frames from each original
regular-enemy CHR pack.

Like Like uses original left-side frame tiles:

    $A6, $A4, $A2, $A4

Each displayed 16x16 frame consists of four 8x8 tiles:

    base + 0    base + 2
    base + 1    base + 3

Outputs:
    research/likelike_candidate_127.bmp
    research/likelike_candidate_358.bmp
    research/likelike_candidate_469.bmp
"""

from __future__ import annotations

import struct
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "bin" / "dat"
OUTPUT_DIR = ROOT / "research"

PACKS = {
    "127": "PatternBlockUWSP127.dat",
    "358": "PatternBlockUWSP358.dat",
    "469": "PatternBlockUWSP469.dat",
}

PACK_BASE_TILE = 0x9E
FRAME_BASE_TILES = [0xA6, 0xA4, 0xA2, 0xA4]

TILE_BYTES = 16
SCALE = 6
FRAME_GAP = 4

PALETTE = [
    (255, 255, 255),
    (170, 170, 170),
    (85, 85, 85),
    (0, 0, 0),
]


def read_tile(data: bytes, index: int) -> bytes:
    start = index * TILE_BYTES
    end = start + TILE_BYTES

    tile = data[start:end]

    if len(tile) != TILE_BYTES:
        raise ValueError(f"Could not read tile index ${index:02X}")

    return tile


def decode_tile(tile: bytes) -> list[list[int]]:
    pixels: list[list[int]] = []

    for row in range(8):
        plane_0 = tile[row]
        plane_1 = tile[row + 8]
        output_row: list[int] = []

        for column in range(8):
            mask = 0x80 >> column

            low = 1 if plane_0 & mask else 0
            high = 1 if plane_1 & mask else 0

            output_row.append(low | (high << 1))

        pixels.append(output_row)

    return pixels


def render_frame(data: bytes, base_tile: int) -> list[list[int]]:
    source_index = base_tile - PACK_BASE_TILE

    top_left = decode_tile(read_tile(data, source_index))
    bottom_left = decode_tile(read_tile(data, source_index + 1))
    top_right = decode_tile(read_tile(data, source_index + 2))
    bottom_right = decode_tile(read_tile(data, source_index + 3))

    frame: list[list[int]] = []

    for row in range(8):
        frame.append(top_left[row] + top_right[row])

    for row in range(8):
        frame.append(bottom_left[row] + bottom_right[row])

    return frame


def make_contact_sheet(frames: list[list[list[int]]]) -> list[list[int]]:
    height = 16
    width = len(frames) * 16 + (len(frames) - 1) * FRAME_GAP

    sheet = [[0 for _ in range(width)] for _ in range(height)]

    x_offset = 0

    for frame in frames:
        for y in range(16):
            for x in range(16):
                sheet[y][x_offset + x] = frame[y][x]

        x_offset += 16 + FRAME_GAP

    return sheet


def enlarge(pixels: list[list[int]]) -> list[list[int]]:
    enlarged: list[list[int]] = []

    for row in pixels:
        scaled_row: list[int] = []

        for pixel in row:
            scaled_row.extend([pixel] * SCALE)

        for _ in range(SCALE):
            enlarged.append(list(scaled_row))

    return enlarged


def write_bmp(path: Path, pixels: list[list[int]]) -> None:
    height = len(pixels)
    width = len(pixels[0])

    row_size = (width * 3 + 3) & ~3
    pixel_data_size = row_size * height
    file_size = 54 + pixel_data_size

    with path.open("wb") as bmp:
        bmp.write(b"BM")
        bmp.write(struct.pack("<I", file_size))
        bmp.write(struct.pack("<HH", 0, 0))
        bmp.write(struct.pack("<I", 54))

        bmp.write(struct.pack("<I", 40))
        bmp.write(struct.pack("<i", width))
        bmp.write(struct.pack("<i", height))
        bmp.write(struct.pack("<H", 1))
        bmp.write(struct.pack("<H", 24))
        bmp.write(struct.pack("<I", 0))
        bmp.write(struct.pack("<I", pixel_data_size))
        bmp.write(struct.pack("<i", 2835))
        bmp.write(struct.pack("<i", 2835))
        bmp.write(struct.pack("<I", 0))
        bmp.write(struct.pack("<I", 0))

        padding = bytes(row_size - width * 3)

        for row in reversed(pixels):
            for pixel in row:
                red, green, blue = PALETTE[pixel]
                bmp.write(bytes((blue, green, red)))

            bmp.write(padding)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for pack_name, filename in PACKS.items():
        path = DATA_DIR / filename

        if not path.exists():
            raise FileNotFoundError(path)

        data = path.read_bytes()

        frames = [
            render_frame(data, base_tile)
            for base_tile in FRAME_BASE_TILES
        ]

        contact_sheet = make_contact_sheet(frames)
        enlarged = enlarge(contact_sheet)

        output = OUTPUT_DIR / f"likelike_candidate_{pack_name}.bmp"
        write_bmp(output, enlarged)

        print(f"Pack {pack_name}: {output}")

    print()
    print("Open all three files and identify the Like Like animation.")


if __name__ == "__main__":
    main()