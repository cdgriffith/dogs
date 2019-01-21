#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from subprocess import run


def main():
    run("pyinstaller -F dogs/__main__.py -n dogs")
