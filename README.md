# [whatstk](http://lucasrodes.github.io/whatstk)

![Package version](https://img.shields.io/badge/whatstk-v0.1.7-brightgreen.svg?style=for-the-badge)

[![Build Status](https://travis-ci.com/lucasrodes/whatstk.svg?branch=develop)](https://travis-ci.com/lucasrodes/whatstk)[![GitHub license](https://img.shields.io/github/license/lucasrodes/whatstk.svg)](https://github.com/baldassarreFe/lucasrodes/blob/master/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/lucasrodes/whatstk.svg)](https://github.com/lucasrodes/whatstk/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/lucasrodes/whatstk.svg)](https://github.com/lucasrodes/whatstk/network)

whatstk is a Python module for WhatsApp chat group analysis and distributed under the GPL-3.0 license.

The project was started in December 2016 by [lucasrodes](https://github.com/lucasrodes) and [albertaparicio](https://github.com/albertaparicio).

:star: Please **star** our project if you found it interesting to **keep us motivated** :smiley:!

### Installation

Tested on Python 3.7

```
pip install whatstk
```

### Getting Started

#### Cumulative messages sent by day

```python
from whatstk.core import WhatsAppChat, interventions
from whatstk.plot import vis
from plotly.offline import plot

filename = 'chats/example.txt'
hformat = '%d.%m.%y, %H:%M - %name:'

chat = WhatsAppChat.from_txt(filename, hformat)
counts = interventions(chat, 'date', msg_length=False)
counts_cumsum = counts.cumsum()
plot(vis(counts_cumsum, 'cummulative characters sent per day'))
```
![](assets/example1.png)

*Note*: More examples to come soon.

### Contribute
We are very open to have collaborators. You can freely fork and issue a pull request with your updates!
For other issues/bugs/suggestions, please report it as an issue or [text me](mailto:lucasrg@kth.se).