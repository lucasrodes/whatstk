<div align="left">
  <img src="https://raw.githubusercontent.com/lucasrodes/whatstk/develop/assets/logo.svg" width="70%">
</div>
<h1 align="left" style="border-bottom: none;"> whatstk: analyze WhatsApp chats with python
</h1>
<p align="left">
  <a href="#">
    <img alt="Package version" src="https://img.shields.io/badge/pypi-0.6.0-blue.svg?&color=25D366&logo=whatsapp&">
  </a>
</p>
<!-- style=for-the-badge -->

<p align="left">
  <a href="https://travis-ci.com/lucasrodes/whatstk">
    <img alt="Build Status" src="https://travis-ci.com/lucasrodes/whatstk.svg?branch=develop">
  </a>
  <a href="https://codecov.io/gh/lucasrodes/whatstk">
    <img alt="codecov" src="https://codecov.io/gh/lucasrodes/whatstk/branch/master/graph/badge.svg">
  </a>
  <a href='https://whatstk.readthedocs.io/en/stable/?badge=stable'>
    <img src='https://readthedocs.org/projects/whatstk/badge/?version=stable' alt='Documentation Status' />
  </a>
  <a href="https://towardsdatascience.com/analyzing-whatsapp-chats-with-python-20d62ce7fe2d">
    <img alt="Tutorial" src="https://img.shields.io/badge/tutorial-on_medium-1a8917.svg?&logo=medium&logoColor=white">
  </a>
  <a href="https://www.python.org/downloads/release/python-3/">
    <img alt="Python 3" src="https://img.shields.io/badge/python-3.8|3.9|3.10|3.11-blue.svg?&logo=python&logoColor=yellow">
  </a>
  <a href="https://pepy.tech/badge/whatstk">
    <img alt="Number of downloads" src="https://pepy.tech/badge/whatstk">
  </a>
  <a href="https://github.com/lucasrodes/whatstk/blob/master/LICENSE">
    <img alt="GitHub license" src="https://img.shields.io/github/license/lucasrodes/whatstk.svg?">
  </a>
  <a href="https://gitter.im/sociepy/whatstk?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge">
    <img alt="Join the chat at https://gitter.im/sociepy/whatstk" src="https://badges.gitter.im/sociepy/whatstk.svg">
  </a>
</p>

---

<!-- [![Downloads](https://pepy.tech/badge/whatstk)](https://pepy.tech/project/whatstk) -->
<!-- > [Get the Desktop App](https://lcsrg.me/whatstk-gui) -->

**whatstk** is a python package providing tools to parse, analyze and visualise WhatsApp chats developed under the
**[sociepy](https://sociepy.org)** project. Easily convert your chats to csv or simply visualise some stats using
the provided command-line tools or python. The package uses [pandas](https://github.com/pandas-dev/pandas) to process
the data and [plotly](https://github.com/plotly/plotly.py) to visualise it.

It is distributed under the GPL-3.0 license.

⭐ Please **star** our project if you found it interesting to **give us some dopamine** 😄!

### Content

- [Installation](#installation)
- [Getting Started](#getting-started)
- [Documentation](https://whatstk.readthedocs.io/en/stable/)
- [Contribute](#contribute)
- [Covered in](#covered-in)
- [Citation](#citation)

## Installation

```
pip install whatstk
```

Install develop version (not stable):

```
pip install git+https://github.com/lucasrodes/whatstk.git@develop
```

_More details [here](https://whatstk.readthedocs.io/en/stable/source/about.html#installation-compatibility)_

## Getting Started

For a rapid introduction, check this [tutorial on Medium](https://towardsdatascience.com/analyzing-whatsapp-chats-with-python-20d62ce7fe2d).

#### Export your chat using your phone:

_See [instructions](https://whatstk.readthedocs.io/en/stable/source/getting_started/export_chat.html)._

#### Load chat as a DataFrame

```python
from whatstk import df_from_txt_whatsapp
df = df_from_txt_whatsapp("path/to/chat.txt")
```

#### Convert chat to csv

```bash
$ whatstk-to-csv [input_filename] [output_filename]
```

#### More examples

_See more in sections [getting started](https://whatstk.readthedocs.io/en/stable/source/getting_started/index.html) and
[examples](https://whatstk.readthedocs.io/en/stable/source/code_examples/index.html)._

## Documentation

_See [official documentation](https://whatstk.readthedocs.io/en/stable/)._

## Contribute

_See [contribute section](https://whatstk.readthedocs.io/en/stable/source/contribute.html)._

## License

[GPL-3.0](LICENSE)

## Citation

Lucas Rodés-Guirao. "whatstk, WhatsApp analysis and parsing toolkit", https://github.com/lucasrodes/whatstk

## Covered in

- [Your Whatsapp Chat History in Cool Graphs](https://deepnote.com/@batmanscode/Your-Whatsapp-Chat-History-in-Cool-Graphs-mQoSsYjUSw29D4nZDs_KwA), by [@batmanscode](https://github.com/batmanscode).
- [WhatsAppening to the news](https://whatsappening.joltetn.eu/), by [@enric1994](https://github.com/enric1994)
- [whatsappening source code](https://github.com/enric1994/whatsappening), by [@enric1994](https://github.com/enric1994)
