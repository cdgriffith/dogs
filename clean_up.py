#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import digitalocean

from box import Box

config = Box.from_yaml(filename='config.yaml')
required_keys = ["name", "token"]
for key in required_keys:
    if key not in config:
        raise AssertionError(f"Need all these keys in the config: {', '.join(required_keys)}")


manager = digitalocean.Manager(token=config.token)




