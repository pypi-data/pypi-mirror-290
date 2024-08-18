import hashlib
import json
import os
import re
import shutil
from typing import Any, NamedTuple, TypedDict

import pandas as pd

CWD = os.path.dirname(__file__)

RESOURCES_DIR = f"{CWD}/resources"
RENPY_COMMON_NAME = "common"
RENPY_RPY_EXTENSION = "rpy"
RENPY_RPYM_EXTENSION = f"{RENPY_RPY_EXTENSION}m"
RESOURCES_COMMON_RPYM = (
    f"{RESOURCES_DIR}/{RENPY_COMMON_NAME}.{RENPY_RPYM_EXTENSION}.txt"
)
RENPY_COMMON_DIR = f"renpy/{RENPY_COMMON_NAME}"
GAME_DIR = "game"
GAME_COMMON = f"{GAME_DIR}/tl/None/{RENPY_COMMON_NAME}.{RENPY_RPYM_EXTENSION}"
GAME_DIALOGUE = "dialogue.tab"
CROWDIN_DIR = "crowdin"
CROWDIN_INPUTS_DIR = f"{CROWDIN_DIR}/inputs"


class DialogueEntry(NamedTuple):
    hash: str
    identifier: str | None
    character: str | None
    dialogue: str
    filename: str
    line_number: int
    renpy_script: str | None


class CrowdinInput(TypedDict):
    text: str
    crowdinContext: str


def hash_object(obj: Any, length=8):
    # Convert the tuple to a string representation
    tuple_string = str(obj)

    # Create a SHA-256 hash of the string
    sha = hashlib.sha256(tuple_string.encode())

    # Convert the hash to a hexadecimal string and take the first 8 characters
    hash_hex = sha.hexdigest()[:length]

    return hash_hex


def read_common(file=GAME_COMMON):
    if not os.path.exists(file):
        file = RESOURCES_COMMON_RPYM
    with open(file, encoding="utf-8") as fo:
        common = fo.read()
    pattern = r"^.*#\s(.+):(\d+)\n.*old\s['\"](.*)['\"]$"
    matches = re.findall(pattern, common, re.MULTILINE)
    rv: list[DialogueEntry] = []
    for match in matches:
        tpl = (None, None, match[2], match[0], int(match[1]), None)
        rv.append(DialogueEntry(hash_object(tpl), *tpl))
    return rv


def read_dialogue(file=GAME_DIALOGUE):
    df = pd.read_csv(file, sep="\t")
    df = df.where(pd.notnull(df), None)
    dialogue = list(
        map(
            lambda e: DialogueEntry(hash_object(e), *e),
            df.itertuples(index=False, name=None),
        )
    )
    return dialogue


def create_crowdin_inputs(
    inputs=CROWDIN_INPUTS_DIR, dialogue=GAME_DIALOGUE, common=GAME_COMMON
):
    cdialogue = read_common(common)
    mdialogue = read_dialogue(dialogue)
    adialouge = cdialogue + mdialogue

    if os.path.exists(inputs):
        shutil.rmtree(inputs)
    os.makedirs(inputs, exist_ok=True)

    files: dict[str, dict[str, CrowdinInput]] = {}

    for de in adialouge:
        path = de.filename
        if path.startswith(RENPY_COMMON_DIR):
            path = f"{inputs}/{RENPY_COMMON_NAME}.{RENPY_RPY_EXTENSION}.json"
        else:
            path = path.removeprefix(GAME_DIR + "/")
            path = f"{inputs}/{path}.json"
        if path not in files:
            file = files[path] = {}
        else:
            file = files[path]
        file[de.hash] = {"text": de.dialogue, "crowdinContext": ""}

    for path, content in files.items():
        dirname = os.path.dirname(path)
        os.makedirs(dirname, exist_ok=True)
        with open(path, "w", encoding="utf-8") as fo:
            json.dump(content, fo, indent=4)
