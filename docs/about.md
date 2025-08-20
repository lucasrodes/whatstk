# About whatstk

**whatstk** is a python package providing tools to parse, analyze and visualize WhatsApp chats developed by [Lucas Rodés-Guirao](https://lcsrg.me). Easily convert your chats to csv or simply visualize statistics using the python library. The package uses [pandas](https://github.com/pandas-dev/pandas) to process the data and [plotly](https://github.com/plotly/plotly.py) to visualise it.

You can also [try a live demo](https://whatstk.streamlit.app/).

The project is distributed under the [GPL-3.0 license](https://github.com/lucasrodes/whatstk/blob/master/LICENSE) and is available on [GitHub](http://github.com/lucasrodes/whatstk).

---

## First contact with whatstk

**whatstk** is built around `BaseChat` object interface, which requires class method `from_source` to be implemented. This method loads and parses the source chat file into a pandas.DataFrame.

Below, we use method `df_from_whatsapp` to load [LOREM chat](http://raw.githubusercontent.com/lucasrodes/whatstk/develop/chats/whatsapp/lorem.txt). To test it with your own chat, simply [export it as a txt file](getting_started/export_chat.md) to your computer and then use class argument `filepath`, as shown in the following example.

```python
>>> from whatstk import df_from_whatsapp
>>> from whatstk.data import whatsapp_urls
>>> df = df_from_whatsapp(filepath=whatsapp_urls.LOREM)
>>> df.head(5)
                 date        username                                            message
0 2020-01-15 02:22:56            Mary                     Nostrud exercitation magna id.
1 2020-01-15 03:33:01            Mary     Non elit irure irure pariatur exercitation. 🇩🇰
2 2020-01-15 04:18:42  +1 123 456 789  Exercitation esse lorem reprehenderit ut ex ve...
3 2020-01-15 06:05:14        Giuseppe  Aliquip dolor reprehenderit voluptate dolore e...
4 2020-01-15 06:56:00            Mary              Ullamco duis et commodo exercitation.
```

---

## Installation & compatibility

This project is on [PyPI](https://pypi.org/project/whatstk/), install it with pip:

```bash
pip install whatstk
```

Project has been tested in Python>=3.7.

### From source

Clone the project from the [official repository](https://github.com/lucasrodes/whatstk/) and install it locally 

```bash
git clone https://github.com/lucasrodes/whatstk.git
cd whatstk
pip install .
```

### Extensions

To use Google Drive or Chat Generation support, install the library along with the corresponding extensions:

```bash
pip install whatstk[gdrive]
```

```bash
pip install whatstk[generate]
```

Or install the full suite:

```bash
pip install whatstk[full]
```

### Develop

You can also install the version in development directly from github [develop](https://github.com/lucasrodes/whatstk/tree/develop) branch. 

```bash
pip install git+https://github.com/lucasrodes/whatstk.git@develop
```

Note: It requires [git](https://git-scm.com/) to be installed.

---

## Support

You can ask questions and join the development discussion on [GitHub](https://github.com/lucasrodes/whatstk). Use the [GitHub issues](https://github.com/lucasrodes/whatstk/issues) section to report bugs or request features and [GitHub discussions](https://github.com/lucasrodes/whatstk/issues) to open up broader discussions. You can also check the [project roadmap](https://github.com/lucasrodes/whatstk/projects/3).

For more details, refer to the [contribute section](contribute.md).

---

## Why this name, whatstk?

whatstk stands for "WhatsApp Toolkit", since the project was initially conceived as a python library to read and process WhatsApp chats. It currently only supports WhatsApp chats, but this might be extended in the future.