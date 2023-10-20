#!/bin/sh
cd /opt/tc/idstools/etc  || exit

idstools-rulecat --force

while true; do sleep 1; done
