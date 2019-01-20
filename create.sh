#!/usr/bin/env bash
useradd factorio
chown -R factorio:factorio /opt/factorio

touch /etc/systemd/system/factorio.service
chmod 0755 /etc/systemd/system/factorio.service
systemctl daemon-reload
systemctl enable  /etc/systemd/system/factorio.service
systemctl start factorio.service
