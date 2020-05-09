from datetime import datetime, timedelta
from lorem_text import lorem
from scipy.stats import lomax
import numpy as np
import pandas as pd
from whatstk.objects import WhatsAppChat


USERS = [
    'John', 'Mary', 'Giuseppe'
]

class ChatGenerator:
    """Generate a chat."""


    def __init__(self, size, users=None):
        """Instantiate ChatGenerator class.

        Args:
            size (int): Number of messages to generate.
            users (list, optional): List with names of the users. Defaults to module variable USERS.

        """
        self.size = size
        self.users = USERS if not users else users
    
    def generate_messages(self):
        """Generate list of messages.

        To generate sentences, Lorem Ipsum is used.

        Returns:
            list: List with messages (as strings).

        """
        messages = [lorem.sentence() for i in range(self.size)]
        return messages

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
        c = 1.0365
        scale = 1.06
        loc = 20
        ts_ = [0] + np.round(lomax.rvs(c=c, loc=loc, scale=scale, size=self.size-1, random_state=100)).cumsum().tolist()
        ts = [last-timedelta(minutes=t) for t in ts_]
        return ts[::-1]

    def generate_users(self):
        """Generate list of users.

        Returns:
            list: List of name of the users sending the messages.

        """
        return np.random.choice(self.users, self.size)

    def generate_df(self):
        """Generate random chat as DataFrame.

        Returns:
            pandas.DataFrame: DataFrame with random messages.

        """
        messages = self.generate_messages()
        timestamps = self.generate_timestamps()
        users = self.generate_users()
        df = pd.DataFrame.from_dict({
            'date': timestamps,
            'username': users,
            'message': messages
        }).set_index('date')
        return df
    
    def generate(self, filename=None, hformat=None):
        """Generate random chat as WhatsAppChat.

        Args:
            filename (str): Set to a string name to export the generated chat. Must have txt format.
            hformat (str): Header format of the text to be generated. If None, defaults to '%Y-%m-%d, %H:%M - %name:'.

        Returns:
            WhatsAppChat: Chat with random messages.

        """
        if not hformat:
            hformat = '%Y-%m-%d, %H:%M - %name:'
        df = self.generate_df()
        chat = WhatsAppChat(df)
        if filename:
            self.export(chat=chat, filename=filename, hformat=hformat)
        return chat

    def export(self, chat, filename, hformat=None):
        """Export chat as txt file.

        Args:
            chat (WhatsAppChat): Chat as WhatsAppChat instance.
            filename (str): Name of the file.
            hformat (str, optional): Format of the header. Defaults to '%Y-%m-%d, %H:%M - %name:'.

        """
        if not hformat:
            hformat = '%Y-%m-%d, %H:%M - %name:'
        chat.to_txt(filename=filename, hformat=hformat)
