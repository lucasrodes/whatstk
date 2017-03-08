# whatsapp-stats

This project is in current development. Its purpose is to provide a set of
tools to detect some hidden patterns in whatsapp group chats.

## Test

Test the program running `python main.py < file.in`, where file.in is the chat
you want to analyze.

### Comments on `file.in`

Email the chat of your whatsapp group using your phone. To do so, got to the
group conversation, click the three dots (up-right) and select More. Finally,
click on Email chat.

## Dependencies

Use the `requirements.txt` file to install all dependencies

`pip install -r requirements.txt`

It is highly recommended (as well as being the simplest and easiest way) to install these dependencies with `pip` inside a virtual environment to keep
them isolated from the rest of the system.

### Virtualenv setup

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

For more details, pleace check the related [Python documentation](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
<>- [NumPy](https://github.com/numpy/numpy)
<>- [Pandas](https://github.com/pandas-dev/pandas)
<>- [SciPy](http://www.scipy.org/install.html)
<>- [Matplotlib](http://matplotlib.org/users/installing.html)
<>    - [LaTeX](http://www.tug.org/)
<>    - dvipng
<>    - ghostscript
<>- [SeaBorn](http://seaborn.pydata.org/installing.html#installing)

<>The sub-dependencies of Matplotlib are needed for plotting with LaTeX fonts.



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
