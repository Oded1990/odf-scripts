#!/bin/bash
cd ./odf-scripts
pwd=$(pwd)
echo $pwd
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
