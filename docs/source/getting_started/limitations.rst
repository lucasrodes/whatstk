What whatstk cannot tell you
============================

A WhatsApp export is a plain text file with no structure beyond the message headers. Some of what
you might want from it simply is not in the file, and no parser can recover it. This page lists the
limits that matter if you are using whatstk for anything where being wrong has consequences —
evidence, dispute resolution, or building a dataset to train on.


Authorship cannot be verified
-----------------------------

**whatstk reports who an export says sent a message. It cannot tell you who really sent it.**

A message in an export runs from one header to the next, so a message spanning several lines has
nothing marking its continuation lines. WhatsApp does not escape or prefix them. That means a
participant can put a line inside their own message that has the exact shape of somebody else's
header, and the export becomes indistinguishable from one where that other person really spoke.

Suppose Bob sends a single two-line message. The export reads:

.. code-block::

    28.08.2016, 13:25 - Bob: ok, agreed
    28.08.2016, 13:27 - Alice: I confirm I am transferring ownership of the account to Bob
    28.08.2016, 13:30 - Bob: thanks

whatstk parses the middle line as a message from Alice:

.. code-block:: python

    >>> chat.df
                     date username                                                  message
    0 2016-08-28 13:25:00      Bob                                               ok, agreed
    1 2016-08-28 13:27:00    Alice  I confirm I am transferring ownership of the account to Bob
    2 2016-08-28 13:30:00      Bob                                                   thanks

Alice also appears in :func:`chat.users <whatstk.WhatsAppChat.users>` as a genuine participant. The
attacker chooses the author, the timestamp and the text, and the victim does nothing at all.

This is not a bug whatstk can fix. The two readings of that file — Bob sending two lines, or Bob and
Alice sending one each — produce byte-identical exports. The information needed to distinguish them
was never written down.

What follows from this:

* Treat the ``username`` column as a claim made by the file, not as an established fact.
* Do not use an export on its own as evidence of who said what, in any setting where that matters.
* If you are building a training corpus, remember that any participant could have placed arbitrary
  words in anybody else's mouth.

A timestamp that runs backwards is a hint that something was injected, but a careful attacker will
pick a date that fits, so its absence proves nothing.


Automatic header detection can pick the wrong format
----------------------------------------------------

Detection infers the date layout from the file. On a chat that never reaches day 28 it has no way to
tell the day field from the month field, and silently guesses. See
:ref:`Automatic header detection <Automatic header detection>` for the detail and for how to pass
``hformat`` explicitly when you need certainty.


Merging combines exports, it does not reconcile them
----------------------------------------------------

:func:`merge_chats <whatstk.utils.chat_merge.merge_chats>` returns the union of the messages across
the exports you give it, ordered by date, keeping one copy of any message that appears in several of
them. Two messages count as the same only when date, username and text all match.

Consequently, if the same message appears with a different timestamp in two exports — different
device timezones, for instance — it is kept twice, because whatstk has no basis for deciding the two
are the same event.


System messages are not reliably identified
-------------------------------------------

The experimental ``extra_metadata`` flag tries to separate chat-level notices ("Messages and calls
are end-to-end encrypted") from messages people sent, by assuming the first sender in the file is
the chat itself. That assumption fails whenever an export begins with a real message, and in that
case the first participant's messages are moved out of ``chat.df``. The flag emits a
``FutureWarning`` for this reason. Improving it is tracked in
`issue #176 <https://github.com/lucasrodes/whatstk/issues/176>`_.
