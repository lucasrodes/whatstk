Load chat
==============

Once you have :doc:`exported <../getting_started/export_chat>` a chat it is time to load it in python.

In this example we load the example `LOREM chat <http://raw.githubusercontent.com/lucasrodes/whatstk/
develop/chats/whatsapp/lorem.txt>`_, which is available online, using library class :class:`WhatsAppChat 
<whatstk.WhatsAppChat>`.

.. code-block:: python

    >>> from whatstk import WhatsAppChat
    >>> from whatstk.data import whatsapp_urls
    >>> chat = WhatsAppChat.from_source(filepath=whatsapp_urls.LOREM)

Once loaded, we can check some of the chat messages by accessing its attribute :func:`df <whatstk.WhatsAppChat.df>`,
which is a pandas.DataFrame with columns `username` (name of user sending the message), `message` (message sent) and
`date` index (timestamp of message).

.. code-block:: python

    >>> chat.df.head(5)
                                   username                                            message
        date
        2020-01-15 02:22:56            Mary                     Nostrud exercitation magna id.
        2020-01-15 03:33:01            Mary     Non elit irure irure pariatur exercitation. 🇩🇰
        2020-01-15 04:18:42  +1 123 456 789  Exercitation esse lorem reprehenderit ut ex ve...
        2020-01-15 06:05:14        Giuseppe  Aliquip dolor reprehenderit voluptate dolore e...
        2020-01-15 06:56:00            Mary              Ullamco duis et commodo exercitation.

Getting the start and end date of the chat can give us a good overview of the chat content.

.. code-block:: python

    >>> print(f"Start date: {chat.start_date}\nEnd date: {chat.end_date}")
    Start date: 2020-01-15 02:22:56
    End date: 2020-05-11 22:32:48

Also, getting a list with the chat members is simple

.. code-block:: python

    >>> chat.users
    ['+1 123 456 789', 'Giuseppe', 'John', 'Mary']