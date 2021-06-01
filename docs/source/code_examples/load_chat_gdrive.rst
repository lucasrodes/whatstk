Load WhatsApp chat from Google Drive
====================================

.. warning::

    To load chats from google drive, install the library with the corresponding extension (ignore the
    ``--upgrade`` option if you haven't installed the library):

    .. code-block::

        pip install whatstk[gdrive] --upgrade

You can also load a file saved in your Google Drive. Note that in order to do so, you need first to configure the
credentials to interact with Google Drive.

Configure credentials
---------------------

In particular, you need the client secret JSON file. This can be downloaded from th Google Console. To get this file, we recommend following `this tutorial
<https://medium.com/analytics-vidhya/how-to-connect-google-drive-to-python-using-pydrive-9681b2a14f20>`_, which is
inspired by `PyDrive2 documentation <https://iterative.github.io/PyDrive2/docs/build/html/quickstart.html>`_. Some
important  additions to previous tutorials are:

- Make sure to add yourself in Test users, as noted in `this thread <https://stackoverflow.com/questions/65980758/pydrive-quickstart-and-error-403-access-denied>`_
- Select Desktop App instead of Web Application as the application type when creating the OAuth Client ID.

Once you have downloaded the clients secrets, run :func:`gdrive_init <whatstk.utils.gdrive.gdrive_init>`, which will
guide you through the Authentification process. You will need to access a link via your browser and copy paste a
verification code.

.. code-block:: python

    >>> from whatstk.utils import gdrive_init
    >>> gdrive_init("path/to/client_secrets.json")
    Go to the following link in your browser:

    https://accounts.google.com/...

    Enter verification code: 

This should only be run the first time to correctly configure your Google credentials.


Load a file from Google Drive
-----------------------------

You can pass a file reference to :class:`WhatsAppChat <whatstk.WhatsAppChat>` by means of its ID. All files in Google
Drive have a unique ID. To obtain it, create a `shareable link
<https://support.google.com/drive/answer/7166529?co=GENIE.Platform%3DDesktop&hl=en>`_, which will have the following format:

.. code-block::

    https://drive.google.com/file/d/[FILE-ID]/view?usp=sharing


Now, simply copy ``[FILE-ID]`` and run:

.. code-block:: python

    >>> from whatstk import WhatsAppChat
    >>> chat = WhatsAppChat.from_source("gdrive://[FILE-ID]")

Note that Google Drive file IDs are passed with prefix `gdrive://`.
