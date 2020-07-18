#!/usr/bin/bash

VIRTUALDIR=$(poetry env info -p)

rm $VIRTUALDIR/lib/python3.*/site-packages/slimit/yacctab.py
rm $VIRTUALDIR/lib/python3.*/site-packages/slimit/lextab.py

