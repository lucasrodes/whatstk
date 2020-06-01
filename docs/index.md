# Table of Contents

* [whatstk](#.whatstk)
* [whatstk.plot](#.whatstk.plot)
  * [vis](#.whatstk.plot.vis)
* [whatstk.analysis](#.whatstk.analysis)
* [whatstk.analysis.responses](#.whatstk.analysis.responses)
  * [response\_matrix](#.whatstk.analysis.responses.response_matrix)
* [whatstk.analysis.base](#.whatstk.analysis.base)
  * [get\_interventions\_count](#.whatstk.analysis.base.get_interventions_count)
* [whatstk.graph](#.whatstk.graph)
* [whatstk.graph.figures](#.whatstk.graph.figures)
* [whatstk.graph.figures.heatma](#.whatstk.graph.figures.heatma)
  * [fig\_heatmap](#.whatstk.graph.figures.heatma.fig_heatmap)
* [whatstk.graph.figures.boxplot](#.whatstk.graph.figures.boxplot)
  * [fig\_boxplot\_msglen](#.whatstk.graph.figures.boxplot.fig_boxplot_msglen)
* [whatstk.graph.figures.utils](#.whatstk.graph.figures.utils)
  * [hex\_color\_palette](#.whatstk.graph.figures.utils.hex_color_palette)
* [whatstk.graph.figures.scatter](#.whatstk.graph.figures.scatter)
  * [fig\_scatter\_time](#.whatstk.graph.figures.scatter.fig_scatter_time)
* [whatstk.graph.figures.base](#.whatstk.graph.figures.base)
  * [FigureBuilder](#.whatstk.graph.figures.base.FigureBuilder)
    * [\_\_init\_\_](#.whatstk.graph.figures.base.FigureBuilder.__init__)
    * [usernames](#.whatstk.graph.figures.base.FigureBuilder.usernames)
    * [user\_color\_mapping](#.whatstk.graph.figures.base.FigureBuilder.user_color_mapping)
    * [user\_msg\_length\_boxplot](#.whatstk.graph.figures.base.FigureBuilder.user_msg_length_boxplot)
    * [user\_interventions\_count\_linechart](#.whatstk.graph.figures.base.FigureBuilder.user_interventions_count_linechart)
    * [user\_message\_responses\_flow](#.whatstk.graph.figures.base.FigureBuilder.user_message_responses_flow)
    * [user\_message\_responses\_heatmap](#.whatstk.graph.figures.base.FigureBuilder.user_message_responses_heatmap)
* [whatstk.graph.figures.sanke](#.whatstk.graph.figures.sanke)
  * [fig\_sankey](#.whatstk.graph.figures.sanke.fig_sankey)
* [whatstk.core](#.whatstk.core)
  * [df\_from\_txt](#.whatstk.core.df_from_txt)
  * [df\_from\_multiple\_txt](#.whatstk.core.df_from_multiple_txt)
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
* [whatstk.utils.chat\_merge](#.whatstk.utils.chat_merge)
  * [merge\_chats](#.whatstk.utils.chat_merge.merge_chats)
* [whatstk.utils.hformat](#.whatstk.utils.hformat)
  * [is\_supported](#.whatstk.utils.hformat.is_supported)
  * [is\_supported\_verbose](#.whatstk.utils.hformat.is_supported_verbose)
  * [get\_supported\_hformats\_as\_list](#.whatstk.utils.hformat.get_supported_hformats_as_list)
  * [get\_supported\_hformats\_as\_dict](#.whatstk.utils.hformat.get_supported_hformats_as_dict)
* [whatstk.utils.parser](#.whatstk.utils.parser)
  * [generate\_regex](#.whatstk.utils.parser.generate_regex)
  * [parse\_chat](#.whatstk.utils.parser.parse_chat)
  * [add\_schema](#.whatstk.utils.parser.add_schema)
  * [remove\_alerts\_from\_df](#.whatstk.utils.parser.remove_alerts_from_df)
* [whatstk.utils.utils](#.whatstk.utils.utils)
* [whatstk.utils.exceptions](#.whatstk.utils.exceptions)
  * [RegexError](#.whatstk.utils.exceptions.RegexError)
  * [HFormatError](#.whatstk.utils.exceptions.HFormatError)
* [whatstk.objects](#.whatstk.objects)
  * [WhatsAppChat](#.whatstk.objects.WhatsAppChat)
    * [\_\_init\_\_](#.whatstk.objects.WhatsAppChat.__init__)
    * [from\_txt](#.whatstk.objects.WhatsAppChat.from_txt)
    * [from\_multiple\_txt](#.whatstk.objects.WhatsAppChat.from_multiple_txt)
    * [merge](#.whatstk.objects.WhatsAppChat.merge)
    * [rename\_users](#.whatstk.objects.WhatsAppChat.rename_users)
    * [to\_txt](#.whatstk.objects.WhatsAppChat.to_txt)
    * [to\_csv](#.whatstk.objects.WhatsAppChat.to_csv)
    * [\_\_len\_\_](#.whatstk.objects.WhatsAppChat.__len__)
    * [shape](#.whatstk.objects.WhatsAppChat.shape)

<a name=".whatstk"></a>
## whatstk

Python wrapper and analysis tools for WhatsApp chats.

This library provides a powerful wrapper for multiple Languages and OS. In addition, analytics tools are provided.

<a name=".whatstk.plot"></a>
## whatstk.plot

Plot utils.

<a name=".whatstk.plot.vis"></a>
#### vis

```python
def vis(user_data, title)
```

See method `vis_scatter_time`.

**Arguments**:

- `user_data` _pandas.DataFrame_ - Input data.
- `title` _str_ - Title of figure.
  

**Returns**:

- `dict` - Figure.

<a name=".whatstk.analysis"></a>
## whatstk.analysis

Analytics tools.

<a name=".whatstk.analysis.responses"></a>
## whatstk.analysis.responses

Get infor regarding responses between users.

<a name=".whatstk.analysis.responses.response_matrix"></a>
#### response\_matrix

```python
def response_matrix(df=None, chat=None, zero_own=True, norm=NORMS.ABSOLUTE)
```

Get response matrix for given chat.

Obtains a DataFrame of shape [n_users, n_users] counting the number of responses between members. Responses can be
counted in different ways, e.g. using absolute values or normalised values. Responses are counted based solely on
consecutive messages. That is, if user_i sends a message right after user_j, it will be counted as a response from
user_i to user_j.

Axis 0 lists senders and axis 1 lists receivers. That is, the value in cell (i, j) denotes the number of times
user_i responded to a message from user_j.

**Arguments**:

- `df` _pandas.DataFrame, optional_ - Chat. Defaults to None.
- `chat` _WhatsAppChat, optional_ - Chat. Defaults to None.
- `zero_own` _bool, optional_ - Set to True to avoid counting own responses. Defaults to True.
- `norm` _str, optional_ - Specifies the type of normalization used for reponse count.
  

**Returns**:

- `pandas.DataFrame` - Response matrix.
  

**Examples**:

  
  Get absolute count on responses (consecutive messages) between users
  
  ```python
  >>> from whatstk import df_from_txt
  >>> from whatstk.analysis.responses import response_matrix
  >>> df = df_from_txt(path)
  >>> responses = response_matrix(df)
  ```
  
  Get percentage of responses received for each user.
  
  ```python
  >>> from whatstk import df_from_txt
  >>> from whatstk.analysis.responses import response_matrix
  >>> df = df_from_txt(path)
  >>> responses = response_matrix(df, norm='receive)
  ```

<a name=".whatstk.analysis.base"></a>
## whatstk.analysis.base

Base analysis tools.

<a name=".whatstk.analysis.base.get_interventions_count"></a>
#### get\_interventions\_count

```python
def get_interventions_count(df=None, chat=None, date_mode='date', msg_length=False, cummulative=False)
```

Get number of interventions per user per unit of time.

The unit of time can be chosen by means of argument `date_mode`.

**Examples**:

  
  Get counts of sent messages per user. Also cumulative.
  
  ```python
  >>> from whatstk import df_from_txt
  >>> from whatstk.analysis get_interventions_count
  >>> filename = 'path/to/samplechat.txt'
  >>> df = df_from_txt(filename)
  >>> counts = get_interventions_count(df=df, date_mode='date', msg_length=False)
  >>> counts_cumsum = counts.cumsum()
  ```
  

**Arguments**:

- `df` _pandas.DataFrame_ - Chat as DataFrame.
- `chat` _WhatsAppChat_ - Object containing parsed WhatsApp chat.
- `date_mode` _str, optional_ - Choose mode to group interventions by. Defaults to 'date'. Available modes are:
  - 'date': Grouped by particular date (year, month and day).
  - 'hour': Grouped by hours.
  - 'month': Grouped by months.
  - 'weekday': Grouped by weekday (i.e. monday, tuesday, ..., sunday).
  - 'hourweekday': Grouped by weekday and hour.
- `msg_length` _bool, optional_ - Set to True to count the number of characters instead of number of messages sent.
- `cummulative` _bool, optional_ - Set to True to obtain commulative counts.
  

**Returns**:

- `pandas.DataFrame` - DataFrame with shape NxU, where N: number of time-slots and U: number of users.
  

**Raises**:

- `ValueError` - if `date_mode` value is not supported.

<a name=".whatstk.graph"></a>
## whatstk.graph

Plot tools using plotly.

<a name=".whatstk.graph.figures"></a>
## whatstk.graph.figures

Build Plotly compatible Figures.

<a name=".whatstk.graph.figures.heatma"></a>
## whatstk.graph.figures.heatma

Heatmap plot figures.

<a name=".whatstk.graph.figures.heatma.fig_heatmap"></a>
#### fig\_heatmap

```python
def fig_heatmap(df_matrix, title="")
```

Generate heatmap figure from NxN matrix.

**Arguments**:

- `df_matrix` _pandas.DataFrame_ - Matrix as DataFrame. Index values and column values must be equal.
- `title` _str_ - Title of plot. Defaults to "".
  

**Returns**:

- `[type]` - [description]

<a name=".whatstk.graph.figures.boxplot"></a>
## whatstk.graph.figures.boxplot

Boxplot figures.

<a name=".whatstk.graph.figures.boxplot.fig_boxplot_msglen"></a>
#### fig\_boxplot\_msglen

```python
def fig_boxplot_msglen(df, username_to_color=None, title="", xlabel=None)
```

Visualize boxplot.

**Arguments**:

- `df` _pandas.DataFrame_ - Chat data.
  username_to_color (dictm optional). Dictionary mapping username to color. Defaults to None.
- `title` _str, optional_ - Title for plot. Defaults to "".
- `xlabel` _str, optional_ - x-axis label title. Defaults to None.
  

**Returns**:

- `dict` - Figure.

<a name=".whatstk.graph.figures.utils"></a>
## whatstk.graph.figures.utils

Utils for library plots.

<a name=".whatstk.graph.figures.utils.hex_color_palette"></a>
#### hex\_color\_palette

```python
def hex_color_palette(n_colors)
```

Get palette of `n_colors` color hexadecimal codes.

**Arguments**:

- `n_colors` _int_ - Size of the color palette.

<a name=".whatstk.graph.figures.scatter"></a>
## whatstk.graph.figures.scatter

Scatter plot figures.

<a name=".whatstk.graph.figures.scatter.fig_scatter_time"></a>
#### fig\_scatter\_time

```python
def fig_scatter_time(user_data, username_to_color=None, title="", xlabel=None)
```

Obtain Figure to plot using plotly.

`user_data` must be a pandas.DataFrame with timestamps as index and a column for each user.

Note: Does not work with output of `get_interventions_count` if date_mode='hourweekday'.

**Arguments**:

- `user_data` _pandas.DataFrame_ - Input data. Shape nrows x ncols, where nrows = number of timestaps and
  ncols = number of users.
  username_to_color (dictm optional). Dictionary mapping username to color. Defaults to None.
- `title` _str, optional_ - Title of figure. Defaults to "".
- `xlabel` _str, optional_ - x-axis label title. Defaults to None.
  

**Returns**:

- `dict` - Figure.

<a name=".whatstk.graph.figures.base"></a>
## whatstk.graph.figures.base

Build plotly-compatible figures.

<a name=".whatstk.graph.figures.base.FigureBuilder"></a>
### FigureBuilder

```python
class FigureBuilder()
```

Generate a variety of figures from your loaded chat.

<a name=".whatstk.graph.figures.base.FigureBuilder.__init__"></a>
#### \_\_init\_\_

```python
 | def FigureBuilder.__init__(df=None, chat=None)
```

Constructor.

**Arguments**:

- `df` _pandas.DataFrame, optional_ - Chat data. Atribute `df` of a chat loaded using WhatsAppChat. Defaults to
  None.
- `chat` _WhatsAppChat, optional_ - Chat data. Object obtained when chat loaded using WhatsAppChat. Defaults to
  None.
- `title` _str, optional_ - Figure title. Defaults to "".
- `xlabel` _str, optional_ - x-axis label. Defaults to None.

<a name=".whatstk.graph.figures.base.FigureBuilder.usernames"></a>
#### usernames

```python
 | @property
 | def FigureBuilder.usernames()
```

Get list with users available in given chat.

**Returns**:

- `list` - List with usernames available in chat DataFrame.

<a name=".whatstk.graph.figures.base.FigureBuilder.user_color_mapping"></a>
#### user\_color\_mapping

```python
 | @property
 | def FigureBuilder.user_color_mapping()
```

Build mapping between user and color.

**Returns**:

- `dict` - Mapping username -> color (rgb).

<a name=".whatstk.graph.figures.base.FigureBuilder.user_msg_length_boxplot"></a>
#### user\_msg\_length\_boxplot

```python
 | def FigureBuilder.user_msg_length_boxplot(title="User message length", xlabel="User")
```

Get boxplot of message length of all users.

**Returns**:

- `dict` - Dictionary with data and layout. Plotly compatible
- `title` _str, optional_ - Title for plot. Defaults to "User message length".
- `xlabel` _str, optional_ - x-axis label title. Defaults to "User".
  

**Examples**:

  
  ```python
  >>> from whatstk import df_from_txt
  >>> from whatstk.graph import plot, FigureBuilder
  >>> filename = 'path/to/samplechat.txt'
  >>> df = df_from_txt(filename)
  >>> fig = FigureBuilder(df).user_msg_length_boxplot()
  >>> plot(fig)
  ```

<a name=".whatstk.graph.figures.base.FigureBuilder.user_interventions_count_linechart"></a>
#### user\_interventions\_count\_linechart

```python
 | def FigureBuilder.user_interventions_count_linechart(date_mode='date', msg_length=False, cummulative=False, title="User interventions count", xlabel="Date/Time")
```

Plot number of user interventions over time.

**Arguments**:

- `date_mode` _str, optional_ - Choose mode to group interventions by. Defaults to 'date'. Available modes are:
  - 'date': Grouped by particular date (year, month and day).
  - 'hour': Grouped by hours.
  - 'month': Grouped by months.
  - 'weekday': Grouped by weekday (i.e. monday, tuesday, ..., sunday).
  - 'hourweekday': Grouped by weekday and hour.
- `msg_length` _bool, optional_ - Set to True to count the number of characters instead of number of messages
  sent.
- `cummulative` _bool, optional_ - Set to True to obtain commulative counts.
- `title` _str, optional_ - Title for plot. Defaults to "User interventions count".
- `xlabel` _str, optional_ - x-axis label title. Defaults to "Date/Time".
  

**Returns**:

- `dict` - Dictionary with data and layout. Plotly compatible
  

**Examples**:

  
  ```python
  >>> from whatstk import df_from_txt
  >>> from whatstk.graph import plot, FigureBuilder
  >>> filename = 'path/to/samplechat.txt'
  >>> df = df_from_txt(filename)
  >>> fig = FigureBuilder(df).user_interventions_count_linechart(cummulative=True)
  >>> plot(fig)
  ```

<a name=".whatstk.graph.figures.base.FigureBuilder.user_message_responses_flow"></a>
#### user\_message\_responses\_flow

```python
 | def FigureBuilder.user_message_responses_flow(title="Message flow")
```

Get the flow of message responses.

A response is from user X to user Y happens if user X sends a message right after message Y does.

This method generates a plotly-ready figure (as a dictionary) using Sankey diagram.

**Arguments**:

- `title` _str, optional_ - Title for plot. Defaults to "Message flow".
  

**Returns**:

- `dict` - Dictionary with data and layout. Plotly compatible
  

**Examples**:

  
  ```python
  >>> from whatstk import df_from_txt
  >>> from whatstk.graph import plot, FigureBuilder
  >>> filename = 'path/to/samplechat.txt'
  >>> df = df_from_txt(filename)
  >>> fig = FigureBuilder(df).user_message_responses_flow()
  >>> plot(fig)
  ```

<a name=".whatstk.graph.figures.base.FigureBuilder.user_message_responses_heatmap"></a>
#### user\_message\_responses\_heatmap

```python
 | def FigureBuilder.user_message_responses_heatmap(title="Response matrix")
```

Get the response matrix heatmap.

A response is from user X to user Y happens if user X sends a message right after message Y does.

This method generates a plotly-ready figure (as a dictionary) using Heatmaps.

**Arguments**:

- `title` _str, optional_ - Title for plot. Defaults to "Response matrix".
  

**Returns**:

- `dict` - Dictionary with data and layout. Plotly compatible
  

**Examples**:

  
  ```python
  >>> from whatstk import df_from_txt
  >>> from whatstk.graph import plot, FigureBuilder
  >>> filename = 'path/to/samplechat.txt'
  >>> df = df_from_txt(filename)
  >>> fig = FigureBuilder(df).user_message_responses_heatmap()
  >>> plot(fig)
  ```

<a name=".whatstk.graph.figures.sanke"></a>
## whatstk.graph.figures.sanke

Sankey plot figures.

<a name=".whatstk.graph.figures.sanke.fig_sankey"></a>
#### fig\_sankey

```python
def fig_sankey(label, color, source, target, value, title="")
```

Generate sankey image.

**Arguments**:

- `label` _list_ - List with node labels.
- `color` _list_ - List with node colors.
- `source` _list_ - List with link source id.
- `target` _list_ - List with linke target id.
- `value` _list_ - List with link value.
- `title` _str, optional_ - Title. Defaults to "".
  

**Returns**:

- `dict` - Figure as dictionary.

<a name=".whatstk.core"></a>
## whatstk.core

Text to dataframe methods.

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

<a name=".whatstk.core.df_from_multiple_txt"></a>
#### df\_from\_multiple\_txt

```python
def df_from_multiple_txt(filenames, auto_header=None, hformat=None, encoding='utf-8')
```

Load the chat log text file as a pandas.DataFrame using multiple txt sources.

The merge is done time-wise. See method whatstk.utils.chat_merge.merge_chats for more details on the merge
impementation.

**Arguments**:

  
- `filenames` _list_ - List with names of the files, e.g. ['part1.txt', 'part2.txt', ...].
- `auto_header` _list, optional_ - Whether auto_header should be performed (for each file, choose True/False).
  Defaults to True for all files.
- `hformat` _list, optional_ - List with the hformat to be used per each file. Defaults to None.
- `encoding` _str, optional_ - Encoding to use when loading file. Defaults to 'utf-8'.
  

**Returns**:

- `pandas.DataFrame` - Chat in DataFrame format with following columns: date (index), username, message.
  

**Examples**:

  
  ```python
  >>>  from whatstk import df_from_multiple_txt
  >>> filename1 = 'path/to/chat1.txt'
  >>> filename2 = 'path/to/chat2.txt'
  >>> df = df_from_multiple_txt([filename1, filename2])
  ```

<a name=".whatstk.utils"></a>
## whatstk.utils

This module includes features which are in development.

<a name=".whatstk.utils.auto_header"></a>
## whatstk.utils.auto\_header

Detect header from chat.

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

Chat generation utils.

Use this module functions to generate chats.

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
- `seed` _int, optional_ - Seed for random processes. Defaults to 100.

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
 | def ChatGenerator.generate_df(last_timestamp=None)
```

Generate random chat as DataFrame.

**Arguments**:

- `last_timestamp` _datetime, optional_ - Datetime of last message. If `None`, defaults to current date.
  

**Returns**:

- `pandas.DataFrame` - DataFrame with random messages.

<a name=".whatstk.utils.chat_generation.ChatGenerator.generate"></a>
#### generate

```python
 | def ChatGenerator.generate(filename=None, hformat=None, last_timestamp=None)
```

Generate random chat as WhatsAppChat.

**Arguments**:

- `filename` _str_ - Set to a string name to export the generated chat. Must have txt format.
- `hformat` _str_ - Header format of the text to be generated. If None, defaults to '%y-%m-%d, %H:%M - %name:'.
- `last_timestamp` _datetime, optional_ - Datetime of last message. If `None`, defaults to current date.
  

**Returns**:

- `WhatsAppChat` - Chat with random messages.

<a name=".whatstk.utils.chat_merge"></a>
## whatstk.utils.chat\_merge

Merge utils.

<a name=".whatstk.utils.chat_merge.merge_chats"></a>
#### merge\_chats

```python
def merge_chats(dfs)
```

Merge several chats into a single one.

Can come in handy when you have old exports and new ones, and both have relevant data.

**Arguments**:

- `dfs` _list_ - List with the chats as DataFrames.
  

**Returns**:

- `pandas.DataFrame` - Merged chat.

<a name=".whatstk.utils.hformat"></a>
## whatstk.utils.hformat

Header format utils.

Example: Check if header is available.

```python
>>> from whatstk.utils.hformat import is_supported
>>> is_supported('%y-%m-%d, %H:%M:%S - %name:')
(True, True)
```

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

Check if header `hformat` is currently supported (both manually and using `auto_header`).

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

Parser utils.

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

Parse chat using given RegEx.

**Arguments**:

  text (str) Whole log chat text.
- `regex` _str_ - Regular expression
  

**Returns**:

- `pandas.DataFrame` - DataFrame with messages sent by users, index is the date the messages was sent.
  

**Raises**:

- `RegexError` - When provided regex could not match the text.

<a name=".whatstk.utils.parser.add_schema"></a>
#### add\_schema

```python
def add_schema(df)
```

Add default chat schema to df.

**Arguments**:

- `df` _pandas.DataFrame_ - Chat dataframe.
  

**Returns**:

- `pandas.DataFrame` - Chat dataframe with correct dtypes.

<a name=".whatstk.utils.parser.remove_alerts_from_df"></a>
#### remove\_alerts\_from\_df

```python
def remove_alerts_from_df(r_x, df)
```

Try to get rid of alert/notification messages.

**Arguments**:

- `r_x` _str_ - Regular expression to detect whatsapp warnings.
- `df` _pandas.DataFrame_ - DataFrame with all interventions.
  

**Returns**:

- `pandas.DataFrame` - Fixed version of input dataframe.

<a name=".whatstk.utils.utils"></a>
## whatstk.utils.utils

Utils.

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

Library objects.

Most important one is `WhatsAppChat`.

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
- `auto_header` _bool_ - Set to True to detect header automatically, otherwise set to False. Defaults to True.
  If False, you have to provide a value to `hformat`.
- `hformat` _str_ - Format of the header. Check `whatstk.WhatsAppChat.prepare_df` docs.
- `encoding` _str_ - Required to load file. Default is 'utf-8'. Should be working. Report any incidence.
  

**Returns**:

- `WhatsAppChat` - Class instance with loaded and parsed chat.

<a name=".whatstk.objects.WhatsAppChat.from_multiple_txt"></a>
#### from\_multiple\_txt

```python
 | @classmethod
 | def WhatsAppChat.from_multiple_txt(cls, filenames, auto_header=None, hformat=None, encoding='utf-8')
```

Load a WhatsAppChat instance from multiple sources.

**Arguments**:

- `filenames` _list_ - List with names of the files, e.g. ['part1.txt', 'part2.txt', ...].
- `auto_header` _list, optional_ - Whether auto_header should be performed (for each file, choose True/False).
  Defaults to True for all files.
- `hformat` _list, optional_ - List with the hformat to be used per each file. Defaults to None.
- `encoding` _str, optional_ - Encoding to use when loading file. Defaults to 'utf-8'.

<a name=".whatstk.objects.WhatsAppChat.merge"></a>
#### merge

```python
 | def WhatsAppChat.merge(chat, rename_users=None)
```

Merge current instance with `chat`.

**Arguments**:

- `chat` _WhatsAppChat_ - Another chat.
- `rename_users` _dict_ - Dictionary mapping old names to new names,
- `example` - {'John':['Jon', 'J'], 'Ray': ['Raymond']} will map 'Jon' and 'J' to
  'John', and 'Raymond' to 'Ray'.
  

**Returns**:

- `WhatsAppChat` - Merged chat.

<a name=".whatstk.objects.WhatsAppChat.rename_users"></a>
#### rename\_users

```python
 | def WhatsAppChat.rename_users(mapping)
```

Rename users.

**Arguments**:

- `mapping` _dict_ - Dictionary mapping old names to new names, example: {'John':['Jon', 'J'], 'Ray':
  ['Raymond']} will map 'Jon' and 'J' to 'John', and 'Raymond' to 'Ray'.
  

**Returns**:

- `pandas.DataFrame` - DataFrame with users renamed according to `mapping`.
  

**Raises**:

- `ValueError` - Raised if mapping is not correct.

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

Get length of DataFrame.

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

