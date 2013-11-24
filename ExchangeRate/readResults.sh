#!/bin/bash

DAYS="$1"
: ${DAYS:="20"}

./readResults.py --management-hide --print-operation=sell --print-currency=EUR --print-days=$DAYS

