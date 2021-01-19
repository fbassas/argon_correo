#!/bin/bash

mapes=$(postconf -n | grep "^virtual_alias_maps" | awk -F= '{print $2}' | sed s/,//g)
postmap -q $1 $mapes

