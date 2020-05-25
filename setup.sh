#!/bin/bash
echo "Setting up things..."
  python3 -m venv env
  source env/bin/activate
  pip3 install -r requirements.txt
  screen -S server
  source env/bin/activate
  python3 run.py
