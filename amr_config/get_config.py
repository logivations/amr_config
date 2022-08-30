#!/usr/bin/python3

import collections.abc
import yaml

def update(d, u):
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = update(d.get(k, {}), v)
        else:
            d[k] = v
    return d

if __name__ == "__main__":
    with open("/root/amr_config/amr6_instance/instance.yaml", 'r') as stream:
        try:
            instance_yaml=yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    with open("/root/amr_config/brummer_environment/environment.yaml", 'r') as stream:
        try:
            environment_yaml=yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    with open("/root/amr_config/defaults.yaml", 'r') as stream:
        try:
            default_yaml=yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    config = update(update(default_yaml, environment_yaml), instance_yaml)
    print(config)