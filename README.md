<div align="center">
  <img src="https://raw.githubusercontent.com/lucasrodes/whatstk/develop/assets/logo.svg" width="70%"><br>
</div>

---

<h1 align="center" style="border-bottom: none;"> whatstk: analyze WhatsApp chats with python
</h1>

<p align="center">
  <a href="#">
    <img alt="Package version" src="https://img.shields.io/badge/version-0.4.0.dev0-blue.svg?&color=25D366&logo=whatsapp&">
  </a>
</p>
<!-- style=for-the-badge -->

<p align="center">
  <a href="https://travis-ci.org/lucasrodes/whatstk"><img alt="Build Status" src="https://travis-ci.com/lucasrodes/whatstk.svg?branch=develop"></a>
  <a href="https://codecov.io/gh/lucasrodes/whatstk"><img alt="codecov" src="https://codecov.io/gh/lucasrodes/whatstk/branch/master/graph/badge.svg"></a>
  <a href="https://www.python.org/downloads/release/python-3/"><img alt="Python 3" src="https://img.shields.io/badge/python-3.7|3.8|3.9-blue.svg?&logo=python&logoColor=yellow"></a>
  <a href="https://lcsrg.me/whatstk"><img alt="Documentation" src="https://img.shields.io/badge/whatstk-docs-royalblue.svg"></a>
  <a href="https://pepy.tech/badge/whatstk"><img alt="Number of downloads" src="https://pepy.tech/badge/whatstk"></a>
  <a href="http://github.com/lucasrodes/whatstk"><img alt="HitCount" src="https://views.whatilearened.today/views/github/lucasrodes/whatstk.svg"></a>
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
* [Documentation](https://lcsrg.me/whatstk)
* [Contributing](#contributing)


## Installation

```
pip install whatstk
```


## Getting Started
#### Export your chat using your phone: 
Follow these [instructions](https://lcsrg.me/whatstk/source/getting_started/export_chat.html).

#### Convert chat to csv
Easily convert your txt chat file to csv using command `whatstk-to-csv`.

```bash
$ whatstk-to-csv [input_filename] [output_filename]
```

#### Load chat in python
You can also load the exported txt file with python.

```python
from whatstk import WhatsAppChat
from whatstk.data import whatsapp_urls
chat = WhatsAppChat.from_source(filepath=whatsapp_urls.LOREM)
```

#### More examples

Find more examples in the [getting started](https://lcsrg.me/whatstk/source/getting_started/index.html) and 
[examples](https://lcsrg.me/whatstk/source/code_examples/index.html) sections.

## Documentation
See [official documentation](https://lcsrg.me/whatstk).

## Contribute
See [contribute section](https://lcsrg.me/whatstk/source/contribute.html).

## License
[GPL-3.0](LICENSE)
