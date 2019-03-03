#!/usr/bin/env bash
set -e

cp factorio.service /etc/systemd/system/factorio.service
chmod 0755 /etc/systemd/system/factorio.service
systemctl daemon-reload
systemctl enable  /etc/systemd/system/factorio.service

useradd factorio
pushd /opt/
mkdir factorio
pushd factorio
wget https://www.factorio.com/get-download/latest/headless/linux64
tar xf linux64
factorio/bin/x64/factorio --create /opt/factorio/main.zip
cp factorio/data/server-settings.example.json /opt/factorio/server-settings.json
chown -R factorio:factorio /opt/factorio
popd
popd

echo "Don't forget to customize /opt/factorio/server-settings.json, then run systemctl start factorio.service"