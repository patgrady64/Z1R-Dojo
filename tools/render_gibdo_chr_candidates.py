#!/usr/bin/env python3
"""
Render the tiles requested by Gibdo from each regular enemy CHR pack.

Gibdo requests:
    left tile  $A4
    right tile $A6

The regular packs begin at PPU tile $9E, so these correspond to:
    $A4 - $9E = source index $06
    $A6 - $9E = source index $08

Outputs three enlarged BMP files in research/.
No external Python packages are required.
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

TILE_SIZE = 16
LEFT_TILE_INDEX = 0x06
RIGHT_TILE_INDEX = 0x08

SCALE = 12
GAP = 2

# Grayscale values for NES 2bpp pixels.
PALETTE = [
    (255, 255, 255),
    (170, 170, 170),
    (85, 85, 85),
    (0, 0, 0),
]


def decode_tile(tile: bytes) -> list[list[int]]:
    if len(tile) != TILE_SIZE:
        raise ValueError(f"Expected 16 tile bytes, found {len(tile)}")

    pixels: list[list[int]] = []

    for row in range(8):
        plane_0 = tile[row]
        plane_1 = tile[row + 8]
        pixel_row: list[int] = []

        for column in range(8):
            mask = 0x80 >> column

            low_bit = 1 if plane_0 & mask else 0
            high_bit = 1 if plane_1 & mask else 0

            pixel_row.append(low_bit | (high_bit << 1))

        pixels.append(pixel_row)

    return pixels


def combine_tiles(
    left: list[list[int]],
    right: list[list[int]],
) -> list[list[int]]:
    combined: list[list[int]] = []

    for row in range(8):
        combined.append(
            left[row]
            + [0] * GAP
            + right[row]
        )

    return combined


def scale_pixels(pixels: list[list[int]]) -> list[list[int]]:
    result: list[list[int]] = []

    for row in pixels:
        scaled_row: list[int] = []

        for pixel in row:
            scaled_row.extend([pixel] * SCALE)

        for _ in range(SCALE):
            result.append(list(scaled_row))

    return result


def write_bmp(path: Path, pixels: list[list[int]]) -> None:
    height = len(pixels)
    width = len(pixels[0])

    row_size = (width * 3 + 3) & ~3
    pixel_data_size = row_size * height
    file_size = 54 + pixel_data_size

    with path.open("wb") as bmp:
        # BITMAPFILEHEADER
        bmp.write(b"BM")
        bmp.write(struct.pack("<I", file_size))
        bmp.write(struct.pack("<HH", 0, 0))
        bmp.write(struct.pack("<I", 54))

        # BITMAPINFOHEADER
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

        # BMP rows are stored bottom-up.
        for row in reversed(pixels):
            for pixel in row:
                red, green, blue = PALETTE[pixel]
                bmp.write(bytes((blue, green, red)))

            bmp.write(padding)


def load_tile(data: bytes, index: int) -> bytes:
    start = index * TILE_SIZE
    end = start + TILE_SIZE
    return data[start:end]


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for pack_name, filename in PACKS.items():
        path = DATA_DIR / filename
        data = path.read_bytes()

        left = decode_tile(load_tile(data, LEFT_TILE_INDEX))
        right = decode_tile(load_tile(data, RIGHT_TILE_INDEX))

        combined = combine_tiles(left, right)
        enlarged = scale_pixels(combined)

        output = OUTPUT_DIR / f"gibdo_candidate_{pack_name}.bmp"
        write_bmp(output, enlarged)

        print(f"Pack {pack_name}: {output}")

    print()
    print("Open the three BMP files and identify which looks like Gibdo.")


if __name__ == "__main__":
    main()