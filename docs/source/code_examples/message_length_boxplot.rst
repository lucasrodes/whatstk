Message length
==============

Hello

.. code-block:: python

    >>> from whatstk import WhatsAppChat, FigureBuilder
    >>> from whatstk.graph import plot
    >>> from whatstk.data import whatsapp_urls
    >>> chat = WhatsAppChat.from_source(filepath=whatsapp_urls.LOREM_2000)
    >>> fig = FigureBuilder(chat=chat).user_msg_length_boxplot()
    >>> plot(fig)


.. raw:: html
    :file: ../../_static/html/boxplot.html