#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from subprocess import run


def build():
    run("pyinstaller -F dogs/__main__.py -n dogs")


if __name__ == '__main__':
    build()
