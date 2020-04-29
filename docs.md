
# whatstk

<a name=".whatstk"></a>
## whatstk

<a name=".whatstk.learn"></a>
## whatstk.learn

This module contains analysis tools

<a name=".whatstk.learn.som"></a>
## whatstk.learn.som

<a name=".whatstk.learn.som.SelfOrganizingMap.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(train_data, num_units, sigma_initial, num_epochs=100, learning_rate_initial=1, topology="line")
```

Train data

<a name=".whatstk.learn.som.SelfOrganizingMap.train"></a>
#### train

```python
 | train()
```

Get list of users

<a name=".whatstk.learn.som.TopologicalMap.get_neighbour_levels"></a>
#### get\_neighbour\_levels

```python
 | get_neighbour_levels(win_idx, sigma)
```

Simple line

<a name=".whatstk.learn.utils"></a>
## whatstk.learn.utils

<a name=".whatstk.learn.utils.preprocess"></a>
#### preprocess

```python
preprocess(dataframe)
```

Center each dimension

<a name=".whatstk.learn.rnn"></a>
## whatstk.learn.rnn

<a name=".whatstk.learn.rnn.RNN.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(text, n_hidden_states=100, learning_rate=.0005, gamma=0.9, epsilon=1e-20, sequence_length=25, sigma=0.01)
```

**Arguments**:

- `text`: Text to train on, as a string
- `n_hidden_states`: number of hidden units
- `learning_rate`: learning rate
- `sequence_length`: Length of the generated strings
- `sigma`: Standard deviation used in the initialization of the model parameters

<a name=".whatstk.learn.rnn.RNN.forward_pass"></a>
#### forward\_pass

```python
 | forward_pass(input_sequence, previous_state)
```

Predicts output sequence given an input sequence (matrix one-hot encoding)

**Arguments**:

- `input_sequence`: Input text sequence as a one-hot encoded matrix alphabet_size x seq_length

**Returns**:

output_estimate: Next character probability matrix (alphabet_size x sequence_length),
hidden_states: Hidden states (hidden_units x sequence_length)

<a name=".whatstk.learn.rnn.RNN.compute_cost"></a>
#### compute\_cost

```python
 | @staticmethod
 | compute_cost(output_estimate, output_sequence)
```

Computes cost between predicted and targeted output sequence

**Arguments**:

- `output_estimate`: Predicted sequence, as one-hot matrix (K x seq_length)
- `output_sequence`: Targeted sequence, as one-hot matrix (K x seq_length)

**Returns**:

Cross-entropy loss

<a name=".whatstk.learn.rnn.RNN.compute_grad"></a>
#### compute\_grad

```python
 | compute_grad(param_names, input_sequence, hidden_states, output_estimate, output_sequence, previous_state)
```

Computes the gradient from the parameters listed in grad_names

**Arguments**:

- `param_names`: List of strings containing the name of the model parameters to find the gradient from
- `input_sequence`: Input sequence, as one-hot matrix (alphabet_size x sequence_length)
- `hidden_states`: Activations in the hidden layer (hidden_units x sequence_length)
- `output_estimate`: Next sequence prediction, as one-hot matrix (alphabet_size x sequence_length)
- `output_sequence`: Targeted sequence, as one-hot matrix (alphabet_size x sequence_length)

**Returns**:

Dictionary containing the gradient from the model parameters specified by grad_names

<a name=".whatstk.learn.rnn.RNN.backward_pass"></a>
#### backward\_pass

```python
 | backward_pass(input_sequence, hidden_states, output_estimate, output_sequence, previous_state)
```

Computes the gradient of all the model parameters

**Arguments**:

- `input_sequence`: Input sequence, as one-hot matrix (alphabet_size x sequence_length)
- `hidden_states`: Activations in the hidden layer (hidden_units x sequence_length)
- `output_estimate`: Next sequence prediction, as one-hot matrix (alphabet_size x sequence_length)
- `output_sequence`: Targeted sequence, as one-hot matrix (alphabet_size x sequence_length)
- `previous_state`: Previous state, hidden units x 1

**Returns**:



<a name=".whatstk.learn.rnn.RNN.adagrad_update"></a>
#### adagrad\_update

```python
 | adagrad_update(grads, m)
```

Ada-Grad update rule

**Arguments**:

- `grads`: Gradients of the model parameters
- `m`: 

**Returns**:



<a name=".whatstk.learn.rnn.RNN.generate_sequence"></a>
#### generate\_sequence

```python
 | generate_sequence(epochs=100)
```

generates a sequence based on the sentences from a user

**Arguments**:

- `epochs`: number of epochs to train the model

**Returns**:



<a name=".whatstk.learn.rnn.RNN.get_data"></a>
#### get\_data

```python
 | get_data(idx)
```

Obtains the idx-th input and output sentences in one-hot-encoded matrices format

**Arguments**:

- `idx`: Index of the input-output pair to get

**Returns**:

Two matrices, one for the input sentence and the other for the output sentence, both K x seq_length

<a name=".whatstk.learn.rnn.RNN.sample_from_distrib"></a>
#### sample\_from\_distrib

```python
 | sample_from_distrib(p)
```

Samples from probability distribution

**Arguments**:

- `p`: Probability distribution vector, p[k] denotes the probability of the k-th value

**Returns**:

An integer {1, 2, ...,k} sampled from the p

<a name=".whatstk.learn.rnn.TestGradient.run"></a>
#### run

```python
 | run()
```

Executes the code, checking if the analytical gradient of rnn is well implemented

**Returns**:

Relative L1 loss between analytical and numerical gradients

<a name=".whatstk.learn.rnn.TestGradient.gradient_check"></a>
#### gradient\_check

```python
 | gradient_check(param_names, input_sequence, hidden_states, output_estimate, output_sequence, init_state)
```

Computes the error between the numerical and analytical gradients

**Arguments**:

- `param_names`: List of strings containing the name of the model parameters to find the gradient from
- `input_sequence`: Input sequence, as one-hot matrix (alphabet_size x sequence_length)
- `hidden_states`: Activations in the hidden layer (hidden_units x sequence_length)
- `output_estimate`: Next sequence prediction, as one-hot matrix (alphabet_size x sequence_length)
- `output_sequence`: Targeted sequence, as one-hot matrix (alphabet_size x sequence_length)

**Returns**:

Relative L1 loss between numerical and analytical gradients

<a name=".whatstk.learn.rnn.TestGradient.error"></a>
#### error

```python
 | @staticmethod
 | error(a, b)
```

Computes the error between two vectors, using the relative l1 loss

**Arguments**:

- `a`: Array of size n
- `b`: Array of size n

**Returns**:

Error (float)

<a name=".whatstk.learn.rnn.TestGradient.compute_grad_num"></a>
#### compute\_grad\_num

```python
 | compute_grad_num(param_names, input_sequence, output, init_state, h=1e-4)
```

Computes the gradient of a model parameter numerically

**Arguments**:

- `param_names`: List containing the model parameters' names to check
- `input_sequence`: Input sequence in one-hot format
- `output`: Output sequence in one-hot format
- `h`: Slope

**Returns**:

Numerical gradients

<a name=".whatstk.learn.rnn.TestGradient.compute_grad_num_vector"></a>
#### compute\_grad\_num\_vector

```python
 | compute_grad_num_vector(param, input_sequence, output, init_state, h)
```

Numerically obtains the gradient of a given model parameter (vector shape)

**Arguments**:

- `param`: Model parameter
- `input_sequence`: Input sequence, one-hot matrix format
- `output`: Output sequence in one-hot matrix format
- `h`: Increment to compute, numerically, the slope

**Returns**:

Vector containing the partial derivatives (gradient) of the given model parameter

<a name=".whatstk.learn.rnn.TestGradient.compute_grad_num_matrix"></a>
#### compute\_grad\_num\_matrix

```python
 | compute_grad_num_matrix(param, input_sequence, output, init_state, h)
```

Numerically obtains the gradient of a given model parameter (matrix shape)

**Arguments**:

- `param`: Model parameter (matrix shape)
- `input_sequence`: Input sequence, one-hot matrix format
- `output`: Output sequence in one-hot matrix format
- `h`: Increment to compute, numerically, the slope

**Returns**:

Matrix containing the partial derivatives (gradient) of the given model parameter

<a name=".whatstk.learn.rnn.Encoder"></a>
### Encoder

```python
class Encoder():
 |  Encoder(rnn)
```

This class implements several parsers

<a name=".whatstk.learn.rnn.Encoder.index_to_char"></a>
#### index\_to\_char

```python
 | index_to_char(ind)
```

Converts an indexed to its corresponding character

**Arguments**:

- `ind`: integer index

**Returns**:

character

<a name=".whatstk.learn.rnn.Encoder.char_to_index"></a>
#### char\_to\_index

```python
 | char_to_index(char)
```

Converts a character to its corresponding index

**Arguments**:

- `char`: character

**Returns**:

integer index

<a name=".whatstk.learn.rnn.Encoder.index_to_onehot"></a>
#### index\_to\_onehot

```python
 | index_to_onehot(ind)
```

Converts an index to its corresponding one-hot vector

**Arguments**:

- `ind`: integer index

**Returns**:

onehot vector

<a name=".whatstk.learn.rnn.Encoder.onehot_to_index"></a>
#### onehot\_to\_index

```python
 | @staticmethod
 | onehot_to_index(onehot)
```

Converts a one-hot vector to its corresponding index

**Arguments**:

- `onehot`: onehot vector

**Returns**:

integer index

<a name=".whatstk.learn.rnn.Encoder.char_to_onehot"></a>
#### char\_to\_onehot

```python
 | char_to_onehot(char)
```

Converts a character to its corresponding one-hot evector

**Arguments**:

- `char`: 

**Returns**:



<a name=".whatstk.learn.rnn.Encoder.onehot_to_char"></a>
#### onehot\_to\_char

```python
 | onehot_to_char(onehot)
```

Converts a one-hot vector to its corresponding chracter

**Arguments**:

- `onehot`: 

**Returns**:



<a name=".whatstk.learn.rnn.softmax"></a>
#### softmax

```python
softmax(x)
```

Applies softmax to an input vector

**Arguments**:

- `x`: Input vector

**Returns**:

Vector with the softmax values of x

<a name=".whatstk.learn.rnn.set_mappings"></a>
#### set\_mappings

```python
set_mappings(alphabet)
```

Given an alphabet it obtains the mapping between characters and indices

**Arguments**:

- `alphabet`: List of characters

**Returns**:

Two dictionaries, mapping indices (int) to characters (chars) and viceversa

<a name=".whatstk.learn.rnn.read_data"></a>
#### read\_data

```python
read_data(filename="Globet.txt")
```

Reads the data from a given file

**Arguments**:

- `filename`: Name of the file containing the text to read

**Returns**:

Read text as a list of characters

<a name=".whatstk.plot"></a>
## whatstk.plot

This import makes Python use 'print' as in Python 3.x

<a name=".whatstk.plot.vis"></a>
#### vis

```python
vis(user_data, title)
```

Obtain Figure to plot using plotly.

Does not work if you use date_mode='hourweekday'.

:Example:

>>> from whatstk.core import WhatsAppChat, interventions
>>> filename = 'path/to/samplechat.txt'
>>> hformat = '%d/%m/%y, %H:%M - %name:'
>>> chat = WhatsAppChat.from_txt(filename, hformat=hformat)
>>> counts = interventions(chat=chat, date_mode='date', msg_length=False)
>>> counts_cumsum = counts.cumsum()
>>> from plotly.offline import plot
>>> from whatstk.plot import vis
>>> plot(vis(counts_cumsum, 'cumulative characters sent per day'))

**Arguments**:

- `user_data`: Input data.
:type user_data: pandas.DataFrame
- `title`: Title of figure.
:type title: str

**Returns**:

Figure.
:rtype: dict

<a name=".whatstk.core"></a>
## whatstk.core

<a name=".whatstk.core.WhatsAppChat"></a>
### WhatsAppChat

```python
class WhatsAppChat()
```

Use this class to load and play with your chat log.

<a name=".whatstk.core.WhatsAppChat.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(df)
```

Constructor.

<a name=".whatstk.core.WhatsAppChat.from_txt"></a>
#### from\_txt

```python
 | @classmethod
 | from_txt(cls, filename, auto_header=True, hformat=None, encoding='utf-8')
```

Create instance from chat log txt file hosted locally.

**Arguments**:

- `filename`: Name to the txt chat log file.
:type filename: str
- `auto_header`: Set to True to detect header automatically, otherwise set to False. Defaults to True. If
False, you have to provide a value to `hformat`.
- `hformat`: Format of the header. Check whatstk.WhatsAppChat.prepare_df docs.
:type hformat: str
- `encoding`: Required to load file. Default is 'utf-8'. Should be working. Report any incidence.
:type encoding: str

**Returns**:

WhatsAppChat instance with loaded and parsed chat.
:rtype: whatstk.core.WhatsAppChat

<a name=".whatstk.core.WhatsAppChat.prepare_df"></a>
#### prepare\_df

```python
 | @staticmethod
 | prepare_df(text, hformat)
```

Get a DataFrame-formatted chat.

**Arguments**:

- `text`: Loaded chat as plain text.
:type text: str
- `hformat`: Format of the header. Ude the following keywords:
- %y: for year.
- %m: for month.
- %d: for day.
- %H: for hour.
- %M: for minutes.
- %S: for seconds.
- %P: To denote 12h clock.
- %name: for the username

Example 1: To the header '12/08/2016, 16:20 - username:' corresponds the syntax
'%d/%m/%y, %H:%M - %name:'.

Example 2: To the header '2016-08-12, 4:20 PM - username:' corresponds the syntax
'%y-%m-%d, %H:%M %P - %name:'.
:type hformat: str

**Returns**:

DataFrame containing the chat.
:rtype: pandas.DataFrame

<a name=".whatstk.core.WhatsAppChat.to_csv"></a>
#### to\_csv

```python
 | to_csv(filename)
```

Save data as csv.

**Arguments**:

- `filename`: Name of file.
:type filename: str

<a name=".whatstk.core.WhatsAppChat.__len__"></a>
#### \_\_len\_\_

```python
 | __len__()
```

Get length of DataFrame

**Returns**:

Length.
:rtype: int

<a name=".whatstk.core.WhatsAppChat.shape"></a>
#### shape

```python
 | shape()
```

Get shape of DataFrame-formatted chat.

**Returns**:

Shape.
:rtype: tuple

<a name=".whatstk.core.interventions"></a>
#### interventions

```python
interventions(chat, date_mode='date', msg_length=False)
```

Get number of interventions per user per unit of time.

The unit of time can be chosen by means of argument `date_mode`.

:Example: Get counts of sent messages per user. Also cumulative.

>>> from whatstk.core import WhatsAppChat, interventions
>>> filename = 'path/to/samplechat.txt'
>>> hformat = '%d/%m/%y, %H:%M - %name:'
>>> chat = WhatsAppChat.from_txt(filename, hformat)
>>> counts = interventions(chat, 'date', msg_length=False)
>>> counts_cumsum = counts.cumsum()

**Arguments**:

- `chat`: Object containing parsed WhatsApp chat.
:type chat: whatstk.WhatsAppChat
- `date_mode`: Choose mode to group interventions by. Available modes are:
- 'date': Grouped by particular date (year, month and day).
- 'hour': Grouped by hours.
- 'month': Grouped by months.
- 'weekday': Grouped by weekday (i.e. monday, tuesday, ..., sunday).
- 'hourweekday': Grouped by weekday and hour.
:type date_mode: str
- `msg_length`: Set to True to count the number of characters instead of number of messages sent.
:type msg_length: bool

**Returns**:

DataFrame with shape NxU, where N: number of time-slots and U: number of users.
:rtype: pandas.DataFrame
:raises whatstk.exceptions.InterventionModeError: if invalid mode is chosen.

<a name=".whatstk.utils"></a>
## whatstk.utils

This module includes features which are in development

<a name=".whatstk.utils.auto_header"></a>
## whatstk.utils.auto\_header

<a name=".whatstk.utils.auto_header.extract_header_from_text"></a>
#### extract\_header\_from\_text

```python
extract_header_from_text(text, encoding='utf-8')
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
issep(s)
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
extract_header_format_from_lines(lines)
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
generate_regex(hformat)
```

Generate the appropriate regular expression from simplified syntax.


**Arguments**:

- `hformat`: Simplified syntax for the header.
:type hformat: str

**Returns**:

Regular expression corresponding to the specified syntax.
:rtype: str

<a name=".whatstk.utils.parser.get_message"></a>
#### get\_message

```python
get_message(text, headers, i)
```

Get i:th message from text.

**Arguments**:

- `text`: Whole log chat text.
:type text: str
- `headers`: All headers.
:type headers: list
- `i`: Index denoting the message number.
:type i: int

**Returns**:

i:th message.
:rtype: str

<a name=".whatstk.utils.parser.parse_line"></a>
#### parse\_line

```python
parse_line(text, headers, i)
```

Get date, username and message from the i:th intervention.

**Arguments**:

- `text`: Whole log chat text.
:type text: str
- `headers`: All headers.
:type headers: list
- `i`: Index denoting the message number.
:type i: int

**Returns**:

i:th date, username and message.
:rtype: dict

<a name=".whatstk.utils.parser.parse_chat"></a>
#### parse\_chat

```python
parse_chat(text, regex)
```

**Arguments**:

- `text`: Whole log chat text.
:type text: str
- `regex`: Regular expression
:type regex: str

**Returns**:



<a name=".whatstk.utils.parser.fix_df"></a>
#### fix\_df

```python
fix_df(r_x, df)
```

Get rid of alert/notification messages

**Arguments**:

- `r_x`: Regular expression to detect whatsapp warnings.
:type r_x: str
- `df`: DataFrame with all interventions.
:type df: pandas.DataFrame

**Returns**:

Fixed version of input dataframe.
:rtype: pandas.DataFrame

<a name=".whatstk.utils.exceptions"></a>
## whatstk.utils.exceptions

Library exceptions.

<a name=".whatstk.utils.exceptions.InterventionModeError"></a>
### InterventionModeError

```python
class InterventionModeError(Exception)
```

Raised when a non-implemented mode is selected.

<a name=".whatstk.utils.data_extract"></a>
## whatstk.utils.data\_extract

<a name=".whatstk.utils.data_extract.user_interventions_days"></a>
#### user\_interventions\_days

```python
user_interventions_days(data, length=False)
```

Return DataFrame with interventions of all users (columns) for all days (rows)

Parameters
----------
data: list
DataFrame containing the interventions of all users, including the text.

Returns
----------
df: DataFrame
Table containing `interventions` per user per each day

**Arguments**:

- `data`: 
- `length`: 

**Returns**:



<a name=".whatstk.utils.data_extract.user_interventions_hours"></a>
#### user\_interventions\_hours

```python
user_interventions_hours(data)
```

Return DataFrame with interventions of all users (columns) for all days (rows)

Parameters
----------
data: DataFrame
    DataFrame containing the interventions of all users, including the text.

Returns
----------
df: DataFrame
    Table containing `interventions` per user per each day

<a name=".whatstk.utils.data_extract.week_hour_grid"></a>
#### week\_hour\_grid

```python
week_hour_grid(chat)
```

Return DataFrame with interventions of all users (columns) for all days (rows)

**Arguments**:

- `chat`: DataFrame containing the interventions of all users, including the text.

**Returns**:

DataFrame containing `interventions` per user per each day and hour

<a name=".whatstk.utils.data_extract.response_matrix"></a>
#### response\_matrix

```python
response_matrix(chat, ptype='absolute')
```

Obtains the response matrix between users in the chat group

**Arguments**:

- `chat`: DataFrame containing the interventions of all users, including the text.
- `ptype`: Options for the response matrix (normalized, conditional probabilities etc.)

**Returns**:

Response matrix as DataFrame

<a name=".whatstk.utils.data_extract.histogram_intervention_length"></a>
#### histogram\_intervention\_length

```python
histogram_intervention_length(chat)
```

Obtains the response matrix between users in the chat group

**Arguments**:

- `chat`: DataFrame containing the interventions of all users, including the text.

**Returns**:



<a name=".whatstk.alpha"></a>
## whatstk.alpha

Will be deprecated

