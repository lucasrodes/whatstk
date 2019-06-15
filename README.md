Working towards first release. Coming soon, instructions in this readme are not valid at the moment.
----
# [whatstk](http://lucasrodes.github.io/whatstk)

![Package version](https://img.shields.io/badge/whatstk-v0.0.1-brightgreen.svg?style=for-the-badge)
[![GitHub license](https://img.shields.io/github/license/lucasrodes/whatstk.svg?style=for-the-badge)](https://github.com/baldassarreFe/lucasrodes/blob/master/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/lucasrodes/whatstk.svg?style=for-the-badge)](https://github.com/lucasrodes/whatstk/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/lucasrodes/whatstk.svg?style=for-the-badge)](https://github.com/lucasrodes/whatstk/network)

whatstk is a Python module for WhatsApp chat group analysis and distributed under the GPL-3.0 license.

The project was started in December 2016 by [lucasrodes](https://github.com/lucasrodes) and [albertaparicio](https://github.com/albertaparicio).

:star: Please **star** our project if you found it interesting to **keep us motivated** :smiley:!
### Installation

```
pip install whatstk
```

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
We are very open to have collaborators. You can freely fork and issue a pull request with your updates!
For other issues/bugs/suggestions, please report it as an issue or [text me](mailto:lucasrg@kth.se).