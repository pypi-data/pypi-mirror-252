import os
from setuptools import setup


def find_data_files(directory):
    data_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            data_files.append(os.path.relpath(os.path.join(root, file), directory))
    return data_files


setup(
    package_data={
        'synonymset': find_data_files('data'),
    }
)
