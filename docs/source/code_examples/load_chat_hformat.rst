Load WhatsApp chat with specific hformat
========================================

If ``auto_header`` option fails, you can still load your chat manually specifying the ``hformat``. In the example below,
we have that the ``hformat='%d.%m.%y, %H:%M - %name:'``.

.. code-block:: python

    >>> from whatstk.whatsapp.objects import WhatsAppChat
    >>> from whatstk.data import whatsapp_urls
    >>> chat = WhatsAppChat.from_source(filepath=whatsapp_urls.POKEMON, hformat='%d.%m.%y, %H:%M - %name:')
    >>> chat.df.head(5)
                     date     username                                            message
    0 2016-08-06 13:23:00  Ash Ketchum                                          Hey guys!
    1 2016-08-06 13:25:00        Brock              Hey Ash, good to have a common group!
    2 2016-08-06 13:30:00        Misty  Hey guys! Long time haven't heard anything fro...
    3 2016-08-06 13:45:00  Ash Ketchum  Indeed. I think having a whatsapp group nowada...
    4 2016-08-06 14:30:00        Misty                                          Definetly

----

.. seealso::

    * :ref:`The header format <The header format>`
    * :ref:`Load WhatsApp chat <Load WhatsApp chat>`
    * :ref:`Load WhatsApp chat from Google Drive <Load WhatsApp chat from Google Drive>`
    * :ref:`Load WhatsApp chat with specific hformat <Load WhatsApp chat with specific hformat>`
