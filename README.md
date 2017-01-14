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

- [NumPy](https://github.com/numpy/numpy)
- [Pandas](https://github.com/pandas-dev/pandas)
- [SciPy](http://www.scipy.org/install.html)
- [Matplotlib](http://matplotlib.org/users/installing.html)
- [SeaBorn](http://seaborn.pydata.org/installing.html#installing)

It is recommended (as well as being the simplest and easiest way) to install these dependencies with `pip` inside a `virtualenv` to keep
them isolated from the rest of the system.

## License

whatsapp-stats

Copyright (C) 2016  Lucas Rodés Guirao, Albert Aparicio, Nicolas Buenavides Cuervo

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
