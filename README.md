<h1 align="center" style="border-bottom: none;"> <a href="http://lcsrg.me/whatstk">whatstk</a>
</h1>
<h3 align="center" style="border-bottom: none;">python whatsapp parser and analysis tool</h3>

<p align="center">
  <a href="#">
    <img alt="Package version" src="https://img.shields.io/badge/version-0.2.6-blue.svg?&color=25D366&logo=whatsapp">
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
</p>


<!-- [![Downloads](https://pepy.tech/badge/whatstk)](https://pepy.tech/project/whatstk) -->
<!-- > [Get the Desktop App](https://lcsrg.me/whatstk-gui) -->

**whatstk** is a Python module for WhatsApp chat group analysis and distributed under the GPL-3.0 license. Parse your
chats to csv with a simple command or read and analyze them using Python and pandas.DataFrame. 

⭐ Please **star** our project if you found it interesting to **keep us motivated** 😄!

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
Make sure to first obtain the chat to be analyzed. Export it as a `txt` file using your phone (more info on this
[here](https://lcsrg.me/whatstk-gui/#faqs)). Then you can use the library as follows

```python
from whatstk.objects import WhatsAppChat

filename = 'chats/example.txt'
chat = WhatsAppChat.from_txt(filename)
```

See more examples [here](docs/api.md)

## Documentation
Check [documentation](docs/index.md).

## Contributing
See [contributing section](CONTRIBUTING.md).


## License
See [license](LICENSE).
