Custom plot
===========

:class:`FigureBuilder <whatstk.FigureBuilder>` provides some tools to easily visualize your chat. However, the possible
visualizations are infinite. Here, we provide some examples of a custom visualization using some library tools together
with pandas and plotly.


Number of messages vs. Number of characters sent
------------------------------------------------
For each user, we will obtain a 2D scatter plot measuring the number of messages and characters sent in a day. That is,
for a given user we will have `N` points, where `N` is the number of days that the user has sent at least one message.
Each point therefore corresponds to a specific day, where the x-axis and the y-axis measure the number of messages sent
and the average number of characters per message in that day, respectively.


First of all, lets instatiate objects :class:`WhatsAppChat<whatstk.WhatsAppChat>` (chat loading) and
:class:`FigureBuilder <whatstk.FigureBuilder>` (figure coloring).

.. code-block:: python

    >>> from whatstk import WhatsAppChat, FigureBuilder
    >>> from whatstk.data import whatsapp_urls
    >>> chat = WhatsAppChat.from_source(filepath=whatsapp_urls.LOREM_2000)
    >>> fb = FigureBuilder(chat=chat)

Next, we obtain the number of messages and number of characters sent per user per day.

.. code-block:: python

    >>> from whatstk.analysis import get_interventions_count
    >>> counts_interv = get_interventions_count(chat=chat, date_mode='date', msg_length=False, cummulative=False)
    >>> counts_len = get_interventions_count(chat=chat, date_mode='date', msg_length=True, cummulative=False)

Time to process a bit the data. We obtain a DataFrame with five columns: *username*, *date*, *num_characters*,
*num_interventions* and *avg_characters*.

.. code-block:: python

    >>> import pandas as pd
    >>> counts_len = pd.DataFrame(counts_len.unstack(), columns=['num_characters'])
    >>> counts_interv = pd.DataFrame(counts_interv.unstack(), columns=['num_interventions'])
    >>> counts = counts_len.merge(counts_interv, left_index=True, right_index=True)
    >>> # Remove all zero entries and get average number of characters
    >>> counts = counts[~(counts['num_interventions'] == 0)].reset_index()
    >>> counts['avg_characters'] = counts['num_characters']/counts['num_interventions']
    >>> counts.head(5)
             username       date  num_characters  num_interventions  avg_characters
    0  +1 123 456 789 2019-04-16              40                  1       40.000000
    1  +1 123 456 789 2019-04-17              21                  1       21.000000
    2  +1 123 456 789 2019-04-21              90                  2       45.000000
    3  +1 123 456 789 2019-04-25             127                  3       42.333333
    4  +1 123 456 789 2019-04-26              33                  1       33.000000

    [5 rows x 5 columns]

So far we have obtained a dataframe ``counts``, whose rows correspond to a specific message. However, in this example we
are interested in the aggregated values per day. Hence, we group this dataframe by user and date and re-calculate the
number of messages sent and average number of characters sent per day.

.. code-block:: python

    >>> agg_operations = {'avg_characters': 'mean','num_interventions': 'mean'}
    >>> counts = counts.groupby(['username', counts.date.dt.date]).agg(agg_operations)
    >>> counts = counts.rename_axis(index=['username', 'date'])
    >>> counts = counts.reset_index()
    >>> counts.head(5)
              username	      date	avg_characters	num_interventions
    0	+1 123 456 789	2019-04-16	     40.000000	                1
    1	+1 123 456 789	2019-04-17	     21.000000	                1
    2	+1 123 456 789	2019-04-21	     45.000000	                2
    3	+1 123 456 789	2019-04-25	     42.333333	                3
    4	+1 123 456 789	2019-04-26	     33.000000	                1

Once the dataframe is obtained, we generate a plot using `Histogram2dContour
<https://plotly.com/python/2d-histogram-contour/>`_ by plotly.

.. code-block:: python

    >>> from whatstk.graph import plot
    >>> import plotly.graph_objs as go
    >>> traces = []
    >>> for username in fb.usernames:
    >>>     counts_user = counts[counts['username']==username]
    >>>     traces.append(
    >>>         go.Histogram2dContour(
    >>>             contours={'coloring': 'none'},
    >>>             x=counts_user['num_interventions'],
    >>>             y=counts_user['avg_characters'],
    >>>             # mode='markers',
    >>>             # marker=dict(color=fb.user_color_mapping[username], opacity=0.2),
    >>>             name=username,
    >>>             showlegend=True,
    >>>             line={'color': fb.user_color_mapping[username]},
    >>>             nbinsx=10, nbinsy=20
    >>>         )
    >>>     )


.. code-block:: python

    >>> layout = {
    >>>     'title': 'Average number of characters sent in a day vs Interventions per day',
    >>>     'yaxis_title': 'avg characters',
    >>>     'xaxis_title': 'num interventions',
    >>> }
    >>> fig = go.Figure(data=traces, layout=layout)
    >>> plot(fig)

.. raw:: html
    :file: ../../_static/html/custom_interventions_vs_length.html

