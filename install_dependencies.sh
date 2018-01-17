#!/usr/bin/env bash
echo ">> Downloading python virtual environment"
pip3 install --user virtualenv

echo ">> Creating python environment"
python3  -m venv .whatstk

echo ">> Creating virtual environment for Jupyter Notebooks"
python3 -m ipykernel install --user --name .whatstk --display-name "whatstk"

echo ">> Installing python dependencies"
source .whatstk/bin/activate
pip3 install -r requirements.txt

