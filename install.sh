#!/bin/bash

sudo apt update
sudo apt install python3 python3-venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
