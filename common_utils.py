import yaml
import sys

def get_config(config_path:str):
    with open(config_path, 'r') as f:
        contents = yaml.safe_load(f)
    return contents
