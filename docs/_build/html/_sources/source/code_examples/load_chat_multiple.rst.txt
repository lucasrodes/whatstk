Load chat from multiple sources
===============================

You can also load a chat using multiple source files. You might want to use this when several files have been exported
from the same chat over time. 

In the example below, we load chats
`LOREM1 <http://raw.githubusercontent.com/lucasrodes/whatstk/develop/chats/whatsapp/lorem-merge-part1.txt>`_ and `LOREM2 <http://raw.githubusercontent.com/lucasrodes/whatstk/develop/chats/whatsapp/lorem-merge-part2.txt>`_.

.. code-block:: python

    >>> from whatstk import WhatsAppChat
    >>> from whatstk.data import whatsapp_urls
    >>> chat = WhatsAppChat.from_sources(filepaths=[whatsapp_urls.LOREM1, whatsapp_urls.LOREM2])
