About whatstk
=============

**whatstk**  is a python package providing tools to parse, analyze and visualize WhatsApp chats developed under the
`sociepy <https://github.com/sociepy>`_ project. Easily convert your chats to csv or simply visualize statistics
using the python library. The package uses `pandas <https://github.com/pandas-dev/pandas>`_ to
process the data and `plotly <https://github.com/plotly/plotly.py>`_ to visualise it.

The project is distributed under the `GPL-3.0 license <https://github.com/lucasrodes/whatstk/blob/master/LICENSE>`_
and is available on `GitHub <http://github.com/lucasrodes/whatstk>`_.

----

First contact with whatstk
--------------------------
**whatstk** is built around :func:`BaseChat <whatstk._chat.BaseChat>` object interface, which requires class method
:func:`from_source <whatstk._chat.BaseChat.from_source>` to be implemented. This method loads and parses the source 
chat file into a pandas.DataFrame.

Below, we use the WhatsApp implementation, i.e. :class:`WhatsAppChat <whatstk.WhatsAppChat>`, to load `LOREM chat
<http://raw.githubusercontent.com/lucasrodes/whatstk/develop/chats/whatsapp/lorem.txt>`_. To test it with your own 
chat, simply :ref:`export it as a txt file<Export chat>` to your computer and then use class argument ``filepath``, as
shown in the following example.


.. code-block:: python

    >>> from whatstk.whatsapp.objects import WhatsAppChat
    >>> from whatstk.data import whatsapp_urls
    >>> chat = WhatsAppChat.from_source(filepath=whatsapp_urls.LOREM)
    >>> chat.df.head(5)
                               username                                            message
    date                                                                                  
    2020-01-15 02:22:56            Mary                     Nostrud exercitation magna id.
    2020-01-15 03:33:01            Mary     Non elit irure irure pariatur exercitation. 🇩🇰
    2020-01-15 04:18:42  +1 123 456 789  Exercitation esse lorem reprehenderit ut ex ve...
    2020-01-15 06:05:14        Giuseppe  Aliquip dolor reprehenderit voluptate dolore e...
    2020-01-15 06:56:00            Mary              Ullamco duis et commodo exercitation.

----

Installation & compatibility
----------------------------
This project is on `PyPI <https://pypi.org/project/whatstk/>`_, install it with pip:

.. code-block:: bash

    pip install whatstk

Project has been tested with Python 3.7-3.8.

From source
^^^^^^^^^^^
Clone the project from the `official repository <https://github.com/lucasrodes/whatstk/>`_

.. code-block:: bash

    git clone https://github.com/lucasrodes/whatstk.git


and install it locally 

.. code-block:: bash

    cd whatstk
    pip install .


Develop
^^^^^^^
You can also install the version in development directly from github
`develop <https://github.com/lucasrodes/whatstk/tree/develop>`_ branch.

.. code-block:: bash

    pip install  
    pip install git+https://github.com/lucasrodes/whatstk.git@develop

----

Support
-------
You can ask questions and join the development discussion on `Gitter <https://gitter.im/sociepy/whatstk>`_. Use the
`GitHub issues <https://github.com/lucasrodes/whatstk/issues>`_ section to report bugs or request features. You
can also check the `project roadmap <https://github.com/lucasrodes/whatstk/projects/3>`_.

For more details, refer to the :ref:`contribute section <Contribute>`.

----

Why this name, whatstk?
-----------------------
whatstk stands for "WhatsApp Toolkit", since the project was initially conceived as a python library to read and process
WhatsApp chats.