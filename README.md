# whatsapp-stats

This project is in current development. Its purpose is to provide a set of
tools to detect some hidden patterns in whatsapp group chats.

## Run

Simply run

`$ python main.py file`

where `file` is the name of the chat log file that you want to analyze. The program will prompt an error if `file` does not exist.

## Dependencies

This project uses some of the most common used Python libraries. Use the `requirements.txt` file to install all dependencies

`$ pip install -r requirements.txt`

We highly recommended to install these dependencies with `pip` inside a virtual environment to keep them isolated from the rest of the system.


## F.A.Q.

**_How do I obtain the log of my chat?_**

Email the chat of your whatsapp group using your phone. To do so, go to the
group conversation, click the three dots (up-right) and select More. Finally,
click on Email chat. More information can be found [here](https://www.whatsapp.com/faq/en/s60/21055276)

**_Is this working for all languages?_**

So far, this code was succesfully ran in the following languages:
- English (24-clock)
- Spanish (24-clock)

Please report an issue if it is not working for you!

**_How do I setup a virtual environment?_**

Install virtualenv

`$ pip install virtualenv`

Create a new virtualenv (we name it `.env`)

`$ python3 -m venv .env`

Activate the environment

`$ . .env/bin/activate`

Install all the dependencies

`$ pip install -r requirements.txt`

You can exit the environment by typing

`$ deactivate`

I you modify the project using new libraries you might install, update the `requirements.txt` file

`$ pip freeze > requirements.txt`

For further questions, please consider reading the related documentation [here](http://docs.python-guide.org/en/latest/dev/virtualenvs/).


## License

whatsapp-stats

Copyright (C) 2016  Lucas Rodés Guirao, Albert Aparicio, Nicolas Cuervo Benavides

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
