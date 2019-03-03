#!/usr/bin/env bash
set -e

pushd /opt/factorio
systemctl stop factorio.service
rm -f linux64
mv factorio "factorio-(date +"%y%m%d%H%M%S")"

wget https://www.factorio.com/get-download/latest/headless/linux64
tar xf linux64
chown -R factorio:factorio /opt/factorio
popd

systemctl start factorio.service

