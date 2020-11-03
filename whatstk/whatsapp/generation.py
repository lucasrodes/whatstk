"""Automatic generation of chat using Lorem Ipsum text and time series statistics."""


import os
from datetime import datetime, timedelta
import itertools
import numpy as np
import pandas as pd
from scipy.stats import lomax
from lorem import sentence
from emoji.unicode_codes import EMOJI_UNICODE
from whatstk.whatsapp.objects import WhatsAppChat
from whatstk.whatsapp.hformat import get_supported_hformats_as_list
from whatstk.utils.utils import COLNAMES_DF


USERS = [
    'John', 'Mary', 'Giuseppe', '+1 123 456 789'
]


class ChatGenerator:
    """Generate a chat.

    Args:
        size (int): Number of messages to generate.
        users (list, optional): List with names of the users. Defaults to module variable USERS.
        seed (int, optional): Seed for random processes. Defaults to 100.

    Examples:
        This simple example loads a chat using :func:`WhatsAppChat <whatstk.whatsapp.objects.WhatsAppChat>`. Once
        loaded, we can access its attribute ``df``, which contains the loaded chat as a DataFrame.

        ..  code-block:: python

            >>> from whatstk.whatsapp.generation import ChatGenerator
            >>> from datetime import datetime
            >>> from whatstk.data import whatsapp_urls
            >>> chat = ChatGenerator(size=10).generate(last_timestamp=datetime(2020, 1, 1, 0, 0))
            >>> chat.df.head(5)
                                    date  username                                            message
            0 2019-12-31 09:43:04.000525  Giuseppe                               Nisi ad esse cillum.
            1 2019-12-31 10:19:21.980039  Giuseppe      Tempor dolore sint in eu lorem veniam veniam.
            2 2019-12-31 13:56:45.575426  Giuseppe  Do quis fugiat sint ut ut, do anim eu est qui ...
            3 2019-12-31 15:47:29.995420  Giuseppe  Do qui qui elit ea in sed culpa, aliqua magna ...
            4 2019-12-31 16:23:00.348542      Mary  Sunt excepteur mollit voluptate dolor sint occ...

    """

    def __init__(self, size, users=None, seed=100):
        """Instantiate ChatGenerator class.

        Args:
            size (int): Number of messages to generate.
            users (list, optional): List with names of the users. Defaults to module variable USERS.
            seed (int, optional): Seed for random processes. Defaults to 100.

        """
        self.size = size
        self.users = USERS if not users else users
        self.seed = seed
        np.random.seed(seed=self.seed)

    def _generate_messages(self):
        """Generate list of messages.

        To generate sentences, Lorem Ipsum is used.

        Returns:
            list: List with messages (as strings).

        """
        emojis = self._generate_emojis()
        s = sentence(count=self.size, comma=(0, 2), word_range=(4, 8))
        sentences = list(itertools.islice(s, self.size))
        messages = [sentences[i] + ' ' + emojis[i] for i in range(self.size)]
        return messages

    def _generate_emojis(self, k=1):
        """Generate random list of emojis.

        Emojis are sampled from a list of `n` emojis and `k*n` empty strings.

        Args:
            k (int, optional): Defaults to 20.

        Returns:
            list: List with emojis

        """
        emojis = list(EMOJI_UNICODE.values())
        n = len(emojis)
        emojis = emojis + [''] * k*n
        return np.random.choice(emojis, self.size)

    def _generate_timestamps(self, last=None):
        """Generate list of timestamps.

        Args:
            last (datetime, optional): Datetime of last message. If ``None``, defaults to current date.

        Returns:
            list: List with timestamps.

        """
        if not last:
            last = datetime.now()
            last = last.replace(microsecond=0)
        c = 1.0065
        scale = 40.06
        loc = 30
        ts_ = [0] + lomax.rvs(c=c, loc=loc, scale=scale, size=self.size-1, random_state=self.seed).cumsum().tolist()
        ts = [last-timedelta(seconds=t*60) for t in ts_]
        return ts[::-1]

    def _generate_users(self):
        """Generate list of users.

        Returns:
            list: List of name of the users sending the messages.

        """
        return np.random.choice(self.users, self.size)

    def _generate_df(self, last_timestamp=None):
        """Generate random chat as DataFrame.

        Args:
            last_timestamp (datetime, optional): Datetime of last message. If ``None``, defaults to current date.

        Returns:
            pandas.DataFrame: DataFrame with random messages.

        """
        messages = self._generate_messages()
        timestamps = self._generate_timestamps(last=last_timestamp)
        users = self._generate_users()
        df = pd.DataFrame.from_dict({
            COLNAMES_DF.DATE: timestamps,
            COLNAMES_DF.USERNAME: users,
            COLNAMES_DF.MESSAGE: messages
        })
        return df

    def generate(self, filepath=None, hformat=None, last_timestamp=None):
        """Generate random chat as :func:`WhatsAppChat <whatstk.whatsapp.objects.WhatsAppChat>`.

        Args:
            filepath (str): If given, generated chat is saved with name ``filepath`` (must be a local path).
            hformat (str, optional): :ref:`Format of the header <The header format>`, e.g.
                                    ``'[%y-%m-%d %H:%M:%S] - %name:'``.
            last_timestamp (datetime, optional): Datetime of last message. If `None`, defaults to current date.

        Returns:
            WhatsAppChat: Chat with random messages.

        ..  seealso::

            * :func:`WhatsAppChat.to_txt <whatstk.whatsapp.objects.WhatsAppChat.to_txt>`

        """
        df = self._generate_df(last_timestamp=last_timestamp)
        chat = WhatsAppChat(df)
        if filepath:
            chat.to_txt(filepath=filepath, hformat=hformat)
        return chat


def generate_chats_hformats(output_path, size=2000, hformats=None, filepaths=None,
                            last_timestamp=None, seed=100, verbose=False):
    r"""Generate a chat and export using given header format.

    If no hformat specified, chat is generated & exported using all supported header formats.

    Args:
        output_path (str): Path to directory to export all generated chats as txt.
        size (int, optional): Number of messages of the chat. Defaults to 2000.
        hformats (list, optional): List of header formats to use when exporting chat. If None,
                                    defaults to all supported header formats.
        filepaths (list, optional): List with filepaths. If None, defaults to
                                    `hformat.replace(' ', '_').replace('/', '\\')`.
        last_timestamp (datetime, optional): Datetime of last message. If `None`, defaults to current date.
        seed (int, optional): Seed for random processes. Defaults to 100.
        verbose (bool): Set to True to print runtime messages.

    ..  seealso::

            * :func:`ChatGenerator <ChatGenerator>`
            * :func:`ChatGenerator.generate <ChatGenerator.generate>`

    """
    if not hformats:
        hformats = get_supported_hformats_as_list()
    chat = ChatGenerator(size=size, seed=seed).generate(last_timestamp=last_timestamp)
    for i in range(len(hformats)):
        hformat = hformats[i]
        print("Exporting format: {}".format(hformat)) if verbose else 0
        if filepaths:
            filepath = filepaths[i]
        else:
            filepath = '{}.txt'.format(hformat.replace(' ', '_').replace('/', '\\'))
        filepath = os.path.join(output_path, filepath)
        chat.to_txt(filepath=filepath, hformat=hformat)
