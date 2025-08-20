Message length boxplot
======================

Different users send different sort of messages. In particular, the length of the messages (number of characters) can
substatially vary depending on the user sending the message.

In this example, we explore the statistics behind the length of user messages. To this end, we can use method
:func:`user_msg_length_boxplot <whatstk.FigureBuilder.user_msg_length_boxplot>`, which illustrates the length of each
user's messages by means of `box plots <https://en.wikipedia.org/wiki/Box_plot>`_.


.. code-block:: python

    >>> from whatstk import WhatsAppChat, FigureBuilder
    >>> from whatstk.graph import plot
    >>> from whatstk.data import whatsapp_urls
    >>> chat = WhatsAppChat.from_source(filepath=whatsapp_urls.LOREM_2000)
    >>> fig = FigureBuilder(chat=chat).user_msg_length_boxplot()
    >>> plot(fig)


.. raw:: html
    :file: ../../_static/html/boxplot.html
