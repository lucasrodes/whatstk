Automatic header detection
==========================

WhatsApp exports use different :ref:`header formats <The header format>` depending on the device, OS
and language settings of the phone that produced them. Rather than asking you to work out which one you
have, **whatstk** tries to infer it from the file itself.

This is on by default, so in most cases you do not need to think about it at all:

.. code-block:: python

    >>> from whatstk import df_from_whatsapp
    >>> from whatstk.data import whatsapp_urls
    >>> df = df_from_whatsapp(filepath=whatsapp_urls.POKEMON)

Under the hood this calls :func:`extract_header_from_text
<whatstk.whatsapp.auto_header.extract_header_from_text>`, which returns the inferred ``hformat``:

.. code-block:: python

    >>> from urllib.request import urlopen
    >>> from whatstk.whatsapp.auto_header import extract_header_from_text
    >>> from whatstk.data import whatsapp_urls
    >>> with urlopen(whatsapp_urls.POKEMON) as f:
    ...     text = f.read().decode('utf-8')
    >>> extract_header_from_text(text)
    '%d.%m.%y, %H:%M - %name:'


How it works
------------

For every line of the chat, the text before the first ``": "`` is treated as a candidate header. Each
candidate is broken into its numeric components and a template — for example
``06.08.2016, 13:23 - Ash Ketchum:`` becomes the components ``[6, 8, 2016, 13, 23]`` and the template
``{}.{}.{}, {}:{} - %name:``.

Candidates whose shape does not match the most common one are discarded, which makes detection robust
to message bodies that happen to contain a colon. The numeric positions are then mapped to date units
using a small set of heuristics:

* **Day** — the position whose maximum value falls between 28 and 31.
* **Year** — of the two remaining date positions, the one with the largest maximum value.
* **Month** — the remaining date position.
* **Hour, minutes and (if present) seconds** — the positions that follow the date.
* **12h vs 24h** — ``%I`` if an AM/PM marker is present in the template, ``%H`` otherwise.


When it fails
-------------

If no format can be inferred, :func:`extract_header_from_text
<whatstk.whatsapp.auto_header.extract_header_from_text>` returns ``None`` and the loader raises a
``RuntimeError`` asking you to supply the format yourself. You can always bypass detection entirely by
passing ``hformat``:

.. code-block:: python

    >>> df = df_from_whatsapp(filepath='path/to/chat.txt', hformat='%d.%m.%y, %H:%M - %name:')

See :ref:`Load WhatsApp chat with specific hformat <Load WhatsApp chat with specific hformat>` for a
worked example.

.. warning::

    Detection is known to be imperfect in a few situations. The most important one is **short chats**:
    the day position is identified by looking for a value between 28 and 31, so a chat that never
    reaches day 28 gives the heuristic nothing to latch onto and it falls back to the first position.
    A chat in ``%y-%m-%d`` format spanning only the first days of a month is inferred as ``%d-%y-%m``,
    and a ``%m/%d/%y`` chat is inferred as ``%d/%m/%y`` — day and month silently swapped.

    Other known limitations:

    * **Month names.** Only all-numeric dates are supported; formats such as ``12 Aug 2016`` return
      ``None``.
    * **Unusual separators.** The username is located by matching ``... - name:`` or ``[...] name:``.

    If a chat is small or you need certainty, pass ``hformat`` explicitly. Improving these heuristics is
    tracked in `issue #175 <https://github.com/lucasrodes/whatstk/issues/175>`_; if detection fails on a
    real export, please `report it <https://github.com/lucasrodes/whatstk/issues>`_ — include the first
    few lines of the file with the message text redacted.


Checking whether a format is supported
--------------------------------------

The formats whatstk knows about, and whether each one supports automatic detection, are listed in
:mod:`whatstk.whatsapp.hformat <whatstk.whatsapp.hformat>`:

.. code-block:: python

    >>> from whatstk.whatsapp.hformat import is_supported_verbose
    >>> is_supported_verbose('%y-%m-%d, %H:%M - %name:')
    "The header '%y-%m-%d, %H:%M - %name:' is supported. `auto_header` for this header is supported."

.. seealso::

    * :ref:`The header format <The header format>`
    * :ref:`Load WhatsApp chat with specific hformat <Load WhatsApp chat with specific hformat>`
    * :func:`extract_header_from_text <whatstk.whatsapp.auto_header.extract_header_from_text>`
