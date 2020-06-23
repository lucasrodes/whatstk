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

Rename usernames
----------------

In the example here, chat `LOREM1
<http://raw.githubusercontent.com/lucasrodes/whatstk/develop/chats/whatsapp/lorem-merge-part1.txt>`_ and chat `LOREM2
<http://raw.githubusercontent.com/lucasrodes/whatstk/develop/chats/whatsapp/lorem-merge-part2.txt>`_ contain slightly
different usernames. In particular, in chat LOREM2, user *Mary* appears as *Maria* and *Maria2*:

.. code-block:: python

    >>> WhatsAppChat.from_source(filepath=whatsapp_urls.LOREM1).users
    ['+1 123 456 789', 'Giuseppe', 'John', 'Mary']
    >>> WhatsAppChat.from_source(filepath=whatsapp_urls.LOREM2).users
    ['+1 123 456 789', 'Giuseppe', 'John', 'Maria', 'Maria2']

To overcome this, we can rename *Maria* and *Maria2* as Mary in previously merged object ``chat``:

.. code-block:: python

    >>> chat.users
    ['+1 123 456 789', 'Giuseppe', 'John', 'Maria', 'Maria2', 'Mary']
    >>> chat = chat.rename_users({'Mary': ['Maria', 'Maria2']})
    >>> chat.users
    ['+1 123 456 789', 'Giuseppe', 'John', 'Mary']
