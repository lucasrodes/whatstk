# Table of Contents

* [whatstk](#.whatstk)
* [whatstk.plot](#.whatstk.plot)
  * [vis](#.whatstk.plot.vis)
* [whatstk.analysis](#.whatstk.analysis)
* [whatstk.analysis.base](#.whatstk.analysis.base)
  * [interventions](#.whatstk.analysis.base.interventions)
* [whatstk.core](#.whatstk.core)
  * [df\_from\_txt](#.whatstk.core.df_from_txt)
* [whatstk.utils](#.whatstk.utils)
* [whatstk.utils.auto\_header](#.whatstk.utils.auto_header)
  * [extract\_header\_from\_text](#.whatstk.utils.auto_header.extract_header_from_text)
  * [extract\_header\_format\_from\_lines](#.whatstk.utils.auto_header.extract_header_format_from_lines)
* [whatstk.utils.chat\_generation](#.whatstk.utils.chat_generation)
  * [ChatGenerator](#.whatstk.utils.chat_generation.ChatGenerator)
    * [\_\_init\_\_](#.whatstk.utils.chat_generation.ChatGenerator.__init__)
    * [generate\_messages](#.whatstk.utils.chat_generation.ChatGenerator.generate_messages)
    * [generate\_emojis](#.whatstk.utils.chat_generation.ChatGenerator.generate_emojis)
    * [generate\_timestamps](#.whatstk.utils.chat_generation.ChatGenerator.generate_timestamps)
    * [generate\_users](#.whatstk.utils.chat_generation.ChatGenerator.generate_users)
    * [generate\_df](#.whatstk.utils.chat_generation.ChatGenerator.generate_df)
    * [generate](#.whatstk.utils.chat_generation.ChatGenerator.generate)
  * [generate\_chats\_hformats](#.whatstk.utils.chat_generation.generate_chats_hformats)
* [whatstk.utils.hformat](#.whatstk.utils.hformat)
  * [is\_supported](#.whatstk.utils.hformat.is_supported)
  * [is\_supported\_verbose](#.whatstk.utils.hformat.is_supported_verbose)
  * [get\_supported\_hformats\_as\_list](#.whatstk.utils.hformat.get_supported_hformats_as_list)
  * [get\_supported\_hformats\_as\_dict](#.whatstk.utils.hformat.get_supported_hformats_as_dict)
* [whatstk.utils.parser](#.whatstk.utils.parser)
  * [generate\_regex](#.whatstk.utils.parser.generate_regex)
  * [parse\_chat](#.whatstk.utils.parser.parse_chat)
  * [remove\_alerts\_from\_df](#.whatstk.utils.parser.remove_alerts_from_df)
* [whatstk.utils.exceptions](#.whatstk.utils.exceptions)
  * [RegexError](#.whatstk.utils.exceptions.RegexError)
  * [HFormatError](#.whatstk.utils.exceptions.HFormatError)
* [whatstk.objects](#.whatstk.objects)
  * [WhatsAppChat](#.whatstk.objects.WhatsAppChat)
    * [\_\_init\_\_](#.whatstk.objects.WhatsAppChat.__init__)
    * [from\_txt](#.whatstk.objects.WhatsAppChat.from_txt)
    * [to\_txt](#.whatstk.objects.WhatsAppChat.to_txt)
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
  >>> from whatstk import df_from_txt
  >>> from whatstk.analysis import interventions
  >>> filename = 'path/to/samplechat.txt'
  >>> df = df_from_txt(filename)
  >>> counts = interventions(df=df, date_mode='date', msg_length=False)
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
def interventions(df=None, chat=None, date_mode='date', msg_length=False)
```

Get number of interventions per user per unit of time.

The unit of time can be chosen by means of argument `date_mode`.

**Examples**:

  Get counts of sent messages per user. Also cumulative.
  
  ```python
  >>> from whatstk import df_from_txt
  >>> from whatstk.analysis interventions
  >>> filename = 'path/to/samplechat.txt'
  >>> df = df_from_txt(filename)
  >>> counts = interventions(df=df, date_mode='date', msg_length=False)
  >>> counts_cumsum = counts.cumsum()
  ```
  

**Arguments**:

- `df` _pd.DataFrame_ - Chat as DataFrame.
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

<a name=".whatstk.core.df_from_txt"></a>
#### df\_from\_txt

```python
def df_from_txt(filename, auto_header=True, hformat=None, encoding='utf-8')
```

Load the chat log text file as a pandas.DataFrame.

**Arguments**:

  
- `filename` _str_ - Name to the txt chat log file.
- `auto_header` _bool_ - Set to True to detect header automatically, otherwise set to False. Defaults to True. If
  False, you have to provide a value to `hformat`.
- `hformat` _str_ - Format of the header. Check `whatstk.WhatsAppChat.prepare_df` docs.
- `encoding` _str_ - Required to load file. Default is 'utf-8'. Should be working. Report any incidence.
  

**Returns**:

- `pandas.DataFrame` - Chat in DataFrame format with following columns: date (index), username, message.
  

**Examples**:

  
  ```python
  >>>  from whatstk import df_from_txt
  >>> filename = 'path/to/chat.txt'
  >>> df = df_from_txt(filename)
  ```

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

<a name=".whatstk.utils.chat_generation"></a>
## whatstk.utils.chat\_generation

<a name=".whatstk.utils.chat_generation.ChatGenerator"></a>
### ChatGenerator

```python
class ChatGenerator()
```

Generate a chat.

<a name=".whatstk.utils.chat_generation.ChatGenerator.__init__"></a>
#### \_\_init\_\_

```python
 | def ChatGenerator.__init__(size, users=None, seed=100)
```

Instantiate ChatGenerator class.

**Arguments**:

- `size` _int_ - Number of messages to generate.
- `users` _list, optional_ - List with names of the users. Defaults to module variable USERS.

<a name=".whatstk.utils.chat_generation.ChatGenerator.generate_messages"></a>
#### generate\_messages

```python
 | def ChatGenerator.generate_messages()
```

Generate list of messages.

To generate sentences, Lorem Ipsum is used.

**Returns**:

- `list` - List with messages (as strings).

<a name=".whatstk.utils.chat_generation.ChatGenerator.generate_emojis"></a>
#### generate\_emojis

```python
 | def ChatGenerator.generate_emojis(k=1)
```

Generate random list of emojis.

Emojis are sampled from a list of `n` emojis and `k*n` empty strings.

**Arguments**:

- `k` _int, optional_ - Defaults to 20.
  

**Returns**:

- `list` - List with emojis

<a name=".whatstk.utils.chat_generation.ChatGenerator.generate_timestamps"></a>
#### generate\_timestamps

```python
 | def ChatGenerator.generate_timestamps(last=None)
```

Generate list of timestamps.

**Arguments**:

- `last` _datetime, optional_ - Datetime of last message. If `None`, defaults to current date.
  

**Returns**:

- `[type]` - [description]

<a name=".whatstk.utils.chat_generation.ChatGenerator.generate_users"></a>
#### generate\_users

```python
 | def ChatGenerator.generate_users()
```

Generate list of users.

**Returns**:

- `list` - List of name of the users sending the messages.

<a name=".whatstk.utils.chat_generation.ChatGenerator.generate_df"></a>
#### generate\_df

```python
 | def ChatGenerator.generate_df()
```

Generate random chat as DataFrame.

**Returns**:

- `pandas.DataFrame` - DataFrame with random messages.

<a name=".whatstk.utils.chat_generation.ChatGenerator.generate"></a>
#### generate

```python
 | def ChatGenerator.generate(filename=None, hformat=None)
```

Generate random chat as WhatsAppChat.

**Arguments**:

- `filename` _str_ - Set to a string name to export the generated chat. Must have txt format.
- `hformat` _str_ - Header format of the text to be generated. If None, defaults to '%y-%m-%d, %H:%M - %name:'.
  

**Returns**:

- `WhatsAppChat` - Chat with random messages.

<a name=".whatstk.utils.chat_generation.generate_chats_hformats"></a>
#### generate\_chats\_hformats

```python
def generate_chats_hformats(output_path, size=2000, hformats=None, verbose=False)
```

Generate a chat and export using given header format.

If no hformat specified, chat is generated & exported using all supported header formats.

**Arguments**:

- `output_path` _str_ - Path to directory to export all generated chats as txt.
- `size` _int, optional_ - Number of messages of the chat. Defaults to 2000.
- `hformats` _list, optional_ - List of header formats to use when exporting chat. If None,
  defaults to all supported header formats.
- `verbose` _bool_ - Set to True to print runtime messages.

<a name=".whatstk.utils.hformat"></a>
## whatstk.utils.hformat

<a name=".whatstk.utils.hformat.is_supported"></a>
#### is\_supported

```python
def is_supported(hformat)
```

Check if header `hformat` is currently supported.

**Arguments**:

- `hformat` _str_ - Header format.
  

**Returns**:

  tuple:
  - bool: True if header is supported.
  - bool: True if header is supported with `auto_header` feature.

<a name=".whatstk.utils.hformat.is_supported_verbose"></a>
#### is\_supported\_verbose

```python
def is_supported_verbose(hformat)
```

Check if header `hformat` is currently supported, manually and using `auto_header`.

Result is shown as a string.

**Arguments**:

- `hformat` _str_ - Information message.

<a name=".whatstk.utils.hformat.get_supported_hformats_as_list"></a>
#### get\_supported\_hformats\_as\_list

```python
def get_supported_hformats_as_list()
```

Get list of supported formats.

**Returns**:

- `list` - List with supported formats (as str).

<a name=".whatstk.utils.hformat.get_supported_hformats_as_dict"></a>
#### get\_supported\_hformats\_as\_dict

```python
def get_supported_hformats_as_dict()
```

Get dictionary with supported formats and relevant info.

**Returns**:

- `dict` - Dict with two elements, `format` (header format) and `auto_header` (if auto_header is supported).

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
  

**Raises**:

- `RegexError` - When provided regex could not match the text.

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

<a name=".whatstk.utils.exceptions.RegexError"></a>
### RegexError

```python
class RegexError(Exception)
```

To be raised when regex match is not possible.

<a name=".whatstk.utils.exceptions.HFormatError"></a>
### HFormatError

```python
class HFormatError(Exception)
```

To be raised when hformat could not be found.

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

<a name=".whatstk.objects.WhatsAppChat.to_txt"></a>
#### to\_txt

```python
 | def WhatsAppChat.to_txt(filename, hformat=None)
```

Export chat as txt file.

Usefull to export the chat to different formats.

**Arguments**:

- `hformat` _str, optional_ - Header format. Defaults to "%y-%m-%d, %H:%M - %name:".
- `filename` _str_ - Name of the file to export.

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

