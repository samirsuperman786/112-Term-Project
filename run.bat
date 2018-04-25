#!/bin/bash
echo "Starting Server"

start /d "C:\Program Files\MongoDB\Server\3.6\bin\" mongod.exe

start python server.py

start python __init__.py

start python __init__.py

