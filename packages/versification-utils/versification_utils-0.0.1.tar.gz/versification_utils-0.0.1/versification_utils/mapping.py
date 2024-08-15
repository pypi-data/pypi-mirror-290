import json
import os

VALID_SCHEMAS = ["eng", "lxx", "org", "vul", "rsc", "rso"]

cwd = os.path.dirname(os.path.realpath(__file__))
standard_mappings_dir = os.path.join(cwd, "standard_mappings")


def expand(key):
    if "-" not in key:
        return [key]
    chapter, verse = key.split(":")
    first, last = verse.split("-")
    return [f"{chapter}:{i}" for i in range(int(first), int(last) + 1)]


def get_expanded_mappings_for_mapped_verses(mapped_verses):
    return {
        k: v for m in mapped_verses for k, v in zip(expand(m), expand(mapped_verses[m]))
    }


def get_mappings_for_versification_schema(schema):
    if schema not in VALID_SCHEMAS:
        raise ValueError(f"Invalid versification: {schema}")

    with open(os.path.join(standard_mappings_dir, f"{schema}.json")) as f:
        data = json.load(f)

    mapped_verses = data["mappedVerses"]
    return get_expanded_mappings_for_mapped_verses(mapped_verses)


def invert(mappings):
    return {v: k for k, v in mappings.items()}


def remap_verses(verses, from_schema, to_schema):
    from_mappings = get_mappings_for_versification_schema(from_schema)
    to_mappings = invert(get_mappings_for_versification_schema(to_schema))

    def get_new_ref(ref):
        from_ref = from_mappings.get(ref, ref)
        return to_mappings.get(from_ref, from_ref)

    return {get_new_ref(ref): text for ref, text in verses.items()}
