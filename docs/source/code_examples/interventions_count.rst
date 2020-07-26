Counting user interventions
===========================

Counting the user interventions can give relevant insights on which users "dominate" the conversation, even more in a
group chat. To this end, object :class:`FigureBuilder <whatstk.FigureBuilder>` has the method
:func:`user_interventions_count_linechart <whatstk.FigureBuilder.user_interventions_count_linechart>`, which generates a
plotly figure with the count of user interventions.

First of all, we load a chat and create an instance of :class:`FigureBuilder <whatstk.FigureBuilder>`.

.. code-block:: python

    >>> from whatstk import WhatsAppChat, FigureBuilder
    >>> from whatstk.graph import plot
    >>> from whatstk.data import whatsapp_urls
    >>> chat = WhatsAppChat.from_source(filepath=whatsapp_urls.LOREM_2000)
    >>> fb = FigureBuilder(chat=chat)

Count of user interventions
---------------------------

Default call of the aforementioned method displays the number of interventions sent by each user per day.

.. code-block:: python

    >>> fig = fb.user_interventions_count_linechart()
    >>> plot(fig)


.. raw:: html
    :file: ../../_static/html/interventions_count_date.html


As seen in previous plot, the number of messages sent per user in a day tends to oscilate quite a lot
from day to day, which might difficult a good visualisation of the data. Hence, we can use ``cumulative=True`` to
illustrate the cumulative count of interventions instead.

.. code-block:: python

    >>> fig = fb.user_interventions_count_linechart(cumulative=True, title='User inteventions count (cumulative)')
    >>> plot(fig)


.. raw:: html
    :file: ../../_static/html/interventions_count_date_cum.html


Additionally, we can obtain the counts for all users combined using ``all_users=True``:

.. code-block:: python

    >>> fig = fb.user_interventions_count_linechart(cumulative=True, all_users=True, title='Inteventions count (cumulative)')
    >>> plot(fig)


.. raw:: html
    :file: ../../_static/html/interventions_count_date_all.html


Count of characters sent per user
---------------------------------

Now, instead of counting the number of interventions we might want to explore the number of characters sent. Note that a
user might send tons of messages with few words, whereas another user might send few messages with tons of words.
Depending on your analysis you might prefer exploring interventions or number of characters. Getting the number of
characters sent per user can be done using ``msg_len=True`` when calling function
:func:`user_interventions_count_linechart <whatstk.FigureBuilder.user_interventions_count_linechart>`.

In the following we explore the cumulative number of characters sent per user.

.. code-block:: python

    >>> fig = fb.user_interventions_count_linechart(msg_len=True, cumulative=True, title='Characters sent by user (cumulative)')
    >>> plot(fig)


.. raw:: html
    :file: ../../_static/html/interventions_count_date_length_cum.html



Other insights
--------------

Method :func:`user_interventions_count_linechart <whatstk.FigureBuilder.user_interventions_count_linechart>` has the
argument ``date_mode``, which allows for several types of count-grouping methods. By default, the method obtains the
counts per date (what has been used in previous examples).


Using ``date_mode=hour`` illustres the distribution of user interventions over the 24 hours in a day. In this example,
for instance, Giuseppe has their interventions peak in hour ranges [01:00, 02:00] and [20:00, 21:00], with 21
interventions in each. 

.. code-block:: python

    >>> fig = fb.user_interventions_count_linechart(date_mode='hour', title='User interventions count (hour)',
    xlabel='Hour')
    >>> plot(fig)

.. raw:: html
    :file: ../../_static/html/interventions_count_hours.html

Using ``date_mode=weekday`` illustres the distribution of user interventions over the 7 days of the week. In this
example, for instance, we see that Monday and Sunday are the days with the most interventions.

.. code-block:: python

    >>> fig = fb.user_interventions_count_linechart(date_mode='weekday', title='User interventions count (weekly)',
    xlabel='Week day')
    >>> plot(fig)

.. raw:: html
    :file: ../../_static/html/interventions_count_weekday.html


Using ``date_mode=month`` illustres the distribution of user interventions over the 12 months of the year. In this
example, for instance, we observe that all users have their interventions peak in June (except for Giuseppe, which has
their peak in July). Maybe summer calling?

.. code-block:: python

    >>> fig = fb.user_interventions_count_linechart(date_mode='month', title='User interventions count (yearly)', xlabel='Month')
    >>> plot(fig)

.. raw:: html
    :file: ../../_static/html/interventions_count_months.html
