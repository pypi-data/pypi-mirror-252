import os
import json
import yaml
from pathlib import Path

sample_json_file = os.path.join(Path(__file__).parent, 'datafiles', 'sample.json')
sample_yaml_file = os.path.join(Path(__file__).parent, 'datafiles', 'sample.yaml')

def read_sample_yaml(path=sample_yaml_file):
    with open(path, "r") as file:
        return yaml.safe_load(file)

def read_sample_json(path=sample_json_file):
    with open(path, "r") as file:
        return json.load(file)
