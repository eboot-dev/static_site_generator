#!/bin/bash

python3.10 src/main.py
cd public && python3.10 -m http.server 8888
