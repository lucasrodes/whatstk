#!/usr/bin/env bash
echo ">> Downloading python virtual environment"
pip3 install --user virtualenv

echo ">> Creating python environment"
virtualenv -p python3 .whatstk
# python3  -m venv .whatstk

echo ">> Activating venv"
source .whatstk/bin/activate

echo ">> Creating virtual environment for Jupyter Notebooks"
python3 -m ipykernel install --user --name .whatstk --display-name "whatstk"
