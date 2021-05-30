``whatstk-generate-chat``
=========================

.. warning::

    To use the chat generation functionalities, install the library with the corresponding extension (ignore the
    ``--upgrade`` option if you haven't installed the library):

    .. code-block::

        pip install whatstk[generate] --upgrade

Generate random WhatsApp chat.

.. code-block:: bash

    whatstk-generate-chat --help
    usage: Generate chat. Make sure to install the library with required extension: pip install whatstk[generate]
    --upgrade
           [-h] -o OUTPUT_PATH
                          [--filenames FILENAMES [FILENAMES ...]] [-s SIZE]
                          [-f HFORMATS [HFORMATS ...]]
                          [--last-timestamp LAST_TIMESTAMP] [-v]

    optional arguments:
    -h, --help            show this help message and exit
    -o OUTPUT_PATH, --output-path OUTPUT_PATH
                            Path where to store generated chats. Must exist.
    --filenames FILENAMES [FILENAMES ...]
                            Filenames. Must be equal length of --hformats.
    -s SIZE, --size SIZE  Number of messages to create per chat. Defaults to
                            500.
    -f HFORMATS [HFORMATS ...], --hformats HFORMATS [HFORMATS ...]
                            Header format. If None, defaults to all supported
                            hformats. List formats as 'format 1' 'format 2' ...
    --last-timestamp LAST_TIMESTAMP
                            Timestamp of last message. Format YYYY-mm-dd
    -v, --verbose         Verbosity.
