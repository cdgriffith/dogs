#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import time

import digitalocean
from box import Box


def wait_for_action(action):
    for _ in range(100):
        action.load()
        print(f'{action.type}: {action.status}')
        if action.status == 'completed':
            break
        if action.status == 'in-progress':
            time.sleep(10)
        else:
            raise Exception(f"Do not understand action status {action.status}")
    else:
        raise AssertionError(f'Could not {action.type}')


config = Box.from_yaml(filename='config.yaml')

manager = digitalocean.Manager(token=config.token)
try:
    droplet = manager.get_droplet(config.droplet_id)
except digitalocean.Error:
    droplet = None
    for d in manager.get_all_droplets():
        if d.name == config.name:
            droplet = d
    print(f'Found droplet {droplet}')

assert droplet and droplet.name == config.name, "Droplet name and config name do not match!"

print("Shutting down droplet")
shutdown_info = droplet.shutdown()
shutdown_action = droplet.get_action(shutdown_info['action']['id'])
wait_for_action(shutdown_action)

snap_name = f"{config.name}-{int(time.time())}"
print(f"Creating snapshot: {snap_name}")
snap_info = droplet.take_snapshot(snap_name)
snap_action = droplet.get_action(snap_info['action']['id'])
wait_for_action(snap_action)

print("Removing from firewall")
firewall = manager.get_firewall(config.firewall_id)
firewall.remove_droplets([droplet.id])

droplet.destroy()

config.droplet_id = None
config.to_yaml(filename="config.yaml")

print('Droplet destroyed')
