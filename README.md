:construction: :construction_worker: I am currently busy and hardly find time to mantain this repository. However I am willing to push a major code refactoring along with official documentation by May 2018. If anyone feels like helping please contact me.

----
# [whatstk](http://lucasrodes.github.io/whatstk)

whatstk is a Python module for WhatsApp chat group analysis and distributed under the GPL-3.0 license.

The project was started in December 2016 by [lucasrodes](https://github.com/lucasrodes) and [albertaparicio](https://github.com/albertaparicio).

:star: Please **star** our project if you found it interesting to **keep us motivated** :smiley:!
### Installation

First download the repo.
```
$ git clone https://github.com/lucasrodes/whatstk.git
$ cd whatstk
```

It is assumed that you are using Python 3. Next, you can install all its dependencies by running

```
$ bash install_dependencies.sh
```

This creates a virtual environment named `.whatstk` and installs all the python libraries required in the project. You can now
start the virtual environment by running

```
$ source .whatstk/bin/activate
```


Find more details in [install_dependencies.sh](install_dependencies.sh).
This is due to your directory being located within a path with spaces (more info [here](https://stackoverflow.com/questions/7911003/cant-install-via-pip-with-virtualenv)). Please use a path without spaces!

### Known issues

#### Header Support
The header of the chat log texts varies depending on your phone settings. We are making our best to provide support for all of them, but some might not be yet covered. Please check the list of supported headers in this [thread](https://github.com/lucasrodes/whatstk/issues/7) and comment if your header format is not supported!

#### Installation: bad interpreter
While running the installation, you might encounter an error like 

```
bad interpreter: No such file or directory
```

This is due to your directory being located within a path with spaces (more info [here](https://stackoverflow.com/questions/7911003/cant-install-via-pip-with-virtualenv)). Please use a path without spaces!

### Contribute
If you have any suggestion or you found any bug in the code please report it as an Issue or [text me](mailto:lucasrg@kth.se). Furthermore, we are open to pull requests from the community!

### License

whatstk

Copyright (C) 2016-2018 Lucas Rodés-Guirao, Albert Aparicio Isarn

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/.

