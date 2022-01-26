import os
from pathlib import Path


def path_for_resource(filename: str):
    return Path(os.path.dirname(os.path.realpath(__file__))).parent / 'resources' / filename
