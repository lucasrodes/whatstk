#!/usr/bin/env bash
echo "> Downloading python virtual environment"
pip3 install virtualenv

echo "> Creating python environment"
python3 -m venv .whatstk
source .whatstk/bin/activate

echo "> Installing python dependencies"
pip3 install -r dependencies/requirements.txt
