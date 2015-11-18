#!/bin/bash

mongo < setupDatabase.js
python testapi.py $1 $2 test
