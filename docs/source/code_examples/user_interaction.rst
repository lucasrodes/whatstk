User interaction
================

Hello

User interaction heatmap
------------------------

.. code-block:: python

    >>> from whatstk import WhatsAppChat, FigureBuilder
    >>> from whatstk.graph import plot
    >>> from whatstk.data import whatsapp_urls
    >>> chat = WhatsAppChat.from_source(filepath=whatsapp_urls.LOREM_2000)
    >>> fig = FigureBuilder(chat=chat).user_message_responses_heatmap()
    >>> plot(fig)


.. raw:: html
    :file: ../../_static/html/user_message_responses_heatmap.html

User interaction flow
---------------------

.. code-block:: python

    >>> from whatstk import WhatsAppChat, FigureBuilder
    >>> from whatstk.graph import plot
    >>> from whatstk.data import whatsapp_urls
    >>> chat = WhatsAppChat.from_source(filepath=whatsapp_urls.LOREM_2000)
    >>> fig = FigureBuilder(chat=chat).user_message_responses_flow()
    >>> plot(fig)


.. raw:: html
    :file: ../../_static/html/user_message_responses_flow.html