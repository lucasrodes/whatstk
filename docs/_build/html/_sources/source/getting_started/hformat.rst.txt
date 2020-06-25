The header format
=================

In WhatsApp, a chat file syntax can differ between devices, OS and language settings, which makes it hard to correctly
parse the data for all formats.

The header appears for each message sent in the chat and contains the timestamp and name of the user that sent the message.

See it for yourself and open :ref:`an exported chat file <Export a WhatsApp chat>`. You will find that the messages have a similar format like the one below:

.. code-block::

    15.04.2016, 15:04 - You created group “Sample Group”
    06.08.2016, 13:18 - Messages you send to this group are now secured with end-to-end encryption. Tap for more info.
    06.08.2016, 13:23 - Ash Ketchum: Hey guys!
    06.08.2016, 13:25 - Brock: Hey Ash, good to have a common group!
    06.08.2016, 13:30 - Misty: Hey guys! Long time haven't heard anything from you
    06.08.2016, 13:45 - Ash Ketchum: Indeed. I think having a whatsapp group nowadays is a good idea
    06.08.2016, 14:30 - Misty: Definetly
    06.08.2016, 17:25 - Brock: I totally agree
    07.08.2016, 11:45 - Prof. Oak: Kids, shall I design a smart poke-ball?

In this example, the header is **day.month.year, hour:minutes - username:** which corresponds to the header format
(a.k.a. **hformat**) ``'%d.%m.%y, %H:%M - %name:'``. However, in your case it may be slightly different depending on you
phone settings. 

Check the table below to see the codes for each header format unit:


.. csv-table:: header format units
   :header: "Date unit code", "Description"
   :widths: 50, 50
   :align: center

   ``'%y'``, Year
    ``'%m'``,	Month of the year (1-12)
    ``'%d'``,	Day of the month (0-31)
    ``'%H'``,	Hour 24h-clock (0-23)
    ``'%P'``,	Hour 12h-clock (1-12)
    ``'%M'``,	Minutes (0-60)
    ``'%S'``,	Seconds (0-60)
    ``'%name'``,	Name of user

.. seealso::
    :ref:`Loading chat using hformat <Load a chat with specific hformat>`
