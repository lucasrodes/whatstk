#!/usr/bin/env bash
echo ">> Downloading python virtual environment"
pip3 install --user virtualenv

echo ">> Creating python environment"
python3  -m venv .whatstk
<<<<<<< HEAD
=======

echo ">> Activating venv"
source .whatstk/bin/activate
>>>>>>> 61e70f545ffc0e055fe44440462c2b6c8f480300

echo ">> Creating virtual environment for Jupyter Notebooks"
python3 -m ipykernel install --user --name .whatstk --display-name "whatstk"

echo ">> Installing python dependencies"
<<<<<<< HEAD
source .whatstk/bin/activate
pip3 install --user -r requirements.txt
=======
pip3 install -r requirements.txt
>>>>>>> 61e70f545ffc0e055fe44440462c2b6c8f480300

