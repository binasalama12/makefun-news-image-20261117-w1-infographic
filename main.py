"""Wallet 1 entry for news-image-20261117: the infographic collage.

Picture summary: a dark-blue infographic titled "The World in One
Picture" for Tuesday 17 November 2026. Its lead panel draws Ukraine's
strike collapsing one span of the Kerch Bridge into the sea. Six cards
underneath it cover Bahrain blocking Iranian drones, Japan scrambling
jets, the United States losing measles-free status, a Russian warplane
crash that killed nineteen people, British sanctions on settlement
builders, and the COP31 draft climate deal from Antalya.

Before publishing, this program inspects the PNG header of the bundled
picture: it reads the IHDR chunk, extracts the pixel dimensions, and
refuses to publish anything wider or taller than 1024 pixels. It then
moves the picture to the output folder through a bytearray buffer and
reports how many buffer loads the transfer needed.
"""
import os
import struct
import sys

FOLDER = os.path.dirname(os.path.abspath(__file__))
ARTWORK = os.path.join(FOLDER, "entry.png")
BUFFER_SIZE = 16384
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
LIMIT = 1024


def artwork_dimensions(path):
    """Return (width, height) parsed from the PNG IHDR chunk."""
    with open(path, "rb") as handle:
        header = handle.read(24)
    if not header.startswith(PNG_SIGNATURE):
        raise ValueError("bundled artwork is not a PNG file")
    if header[12:16] != b"IHDR":
        raise ValueError("first PNG chunk is not IHDR")
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def transfer(source, destination):
    """Copy source to destination through a reusable bytearray."""
    buffer = bytearray(BUFFER_SIZE)
    view = memoryview(buffer)
    moved = 0
    loads = 0
    with open(source, "rb") as fin, open(destination, "wb") as fout:
        while True:
            count = fin.readinto(buffer)
            if count == 0:
                break
            fout.write(view[:count])
            moved += count
            loads += 1
    return moved, loads


def run():
    width, height = artwork_dimensions(ARTWORK)
    if width > LIMIT or height > LIMIT:
        raise SystemExit(f"artwork is {width}x{height}, over the cap")
    out_folder = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_folder, exist_ok=True)
    destination = os.path.join(out_folder, "entry.png")
    moved, loads = transfer(ARTWORK, destination)
    average_load = moved / loads if loads else 0
    print(f"average buffer load: {average_load:.1f} bytes")
    expected = os.path.getsize(ARTWORK)
    if moved != expected:
        raise SystemExit(f"moved {moved} bytes, artwork holds {expected}")
    print(f"collage {width}x{height} published in {loads} buffer loads")
    print(f"total bytes published: {moved}")
    return 0


if __name__ == "__main__":
    sys.exit(run())
