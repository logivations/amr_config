#!/usr/bin/python3

import collections.abc
import yaml


def update(d, u):
    if u is not None:
        for k, v in u.items():
            if isinstance(v, collections.abc.Mapping):
                d[k] = update(d.get(k, {}), v)
            else:
                d[k] = v
    return d

def get_w2mo_config():
    return {}

def get_config():
    with open("/code/ros2_ws/src/amr_config/instance/instance.yaml", 'r') as stream:
        try:
            instance_yaml=yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    with open("/code/ros2_ws/src/amr_config/environment/environment.yaml", 'r') as stream:
        try:
            environment_yaml=yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    with open("/code/ros2_ws/src/amr_config/defaults.yaml", 'r') as stream:
        try:
            default_yaml=yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    w2mo_config = get_w2mo_config()
    environment_yaml = update(environment_yaml, w2mo_config) # Assuming w2mo parameters only update environment values

    config = update(update(default_yaml, environment_yaml), instance_yaml)
    with open('/code/ros2_ws/src/amr_config/active_config.yaml', 'w') as outfile:
        yaml.dump(config, outfile, default_flow_style=False)

if __name__ == "__main__":
    get_config()
