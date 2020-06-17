User interaction
================

The user interaction can shed some light on the different kinds of conversations that occur in a chat group. For
instance, when a certain topic appears some users might intervene and others will not, forming *user clusters*. To this
end, a first approach in detecting such clusters resides in which users respond to which users.

User interaction heatmap
------------------------

In the following we visualize the *response matrix*, which tells us the number of messages sent by a certain user to the
rest of users.


For instance, in this specific example we observe that user *Giuseppe* sends 153 messages to + *1 123 456 789* and that
*Mary* receives 122 messages from *John*.

.. code-block:: python

    >>> from whatstk import WhatsAppChat, FigureBuilder
    >>> from whatstk.graph import plot
    >>> from whatstk.data import whatsapp_urls
    >>> chat = WhatsAppChat.from_source(filepath=whatsapp_urls.LOREM_2000)
    >>> fig = FigureBuilder(chat=chat).user_message_responses_heatmap()
    >>> plot(fig)


.. raw:: html
    :file: ../../_static/html/user_message_responses_heatmap.html

.. seealso::

        * :func:`user_message_responses_heatmap <whatstk.FigureBuilder.user_message_responses_heatmap>`

User interaction flow
---------------------

A good way o visualize responses between users are `Sankey diagrams <https://en.wikipedia.org/wiki/Sankey_diagram>`_.
The information conveyed by the graph below is the same as the one in previous section, but the way it is done is
slightly different (sankey diagram instead of a heatmap).

.. code-block:: python

    >>> from whatstk import WhatsAppChat, FigureBuilder
    >>> from whatstk.graph import plot
    >>> from whatstk.data import whatsapp_urls
    >>> chat = WhatsAppChat.from_source(filepath=whatsapp_urls.LOREM_2000)
    >>> fig = FigureBuilder(chat=chat).user_message_responses_flow()
    >>> plot(fig)


.. raw:: html
    :file: ../../_static/html/user_message_responses_flow.html

.. seealso::

        * :func:`user_message_responses_flow <whatstk.FigureBuilder.user_message_responses_flow>`
