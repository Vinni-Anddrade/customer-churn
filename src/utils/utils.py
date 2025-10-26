from box import ConfigBox
import yaml


def read_yaml(path):
    with open(path, "rb") as yaml_file:
        yaml_output = yaml.safe_load(yaml_file)

    return ConfigBox(yaml_output)
