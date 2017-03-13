# whatstk

We aim to create a robust and powerful library that provides a set of tools to analyse chat logs of WhatsApp and possibly detect hidden patterns using **unsupervised learning** methods. Currently, it only parses the data in a suitable format and displays basic information of the chat log.

## Organization

This project provides several tools which can be used in several different ways. To illustrate this, we provide with some Jupyter Notebooks and some sample code.

1. Library whatstk: Contains the files from the library
2. Notebooks: This includes some jupyter notebooks with illustrative examples of how to use this library


## Dependencies

This project uses some of the most common used Python libraries. Use the `requirements.txt` file to install all dependencies

`$ pip3 install -r requirements.txt`

We highly recommended to install these dependencies with `pip3` inside a virtual environment to keep them isolated from the rest of the system.


## F.A.Q.

**_How do I obtain the log of my chat?_**

> Email the chat of your whatsapp group using your phone. To do so, go to the group conversation, click the three dots (up-right) and select More. Finally,
click on Email chat. More information can be found [here](https://www.whatsapp.com/faq/en/s60/21055276)

**_Is this working for all languages?_**

> So far, this code was succesfully ran in the following languages:
> - English (12h, 24h-clock)
> - Spanish (24h-clock)

> Please do not hesitate reporting an issue if it does not work for you!

**_How do I setup a virtual environment?_**

> Install virtualenv

> `$ pip3 install virtualenv`

> Create a new virtualenv (we name it `.env`)

> `$ python3 -m venv .env`

> Activate the environment

> `$ . .whatstkenv/bin/activate`

> Install all the dependencies

> `$ pip3 install -r requirements.txt`

> You can exit the environment by typing

> `$ deactivate`

> I you modify the project using new libraries you might install, update the `requirements.txt` file

> `$ pip3 freeze > requirements.txt`

> For further questions, please consider reading the related documentation [here](http://docs.python-guide.org/en/latest/dev/virtualenvs/).


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
