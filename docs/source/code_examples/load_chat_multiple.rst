Load chat from multiple sources
===============================

You can also load a chat

.. code-block:: python

    >>> from whatstk import WhatsAppChat
    >>> from whatstk.data import whatsapp_urls
    >>> chat = WhatsAppChat.from_sources(filepaths=[whatsapp_urls.LOREM1, whatsapp_urls.LOREM2])