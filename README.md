# [whatstk](http://lucasrodes.github.io/whatstk)

![Package version](https://img.shields.io/badge/whatstk-v0.1.11-brightgreen.svg?style=for-the-badge)

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

#### Obtain a dataframe from your chat log file

Export your WhatsApp chat using your phone and send it to your computer. Make sure to choose the correct format of 
the header. In the example here, the header (see [example.txt](chats/example.txt)) uses the syntax '%d.%m.%y, %H:%M -
 %name:'. Header example: `07.08.2016, 19:30 - Misty:`
 
 
```python
from whatstk.core import WhatsAppChat

filename = 'chats/example.txt'
# [IMPORTANT] Choose header format accordingly
hformat = '%d.%m.%y, %H:%M - %name:'
chat = WhatsAppChat.from_txt(filename, hformat)
```

#### Plot the cumulative messages sent by day
Once you have your chat object, you can visualise the cumulative number of messages sent per day using the following 
code

```python
from whatstk.core import interventions
counts = interventions(chat, 'date', msg_length=False)
counts_cumsum = counts.cumsum()

# Plot result
from plotly.offline import plot
from whatstk.plot import vis
plot(vis(counts_cumsum, 'cumulative characters sent per day'))
```
![](assets/example1.png)

*Note*: More examples to come soon.

### Contribute
We are very open to have collaborators. You can freely fork and issue a pull request with your updates!
For other issues/bugs/suggestions, please report it as an issue or [text me](mailto:lucasrg@kth.se).