Library available chats
=======================

For the purpose of showcasing code examples and benchmarking different implementations, we have created a pool of chats,
hosted in the `official repository page <https://github.com/lucasrodes/whatstk/tree/master/chats>`_. If you want to test
the library with one of your own tests, check the :ref:`code examples <Code examples>`.

The chats are available via their corresponding URLs, which are listed in source code :mod:`whatstk.data`.

.. contents:: Contents
    :depth: 3

WhatsApp
--------

Object ``whatsapp_urls`` contains all URLs for WhatsApp chats.

.. code-block:: python

    >>> from whatstk.data import whatsapp_urls

POKEMON
^^^^^^^

Brief chat with Pokemon characters, which was manually designed by  `@lucasrodes <https://github.com/lucasrodes>`_ in
`commit 666d6ea9cc030c4322fbe44ae64b8f1a0fdb5169
<https://github.com/lucasrodes/whatstk/commit/666d6ea9cc030c4322fbe44ae64b8f1a0fdb5169>`_.

.. code-block:: python

    >>> from whatstk.data import whatsapp_urls
    >>> from whatstk import WhatsAppChat
    >>> chat = WhatsAppChat.from_source(filepath=whatsapp_urls.POKEMON)
    >>> chat.head(5)
                            username                                            message
    date                                                                               
    2016-08-06 13:23:00  Ash Ketchum                                          Hey guys!
    2016-08-06 13:25:00        Brock              Hey Ash, good to have a common group!
    2016-08-06 13:30:00        Misty  Hey guys! Long time haven't heard anything fro...
    2016-08-06 13:45:00  Ash Ketchum  Indeed. I think having a whatsapp group nowada...
    2016-08-06 14:30:00        Misty                                          Definetly


.. note:: 
    `Chat file <http://raw.githubusercontent.com/lucasrodes/whatstk/develop/chats/whatsapp/pokemon.txt>`_


LOREM
^^^^^
Chat with 500 interventions of fictional users, generated using `python-lorem <https://lorem.jarryshaw.me/en/latest/>`_.


.. code-block:: python

    >>> from whatstk.data import whatsapp_urls
    >>> from whatstk import WhatsAppChat
    >>> chat = WhatsAppChat.from_source(filepath=whatsapp_urls.LOREM)
    >>> chat.df.head(5)
                               username                                            message
    date                                                                                  
    2020-01-15 02:22:56            Mary                     Nostrud exercitation magna id.
    2020-01-15 03:33:01            Mary     Non elit irure irure pariatur exercitation. 🇩🇰
    2020-01-15 04:18:42  +1 123 456 789  Exercitation esse lorem reprehenderit ut ex ve...
    2020-01-15 06:05:14        Giuseppe  Aliquip dolor reprehenderit voluptate dolore e...
    2020-01-15 06:56:00            Mary              Ullamco duis et commodo exercitation.

.. note::
    `Chat file <http://raw.githubusercontent.com/lucasrodes/whatstk/develop/chats/whatsapp/lorem.txt>`_

LOREM1
^^^^^^
Chat with 300 interventions of fictional users, generated using `python-lorem <https://lorem.jarryshaw.me/en/latest/>`_.

.. code-block:: python

    >>> from whatstk.data import whatsapp_urls
    >>> from whatstk import WhatsAppChat
    >>> chat = WhatsAppChat.from_source(filepath=whatsapp_urls.LOREM1)
    >>> chat.df.head(5)
                               username                                            message
    date                                                                                  
    2019-10-20 10:16:00            John        Laborum sed excepteur id eu cillum sunt ut.
    2019-10-20 11:15:00            Mary  Ad aliquip reprehenderit proident est irure mo...
    2019-10-20 12:16:00  +1 123 456 789  Nostrud adipiscing ex enim reprehenderit minim...
    2019-10-20 12:57:00  +1 123 456 789  Deserunt proident laborum exercitation ex temp...
    2019-10-20 17:28:00            John                Do ex dolor consequat tempor et ex.

.. note::
    `Chat file <http://raw.githubusercontent.com/lucasrodes/whatstk/develop/chats/whatsapp/lorem-merge-part1.txt>`_

LOREM2
^^^^^^
Chat with 300 interventions of fictional users, generated using `python-lorem <https://lorem.jarryshaw.me/en/latest/>`_.

Can be used along with **LOREM1** to test chat merging functionalities.

.. code-block:: python

    >>> from whatstk.data import whatsapp_urls
    >>> from whatstk import WhatsAppChat
    >>> chat = WhatsAppChat.from_source(filepath=whatsapp_urls.LOREM2)
    >>> chat.df.head(5)
                               username                                            message
    date                                                                                  
    2020-06-20 10:16:00            John                 Elit incididunt lorem sed nostrud.
    2020-06-20 11:15:00           Maria        Esse do irure dolor tempor ipsum fugiat. 🇩🇰
    2020-06-20 12:16:00  +1 123 456 789  Cillum anim non eu deserunt consectetur dolor ...
    2020-06-20 12:57:00  +1 123 456 789                  Non ipsum proident veniam est. 🏊🏻
    2020-06-20 17:28:00            John                      Dolore in cupidatat proident.

.. note::
    `Chat file <http://raw.githubusercontent.com/lucasrodes/whatstk/develop/chats/whatsapp/lorem-merge-part1.txt>`_

LOREM_2000
^^^^^^^^^^
Chat with 2000 interventions of fictional users, generated using `python-lorem <https://lorem.jarryshaw.me/en/latest/>`_.

.. code-block:: python

    >>> from whatstk.data import whatsapp_urls
    >>> from whatstk import WhatsAppChat
    >>> chat = WhatsAppChat.from_source(filepath=whatsapp_urls.LOREM_2000)
    >>> chat.df.head(5)
                               username                                            message
    date                                                                                  
    2019-04-16 02:09:00  +1 123 456 789           Et labore proident laboris do labore ex.
    2019-04-16 03:01:00            Mary  Reprehenderit id aute consectetur aliquip nost...
    2019-04-17 12:56:00            John  Amet magna officia ullamco pariatur ipsum cupi...
    2019-04-17 13:30:00            Mary  Cillum aute et cupidatat ipsum, occaecat lorem...
    2019-04-17 15:09:00            John  Eiusmod irure laboris dolore anim, velit velit...

.. note::
    `Chat file <http://raw.githubusercontent.com/lucasrodes/whatstk/develop/chats/whatsapp/lorem-2000.txt>`_
