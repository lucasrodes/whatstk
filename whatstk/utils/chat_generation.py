"""Chat generation utils.

Use this module functions to generate chats.
"""


import os
from datetime import datetime, timedelta
import itertools
import numpy as np
import pandas as pd
from scipy.stats import lomax
from lorem import sentence
from emoji.unicode_codes import EMOJI_UNICODE
from whatstk.objects import WhatsAppChat
from whatstk.utils.hformat import get_supported_hformats_as_list
from whatstk.utils.utils import COLNAMES_DF


USERS = [
    'John', 'Mary', 'Giuseppe', '+1 123 456 789'
]


class ChatGenerator:
    """Generate a chat."""

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

    def generate_messages(self):
        """Generate list of messages.

        To generate sentences, Lorem Ipsum is used.

        Returns:
            list: List with messages (as strings).

        """
        emojis = self.generate_emojis()
        s = sentence(count=self.size, comma=(0, 2), word_range=(4, 8))
        sentences = list(itertools.islice(s, self.size))
        messages = [sentences[i] + ' ' + emojis[i] for i in range(self.size)]
        return messages

    def generate_emojis(self, k=1):
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

    def generate_timestamps(self, last=None):
        """Generate list of timestamps.

        Args:
            last (datetime, optional): Datetime of last message. If `None`, defaults to current date.

        Returns:
            [type]: [description]
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

    def generate_users(self):
        """Generate list of users.

        Returns:
            list: List of name of the users sending the messages.

        """
        return np.random.choice(self.users, self.size)

    def generate_df(self, last_timestamp=None):
        """Generate random chat as DataFrame.

        Args:
            last_timestamp (datetime, optional): Datetime of last message. If `None`, defaults to current date.

        Returns:
            pandas.DataFrame: DataFrame with random messages.

        """
        messages = self.generate_messages()
        timestamps = self.generate_timestamps(last=last_timestamp)
        users = self.generate_users()
        df = pd.DataFrame.from_dict({
            COLNAMES_DF.DATE: timestamps,
            COLNAMES_DF.USERNAME: users,
            COLNAMES_DF.MESSAGE: messages
        }).set_index(COLNAMES_DF.DATE)
        return df

    def generate(self, filename=None, hformat=None, last_timestamp=None):
        """Generate random chat as WhatsAppChat.

        Args:
            filename (str): Set to a string name to export the generated chat. Must have txt format.
            hformat (str): Header format of the text to be generated. If None, defaults to '%y-%m-%d, %H:%M - %name:'.
            last_timestamp (datetime, optional): Datetime of last message. If `None`, defaults to current date.

        Returns:
            WhatsAppChat: Chat with random messages.

        """
        df = self.generate_df(last_timestamp=last_timestamp)
        chat = WhatsAppChat(df)
        if filename:
            chat.to_txt(filename=filename, hformat=hformat)
        return chat


def generate_chats_hformats(output_path, size=2000, hformats=None, filenames=None,
                            last_timestamp=None, seed=100, verbose=False):
    r"""Generate a chat and export using given header format.

    If no hformat specified, chat is generated & exported using all supported header formats.

    Args:
        output_path (str): Path to directory to export all generated chats as txt.
        size (int, optional): Number of messages of the chat. Defaults to 2000.
        hformats (list, optional): List of header formats to use when exporting chat. If None,
                                    defaults to all supported header formats.
        filenames (list, optional): List with filenames. If None, defaults to
                                    `hformat.replace(' ', '_').replace('/', '\\')`.
        last_timestamp (datetime, optional): Datetime of last message. If `None`, defaults to current date.
        seed (int, optional): Seed for random processes. Defaults to 100.
        verbose (bool): Set to True to print runtime messages.

    """
    if not hformats:
        hformats = get_supported_hformats_as_list()
    chat = ChatGenerator(size=size, seed=seed).generate(last_timestamp=last_timestamp)
    for i in range(len(hformats)):
        hformat = hformats[i]
        print("Exporting format: {}".format(hformat)) if verbose else 0
        if filenames:
            filename = filenames[i]
        else:
            filename = '{}.txt'.format(hformat.replace(' ', '_').replace('/', '\\'))
        filepath = os.path.join(output_path, filename)
        chat.to_txt(filename=filepath, hformat=hformat)
