#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import time

import digitalocean
from box import Box

_manager = None


class DOGS:
    def __init__(self, server_name, config_file='config.yaml'):
        self.server_name = server_name
        cfg = Box.from_yaml(filename=config_file)
        self.config_file = config_file
        self.token = cfg.token
        self.config = next((s for s in cfg.servers if s.name == server_name), None)
        self.name = server_name
        self.manager = digitalocean.Manager(token=self.token)
        self.droplet = None
        try:
            self.droplet = self.manager.get_droplet(self.config.get("droplet_id"))
        except digitalocean.Error:
            for d in self.manager.get_all_droplets():
                if d.name == self.name:
                    self.droplet = d
        if self.droplet:
            assert self.droplet.name == self.name, "Droplet name and config name do not match!"

    def create_from_snapshot(self, snapshot):
        my_droplets = self.manager.get_all_droplets()
        keys = self.manager.get_all_sshkeys()

        if isinstance(self.config.startup_sh, list):
            user_data = f"""
                #cloud-config
                runcmd:
                """
            user_data += '\n - '.join(list(self.config.startup_sh))

        for drop in my_droplets:
            assert drop.name != self.name, "Droplet already exists"
        new_droplet = digitalocean.Droplet(
            name=self.name,
            size=self.config.get('size', "s-1vcpu-2gb"),
            image=snapshot.id,
            region=self.config.get('region', "nyc1"),
            ssh_keys=keys,
            user_data=user_data or None,
            monitoring=True,
            token=self.token,
            tags=[self.name]
        )

        print(f"Creating droplet from snapshot {snapshot.id}")
        new_droplet.create()
        self.droplet = new_droplet

    def find_newest_snapshot(self):
        print("Finding newest snapshot")
        snapshots = self.manager.get_all_snapshots()
        newest = 0
        snapshot = None
        for snap in snapshots:
            if snap.name.startswith(self.name):
                if snap.name.endswith('base') and newest == 0:
                    snapshot = snap
                else:
                    dt = int(snap.name.split("-")[-1])
                    if dt > newest:
                        newest = dt
                        snapshot = snap
        return snapshot

    def wait_for_action(self, action=None, action_name=None):
        if action_name:
            for a in self.droplet.get_actions():
                if a.type == action_name:
                    action = a
                    break
            else:
                raise AssertionError(f'could not find {action_name} action')

        for i in range(20):
            action.load()
            print(f'{action.type}: {action.status}')
            if action.status == 'completed':
                break
            elif action.status == 'in-progress':
                time.sleep(15)
            else:
                raise Exception(action.status)
        else:
            raise AssertionError(f'Could not {action.type}')

    def create(self):
        snapshot = self.find_newest_snapshot()
        if not snapshot:
            raise AssertionError("No relevant snapshot found")
        self.create_from_snapshot(snapshot)
        self.wait_for_action(action_name='create')
        self.droplet.load()
        print(f"Droplet online: {self.droplet.ip_address}")

        if self.config.firewall_id:
            print("Adding droplet to Firewall")
            firewall = self.manager.get_firewall(self.config.firewall_id)
            firewall.add_droplets([self.droplet.id])

    def destroy(self, cleanup=True):
        if self.config.shutdown_before_destroy:
            print(f"Shutting down droplet: ${self.name}")
            shutdown_info = self.droplet.shutdown()
            shutdown_action = self.droplet.get_action(shutdown_info['action']['id'])
            self.wait_for_action(action=shutdown_action)
            print('Droplet shut down.')
        else:
            print(f"NOT shutting down droplet '${self.name}' before snapshot")

        snap_name = f"{self.name}-{int(time.time())}"
        print(f"Creating snapshot: {snap_name}")
        snap_info = self.droplet.take_snapshot(snap_name)
        snap_action = self.droplet.get_action(snap_info['action']['id'])
        self.wait_for_action(action=snap_action)
        print('Snapshot created successfully.')

        print('Destroying droplet!')
        self.droplet.destroy()

        if cleanup:
            self.cleanup()

    def cleanup(self):
        all_snapshots = self.manager.get_all_snapshots()
        relevant = []
        for snapshot in all_snapshots:
            if snapshot.name.startswith(self.name):
                relevant.append(snapshot)

        relevant.sort(key=lambda x: int(x.name.split("-")[-1]), reverse=True)

        print(f"Deleting all but the newest {self.config.get('snapshot_max', 2)} snapshots")
        for snapshot in relevant[self.config.get('snapshot_max', 2):]:
            snapshot.destroy()

def find_droplets(prefix, config):
    manager = digitalocean.Manager(token=config.token)
    return [f"{x.name} @ {x.ip_address}" for x in manager.get_all_droplets() if x.name.startswith(prefix)]


def find_snapshots(prefix, config):
    manager = digitalocean.Manager(token=config.token)
    return [f"{x.name}" for x in manager.get_all_snapshots() if x.name.startswith(prefix)]
