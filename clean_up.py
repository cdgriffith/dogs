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

all_snapshots = manager.get_all_snapshots()
relevant = []
for snapshot in all_snapshots:
    if snapshot.name.startswith(config.name):
        relevant.append(snapshot)

relevant.sort(key=lambda x: int(x.name.split("-")[-1]), reverse=True)

print(f"Keeping the newest {config.get('snapshot_max', 1)} snapshots")
for snapshot in relevant[config.get('snapshot_max', 1):]:
    snapshot.destroy()



