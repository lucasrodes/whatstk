About whatstk
=============

**whatstk**  is a python package providing tools to parse, analyze and visualize WhatsApp chats developed by
`Lucas Rodés-Guirao <https://lcsrg.me>`_. Easily convert your chats to csv or simply visualize statistics
using the python library. The package uses `pandas <https://github.com/pandas-dev/pandas>`_ to
process the data and `plotly <https://github.com/plotly/plotly.py>`_ to visualise it.

You can also `try a live demo <https://whatstk.streamlit.app/>`_.


The project is distributed under the `GPL-3.0 license <https://github.com/lucasrodes/whatstk/blob/master/LICENSE>`_
and is available on `GitHub <http://github.com/lucasrodes/whatstk>`_.

----

First contact with whatstk
--------------------------
**whatstk** is built around :func:`BaseChat <whatstk._chat.BaseChat>` object interface, which requires class method
:func:`from_source <whatstk._chat.BaseChat.from_source>` to be implemented. This method loads and parses the source 
chat file into a pandas.DataFrame.

Below, we use method :func:`df_from_whatsapp <whatstk.whatsapp.parser.df_from_whatsapp>` to load `LOREM chat
<http://raw.githubusercontent.com/lucasrodes/whatstk/develop/chats/whatsapp/lorem.txt>`_. To test it with your own
chat, simply :ref:`export it as a txt file <Export a WhatsApp chat from your phone>` to your computer and then use class argument ``filepath``, as
shown in the following example.


.. code-block:: python

    >>> from whatstk import df_from_whatsapp
    >>> from whatstk.data import whatsapp_urls
    >>> df = df_from_whatsapp(filepath=whatsapp_urls.LOREM)
    >>> df.head(5)
                     date        username                                            message
    0 2020-01-15 02:22:56            Mary                     Nostrud exercitation magna id.
    1 2020-01-15 03:33:01            Mary     Non elit irure irure pariatur exercitation. 🇩🇰
    2 2020-01-15 04:18:42  +1 123 456 789  Exercitation esse lorem reprehenderit ut ex ve...
    3 2020-01-15 06:05:14        Giuseppe  Aliquip dolor reprehenderit voluptate dolore e...
    4 2020-01-15 06:56:00            Mary              Ullamco duis et commodo exercitation.

----

Installation & compatibility
----------------------------
This project is on `PyPI <https://pypi.org/project/whatstk/>`_, install it with pip:

.. code-block:: bash

    pip install whatstk

Project has been tested in Python>=3.7.

From source
^^^^^^^^^^^
Clone the project from the `official repository <https://github.com/lucasrodes/whatstk/>`_ and install it locally 

.. code-block:: bash

    git clone https://github.com/lucasrodes/whatstk.git
    cd whatstk
    pip install .

Extensions
^^^^^^^^^^
To use :ref:`Google Drive <Load WhatsApp chat from Google Drive>` or Chat Generation support, install the library along with the corresponding extensions:

.. code-block:: bash

    pip install whatstk[gdrive]

.. code-block:: bash

    pip install whatstk[generate]

Or install the full suite:

.. code-block:: bash

    pip install whatstk[full]


Develop
^^^^^^^
You can also install the version in development directly from github
`develop <https://github.com/lucasrodes/whatstk/tree/develop>`_ branch. 

.. code-block:: bash

    pip install git+https://github.com/lucasrodes/whatstk.git@develop

Note: It requires `git <https://git-scm.com/>`_ to be installed.

----

Support
-------
You can ask questions and join the development discussion on `GitHub <https://github.com/lucasrodes/whatstk>`_. Use the
`GitHub issues <https://github.com/lucasrodes/whatstk/issues>`_ section to report bugs or request features and `GitHub discussions <https://github.com/lucasrodes/whatstk/issues>`_ to open up broader discussions. You can also check the `project roadmap <https://github.com/lucasrodes/whatstk/projects/3>`_.

For more details, refer to the :ref:`contribute section <Contribute>`.

----

Why this name, whatstk?
-----------------------
whatstk stands for "WhatsApp Toolkit", since the project was initially conceived as a python library to read and process WhatsApp chats. It currently only supports WhatsApp chats, but this might be extended in the future.
