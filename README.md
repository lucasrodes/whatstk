<div align="center">
  <img src="assets/logo.svg" width="70%"><br>
</div>

---

<h1 align="center" style="border-bottom: none;"> whatstk: analyze WhatsApp chats with python
</h1>

<p align="center">
  <a href="#">
    <img alt="Package version" src="https://img.shields.io/badge/version-0.3.0dev0-blue.svg?&color=25D366&logo=whatsapp&style=for-the-badge">
  </a>
</p>
<!-- style=for-the-badge -->

<p align="center">
  <a href="https://travis-ci.org/lucasrodes/whatstk"><img alt="Build Status" src="https://travis-ci.com/lucasrodes/whatstk.svg?branch=develop"></a>
  <a href="https://codecov.io/gh/lucasrodes/whatstk"><img alt="codecov" src="https://codecov.io/gh/lucasrodes/whatstk/branch/master/graph/badge.svg"></a>
  <a href="https://www.python.org/downloads/release/python-3/"><img alt="Python 3.7" src="https://img.shields.io/badge/python-3.7|3.8-blue.svg?&logo=python&logoColor=yellow"></a>
  <a href="docs/index.md"><img alt="Documentation" src="https://img.shields.io/badge/documentation-royalblue.svg"></a>
  <a href="https://github.com/lucasrodes/whatstk/blob/master/LICENSE"><img alt="GitHub
license" src="https://img.shields.io/github/license/lucasrodes/whatstk.svg?"></a>
  <a href="https://gitter.im/sociepy/whatstk?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge"><img alt="Join the chat at https://gitter.im/sociepy/whatstk" src="https://badges.gitter.im/sociepy/whatstk.svg"></a>
</p>


<!-- [![Downloads](https://pepy.tech/badge/whatstk)](https://pepy.tech/project/whatstk) -->
<!-- > [Get the Desktop App](https://lcsrg.me/whatstk-gui) -->

**whatstk** is a python package providing tools to parse, analyze and visualise WhatsApp chats developed under the
**[sociepy](https://github.com/sociepy)** project. Easily convert your chats to csv or simply visualise some stats using
the provided command-line tools or python. The package uses [pandas](https://github.com/pandas-dev/pandas) to process
the data and [plotly](https://github.com/plotly/plotly.py) to visualise it.

It is distributed under the GPL-3.0 license. 

⭐ Please **star** our project if you found it interesting to **give us some dopamine** 😄!

### Content
* [Installation](#installation)
* [Getting Started](#getting-started)
* [Documentation](docs/index.md)
* [Contributing](#contributing)


## Installation

```
pip install whatstk
```


## Getting Started
#### Export your chat using your phone: 
Follow this [instructions](https://lcsrg.me/whatstk-gui/#faqs).

#### Convert chat to csv
Easily convert your txt chat file to csv using command `whatstk-to-csv`.

```bash
$ whatstk-to-csv [input_filename] [output_filename]
```

#### Load chat in python
You can also load the exported txt file with python.

```python
from whatstk.objects import WhatsAppChat

filename = 'chats/example.txt'
chat = WhatsAppChat.from_txt(filename)
```
#### More examples

Find more examples [here](docs/api.md).

## Documentation
Check [documentation](docs/index.md).

## Contributing
See [contributing section](CONTRIBUTING.md).


## License
[GPL-3.0](LICENSE)
