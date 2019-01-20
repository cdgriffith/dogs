#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import digitalocean
import time

from box import Box

config = Box.from_yaml(filename='config.yaml')
required_keys = ["name", "firewall_id", "token"]
for key in required_keys:
    if key not in config:
        raise AssertionError(f"Need all these keys in the config: {', '.join(required_keys)}")


manager = digitalocean.Manager(token=config.token)
my_droplets = manager.get_all_droplets()

if config.get('droplet_id'):
    raise AssertionError('Config droplet ID set, should be empty, make sure droplet does not exist and clear config')

for drop in my_droplets:
    assert drop.name != config.name, "Droplet already exists"

print("Finding newest snapshot")
snapshots = manager.get_all_snapshots()
newest = 0
snap_id = 0
for snapshot in snapshots:
    if snapshot.name.startswith(config.name):
        if snapshot.name.endswith('base') and newest == 0:
            snap_id = snapshot.id
        else:
            dt = int(snapshot.name.split("-")[-1])
            if dt > newest:
                newest = dt
                snap_id = snapshot.id

if snap_id == 0:
    raise AssertionError("No relevant snapshot found")

snap_name = f"{config.name}-{newest}"
print(f"using snapshot {snap_id}")


new_droplet = digitalocean.Droplet(
    name=config.name,
    size=config.get('size', "s-1vcpu-2gb"),
    image=snap_id,
    region=config.get('region', "nyc3"),
    ssh_keys=[23913708],
    monitoring=True,
    token=config.token,
    tags=[config.name]
)

print("Creating droplet")
new_droplet.create()

actions = new_droplet.get_actions()
create_action = None
for action in actions:
    if action.type == 'create':
        create_action = action
        break
else:
    raise AssertionError('could not find creation action')

for i in range(20):
    create_action.load()
    if create_action.status == 'completed':
        print('Building: complete')
        break
    elif create_action.status == 'in-progress':
        print(f'Building: {create_action.status}')
        time.sleep(10)
    else:
        raise Exception(create_action.status)
else:
    raise AssertionError('Did not create')

config.droplet_id = new_droplet.id
config.to_yaml(filename="config.yaml")

print("Adding droplet to Firewall")
firewall = manager.get_firewall(config.firewall_id)
firewall.add_droplets(config.droplet_id)

print(f"Droplet online: {new_droplet.ip_address}")


