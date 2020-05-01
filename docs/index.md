# Table of Contents

* [whatstk](#.whatstk)
* [whatstk.plot](#.whatstk.plot)
  * [vis](#.whatstk.plot.vis)
* [whatstk.analysis](#.whatstk.analysis)
* [whatstk.analysis.base](#.whatstk.analysis.base)
  * [interventions](#.whatstk.analysis.base.interventions)
* [whatstk.core](#.whatstk.core)
* [whatstk.utils](#.whatstk.utils)
* [whatstk.utils.auto\_header](#.whatstk.utils.auto_header)
  * [extract\_header\_from\_text](#.whatstk.utils.auto_header.extract_header_from_text)
  * [issep](#.whatstk.utils.auto_header.issep)
  * [extract\_header\_format\_from\_lines](#.whatstk.utils.auto_header.extract_header_format_from_lines)
* [whatstk.utils.parser](#.whatstk.utils.parser)
  * [generate\_regex](#.whatstk.utils.parser.generate_regex)
  * [parse\_chat](#.whatstk.utils.parser.parse_chat)
  * [remove\_alerts\_from\_df](#.whatstk.utils.parser.remove_alerts_from_df)
* [whatstk.utils.exceptions](#.whatstk.utils.exceptions)
* [whatstk.objects](#.whatstk.objects)
  * [WhatsAppChat](#.whatstk.objects.WhatsAppChat)
    * [\_\_init\_\_](#.whatstk.objects.WhatsAppChat.__init__)
    * [from\_txt](#.whatstk.objects.WhatsAppChat.from_txt)
    * [to\_csv](#.whatstk.objects.WhatsAppChat.to_csv)
    * [\_\_len\_\_](#.whatstk.objects.WhatsAppChat.__len__)
    * [shape](#.whatstk.objects.WhatsAppChat.shape)

<a name=".whatstk"></a>
## whatstk

<a name=".whatstk.plot"></a>
## whatstk.plot

This import makes Python use 'print' as in Python 3.x

<a name=".whatstk.plot.vis"></a>
#### vis

```python
def vis(user_data, title)
```

Obtain Figure to plot using plotly.

Does not work if you use date_mode='hourweekday'.

**Arguments**:

- `user_data` _pandas.DataFrame_ - Input data.
- `title` _str_ - Title of figure.
  

**Returns**:

- `dict` - Figure.
  

**Examples**:

  
  ```python
  >>> from whatstk import WhatsAppChat, interventions
  >>> filename = 'path/to/samplechat.txt'
  >>> chat = WhatsAppChat.from_txt(filename)
  >>> counts = interventions(chat=chat, date_mode='date', msg_length=False)
  >>> counts_cumsum = counts.cumsum()
  >>> from plotly.offline import plot
  >>> from whatstk.plot import vis
  >>> plot(vis(counts_cumsum, 'cumulative number of messages sent per day'))
  ```

<a name=".whatstk.analysis"></a>
## whatstk.analysis

<a name=".whatstk.analysis.base"></a>
## whatstk.analysis.base

<a name=".whatstk.analysis.base.interventions"></a>
#### interventions

```python
def interventions(chat, date_mode='date', msg_length=False)
```

Get number of interventions per user per unit of time.

The unit of time can be chosen by means of argument `date_mode`.

**Examples**:

  Get counts of sent messages per user. Also cumulative.
  
  ```python
  >>> from whatstk import WhatsAppChat
  >>> from whatstk.analysis interventions
  >>> filename = 'path/to/samplechat.txt'
  >>> chat = WhatsAppChat.from_txt(filename)
  >>> counts = interventions(chat, date_mode='date', msg_length=False)
  >>> counts_cumsum = counts.cumsum()
  ```
  

**Arguments**:

- `chat` _WhatsAppChat_ - Object containing parsed WhatsApp chat.
- `date_mode` _str_ - Choose mode to group interventions by. Available modes are:
  - 'date': Grouped by particular date (year, month and day).
  - 'hour': Grouped by hours.
  - 'month': Grouped by months.
  - 'weekday': Grouped by weekday (i.e. monday, tuesday, ..., sunday).
  - 'hourweekday': Grouped by weekday and hour.
- `msg_length` _bool_ - Set to True to count the number of characters instead of number of messages sent.
  

**Returns**:

- `pandas.DataFrame` - DataFrame with shape NxU, where N: number of time-slots and U: number of users.
  

**Raises**:

- `ValueError` - if invalid mode is chosen.

<a name=".whatstk.core"></a>
## whatstk.core

For backwards compatibility

<a name=".whatstk.utils"></a>
## whatstk.utils

This module includes features which are in development

<a name=".whatstk.utils.auto_header"></a>
## whatstk.utils.auto\_header

<a name=".whatstk.utils.auto_header.extract_header_from_text"></a>
#### extract\_header\_from\_text

```python
def extract_header_from_text(text, encoding='utf-8')
```

Extract header from filename.

**Arguments**:

- `text` _str_ - Loaded chat as string (whole text).
- `encoding` _str, optional_ - Encoding to be used. Defaults to 'utf-8'.
  

**Returns**:

- `str` - Format extracted. None if no header was extracted.

<a name=".whatstk.utils.auto_header.issep"></a>
#### issep

```python
def issep(s)
```

Check if `s` is a separator character.

Separator can be one of the following: '.', ',', '-', '/', ':', '[' or ']'.

**Arguments**:

- `s` _str_ - Character to be checked.
  

**Returns**:

- `bool` - True if `s` is a separator, False otherwise.

<a name=".whatstk.utils.auto_header.extract_header_format_from_lines"></a>
#### extract\_header\_format\_from\_lines

```python
def extract_header_format_from_lines(lines)
```

Extract header from list of lines.

**Arguments**:

- `lines` _list_ - List of str, each element is a line of the loaded chat.
  

**Returns**:

- `str` - Format of the header.

<a name=".whatstk.utils.parser"></a>
## whatstk.utils.parser

<a name=".whatstk.utils.parser.generate_regex"></a>
#### generate\_regex

```python
def generate_regex(hformat)
```

Generate the appropriate regular expression from simplified syntax.

**Arguments**:

- `hformat` _str_ - Simplified syntax for the header.
  

**Returns**:

- `str` - Regular expression corresponding to the specified syntax.

<a name=".whatstk.utils.parser.parse_chat"></a>
#### parse\_chat

```python
def parse_chat(text, regex)
```

**Arguments**:

  text (str) Whole log chat text.
- `regex` _str_ - Regular expression
  

**Returns**:

- `pandas.DataFrame` - DataFrame with messages sent by users, index is the date the messages was sent.

<a name=".whatstk.utils.parser.remove_alerts_from_df"></a>
#### remove\_alerts\_from\_df

```python
def remove_alerts_from_df(r_x, df)
```

Tries to get rid of alert/notification messages

**Arguments**:

- `r_x` _str_ - Regular expression to detect whatsapp warnings.
- `df` _pandas.DataFrame_ - DataFrame with all interventions.
  

**Returns**:

- `pandas.DataFrame` - Fixed version of input dataframe.

<a name=".whatstk.utils.exceptions"></a>
## whatstk.utils.exceptions

Library exceptions.

<a name=".whatstk.objects"></a>
## whatstk.objects

<a name=".whatstk.objects.WhatsAppChat"></a>
### WhatsAppChat

```python
class WhatsAppChat()
```

Use this class to load and play with your chat log.

<a name=".whatstk.objects.WhatsAppChat.__init__"></a>
#### \_\_init\_\_

```python
 | def WhatsAppChat.__init__(df)
```

Constructor.

<a name=".whatstk.objects.WhatsAppChat.from_txt"></a>
#### from\_txt

```python
 | @classmethod
 | def WhatsAppChat.from_txt(cls, filename, auto_header=True, hformat=None, encoding='utf-8')
```

Create instance from chat log txt file hosted locally.

**Arguments**:

  
- `filename` _str_ - Name to the txt chat log file.
- `auto_header` _bool_ - Set to True to detect header automatically, otherwise set to False. Defaults to True. If
  False, you have to provide a value to `hformat`.
- `hformat` _str_ - Format of the header. Check `whatstk.WhatsAppChat.prepare_df` docs.
- `encoding` _str_ - Required to load file. Default is 'utf-8'. Should be working. Report any incidence.
  

**Returns**:

- `WhatsAppChat` - Class instance with loaded and parsed chat.

<a name=".whatstk.objects.WhatsAppChat.to_csv"></a>
#### to\_csv

```python
 | def WhatsAppChat.to_csv(filename)
```

Save data as csv.

**Arguments**:

- `filename` _str_ - Name of file.

<a name=".whatstk.objects.WhatsAppChat.__len__"></a>
#### \_\_len\_\_

```python
 | def WhatsAppChat.__len__()
```

Get length of DataFrame

**Returns**:

- `int` - Instance length, defined as number of samples.

<a name=".whatstk.objects.WhatsAppChat.shape"></a>
#### shape

```python
 | @property
 | def WhatsAppChat.shape()
```

Get shape of DataFrame-formatted chat.

**Returns**:

- `tuple` - Shape.

