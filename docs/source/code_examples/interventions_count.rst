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
from day to day, which might difficult a good visualisation of the data. Hence, we can use ``cummulative=True`` to
illustrate the cummulative count of interventions instead.

.. code-block:: python

    >>> fig = fb.user_interventions_count_linechart(cummulative=True, title='User inteventions count (cummulative)')
    >>> plot(fig)


.. raw:: html
    :file: ../../_static/html/interventions_count_date_cum.html


Count of characters sent per user
---------------------------------

Now, instead of counting the number of interventions we might want to explore the number of characters sent. Note that a
user might send tons of messages with few words whereas another user might send few messages with tons of words.
Depending on your analysis you might prefer exploring interventions or number of characters.


.. code-block:: python

    >>> fig = fb.user_interventions_count_linechart(msg_len=True, title='Characters sent by user')
    >>> plot(fig)


.. raw:: html
    :file: ../../_static/html/interventions_count_date_length.html

Similar to the previous :ref:`section <Count of user interventions>`, we can also visualize the number of characer sent
in a cummulative manner, which tends to be more readable.

.. code-block:: python

    >>> fig = fb.user_interventions_count_linechart(msg_len=True, cummulative=True)
    >>> plot(fig)


.. raw:: html
    :file: ../../_static/html/interventions_count_date_length_cum.html
