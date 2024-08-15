import os

from .mapping import remap_verses

VALID_SCHEMAS = ["eng", "rsc", "rso", "vul", "org", "lxx"]

cwd = os.path.dirname(os.path.realpath(__file__))
vref_path = os.path.join(cwd, "vref.txt")


def get_master_vref():
    with open(vref_path, "r") as f:
        return [line.strip() for line in f.readlines()]


def to_vref(filename, verses, versification):
    if versification not in VALID_SCHEMAS:
        raise ValueError(f"Invalid versification schema: {versification}")

    if versification != "org":
        verses = remap_verses(verses, versification, "org")

    with open(filename, "w") as f:
        for ref in get_master_vref():
            f.write(verses.get(ref, ""))
            f.write("\n")
