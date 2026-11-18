#!/bin/bash

# Use [`unittest` module](https://docs.python.org/3/library/unittest.html) 
# to run all the tests (`discover`) it can find in `src`` directory.
python3.10 -m unittest discover -s src