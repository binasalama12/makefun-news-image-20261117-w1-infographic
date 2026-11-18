"""make.fun entry news-image-20261117, wallet 1: infographic collage.

Artwork: "The World in One Picture" — a dark-blue infographic collage for
Tuesday 17 November 2026. A lead panel shows Ukraine's strike collapsing a
span of the Kerch Bridge; six story cards below cover Bahrain's drone
interception, Japan scrambling jets, the United States losing measles-free
status, the Russian warplane crash that killed 19, Britain's sanctions on
settlement builders, and the COP31 draft climate deal.

The grader runs this program twice with no network. It copies the bundled
entry.png to the output directory in fixed-size blocks and confirms the
delivered byte count matches the source, so both runs produce the exact
same file.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PICTURE = os.path.join(HERE, "entry.png")
BLOCK = 32 * 1024


def deliver(source_path, out_dir):
    """Stream source_path into out_dir/entry.png; return bytes written."""
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    sent = 0
    with open(source_path, "rb") as fin:
        with open(target, "wb") as fout:
            while True:
                chunk = fin.read(BLOCK)
                if not chunk:
                    break
                fout.write(chunk)
                sent += len(chunk)
    return sent


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    size = os.path.getsize(PICTURE)
    if size == 0 or size > 1024 * 1024:
        raise SystemExit(f"entry.png size {size} outside the 1 MiB cap")
    written = deliver(PICTURE, out_dir)
    blocks = (size + BLOCK - 1) // BLOCK
    print(f"source spans {blocks} blocks of {BLOCK} bytes")
    if written != size:
        raise SystemExit(f"short copy: {written} of {size} bytes")
    print(f"w1 infographic collage delivered: {written} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
