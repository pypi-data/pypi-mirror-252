import importlib.resources
import importlib.metadata
import gzip
import json


def get_main_synonym(language: str):
    first_two_letters = language[:2]
    resource_path = f'{first_two_letters}_main_synonyms.json.gz'

    # Check if the resource exists
    for file in importlib.metadata.files('synonymset'):
        if file.match(resource_path):
            # Open the resource
            with importlib.resources.open_binary('synonymset', resource_path) as resource:
                with gzip.open(resource, 'rt') as f:
                    return json.load(f)
    return {}
