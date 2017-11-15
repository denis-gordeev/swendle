#!/bin/bash

while true;
do
SETTINGS_MODE=prod python3 -u manage.py parse
killall -9 python3
done