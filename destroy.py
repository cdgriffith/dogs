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





