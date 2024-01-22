import gzip
from json import load
from typing import Dict
import os.path


def get_ru_main_synonym(language: str) -> Dict[str, str]:
    first_two_letters = language[:2]
    path = f'../data/{first_two_letters}_main_synonyms.json.gz'
    if not os.path.exists(path):
        return {}
    with gzip.open(path, 'rt') as f:
        return load(f)
