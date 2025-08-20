Why choose whatstk?
===================

There are many python libraries to deal with WhatsApp and other platform chat files. Why should you choose **whatstk**
over these?

Automatic parser
----------------
In WhatsApp, the chat might be exported in :ref:`different formats <The header format>` depending on your phone
configuration, which adds complexity when parsing the chat. **whatstk** incorporates a reliable and powerful
:mod:`parser <whatstk.whatsapp.parser>` to correctly infer the structure of most of the chats. In the rare and
improbable case that the automatic parser does not work for a certain chat, you can still use
`hformat <code_examples/load_chat_hformat.html>`_.

The power of pandas and plotly
------------------------------
**whatstk** uses well established and mantained python libraries `pandas <https://github.com/pandas-dev/pandas>`_ to
process the data and `plotly <https://github.com/plotly/plotly.py>`_ and exploits their potential to efficiently process
and create figures.

Open source and Community oriented
----------------------------------
The project is distributed under the `GPL-3.0 license <https://github.com/lucasrodes/whatstk/blob/master/LICENSE>`_,
available on `GitHub <http://github.com/lucasrodes/whatstk>`_ and open for `user contributions <contribute.html>`_.

The project is mantained since 2016 by `@lucasrodes <https://github.com/lucasrodes>`_.
