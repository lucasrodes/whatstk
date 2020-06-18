Load a chat with specific ``hformat``
=====================================

If auto_header``option fails, you can still oad your chat manually specifying the ``hformat``. In the example below, the
header has the ``hformat='%d.%m.%y, %H:%M - %name:'``.

.. code-block:: python

    from whatstk.whatsapp.objects import WhatsAppChat
    from whatstk.data import whatsapp_urls
    chat = WhatsAppChat.from_source(filepath=whatsapp_urls.POKEMON, hformat='%d.%m.%y, %H:%M - %name:')
    chat.df.head(5)
                            username                                            message
    date
    2016-08-06 13:23:00  Ash Ketchum                                          Hey guys!
    2016-08-06 13:25:00        Brock              Hey Ash, good to have a common group!
    2016-08-06 13:30:00        Misty  Hey guys! Long time haven't heard anything fro...
    2016-08-06 13:45:00  Ash Ketchum  Indeed. I think having a whatsapp group nowada...
    2016-08-06 14:30:00        Misty                                          Definetly
