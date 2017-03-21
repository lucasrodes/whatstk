### Install virtualenv

`$ pip3 install virtualenv`

If this raises an error, try installing `sudo apt install python3-venv`

Create a new virtualenv

`$ python3 -m venv <envname>`

Activate the environment

`$ . <envname>/bin/activate`

Install all the dependencies from `requirements.txt`

`$ pip3 install -r requirements.txt`

You can exit the environment by typing

`$ deactivate`

I you modify the project using new libraries you might install, update the requirements.txt file

`$ pip3 freeze > requirements.txt`

For further questions, please consider reading the related documentation here.
