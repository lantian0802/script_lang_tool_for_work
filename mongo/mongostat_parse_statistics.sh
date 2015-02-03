#!/bin/bash
cat $1 | grep performance_test | head -n $2 | awk -F " " '{print $19,$1,substr($12,18,3)}'