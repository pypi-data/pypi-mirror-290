import os
from typing import List, Union

import yaml

cwd = os.path.dirname(os.path.realpath(__file__))
differences_path = os.path.join(cwd, "diagnostics", "vrs_diffs.yaml")
diagnostics = yaml.load(open(differences_path), Loader=yaml.FullLoader)

VERSIFICATION_SCHEMA_NAME_MAP = {
    "English": "eng",
    "Russian Protestant": "rsc",
    "Russian Orthodox": "rso",
    "Vulgate": "vul",
    "Original": "org",
    "Septuagint": "lxx",
    "Unknown": "unk",
}


def get_last_verse_per_chapter(verses: List[str]) -> List[str]:
    last_verse_per_chapter_list = {}
    for verse in verses:
        book_ch = verse.split(":")[0]
        if book_ch not in last_verse_per_chapter_list:
            last_verse_per_chapter_list[book_ch] = verse
        elif verse > last_verse_per_chapter_list[book_ch]:
            last_verse_per_chapter_list[book_ch] = verse
    return list(last_verse_per_chapter_list.values())


def detect(verses: List[str], log_votes=False) -> Union[str, List[str]]:
    votes = {v: 0 for v in VERSIFICATION_SCHEMA_NAME_MAP.keys()}
    for last_verse in get_last_verse_per_chapter(verses):
        book, chv = last_verse.split(" ")
        chapter, verse = chv.split(":")
        if (
            book in diagnostics
            and int(chapter) in diagnostics[book]
            and int(verse) in diagnostics[book][int(chapter)]
        ):
            for versification in VERSIFICATION_SCHEMA_NAME_MAP.keys():
                to_add = (
                    1
                    if versification in diagnostics[book][int(chapter)][int(verse)]
                    else -1
                )
                votes[versification] += to_add

    if log_votes:
        print(votes)

    if not votes:
        return VERSIFICATION_SCHEMA_NAME_MAP["Unknown"]

    # if there is a tie, return a list
    highest_vote = max(votes.values())
    if list(votes.values()).count(highest_vote) > 1:
        return [
            VERSIFICATION_SCHEMA_NAME_MAP[k]
            for k, v in votes.items()
            if v == highest_vote
        ]

    return VERSIFICATION_SCHEMA_NAME_MAP[max(votes, key=votes.get)]
