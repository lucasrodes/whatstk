#!/usr/bin/env bash
echo ">> Downloading python virtual environment"
pip3 install --user virtualenv

echo ">> Creating python environment"
python3  -m venv .whatstk
source .whatstk/bin/activate

echo ">> Creating virtual environment for Jupyter Notebooks"
python3 -m ipykernel install --user --name .whatstk --display-name "whatstk"

echo ">> Installing python dependencies"
pip3 install --user -r requirements.txt


