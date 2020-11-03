"""Library objects."""


from copy import deepcopy
from whatstk.utils.chat_merge import merge_chats
from whatstk.utils.utils import COLNAMES_DF


class BaseChat:
    """Base chat object.

    Attributes:
        df: Chat as pandas.DataFrame.

    ..  seealso::

        * :func:`WhatsAppChat <whatstk.whatsapp.objects.WhatsAppChat>`

    """

    def __init__(self, df, platform=None):
        """Constructor.

        Args:
            df (pandas.DataFrame): Chat.
            platform (str): Name of the platform, e.g. 'whatsapp'.

        """
        self._df = df
        self._platform = platform

    @property
    def df(self):
        """Chat as DataFrame.

        Returns:
            pandas.DataFrame
        """
        return self._df

    @property
    def users(self):
        """List with users.

        Returns:
            list
        """
        return sorted(list(self.df[COLNAMES_DF.USERNAME].unique()))

    @property
    def start_date(self):
        """Chat starting date.

        Returns:
            datetime

        """
        return self.df[COLNAMES_DF.DATE].min()

    @property
    def end_date(self):
        """Chat end date.

        Returns:
            datetime

        """
        return self.df[COLNAMES_DF.DATE].max()

    @classmethod
    def from_source(cls, **kwargs):
        """Load chat.

        Args:
            kwargs: Specific to the child class.

        Raises:
            NotImplementedError: Must be implemented in children.

        ..  seealso::

            * :func:`WhatsAppChat.from_source <whatstk.WhatsAppChat.from_source>`

        """
        raise NotImplementedError

    def merge(self, chat, rename_users=None):
        """Merge current instance with ``chat``.

        Args:
            chat (WhatsAppChat): Another chat.
            rename_users (dict): Dictionary mapping old names to new names. Example: {'John':['Jon', 'J'], 'Ray':
                                 ['Raymond']} will map 'Jon' and 'J' to 'John', and 'Raymond' to 'Ray'. Note that old
                                 names must come as list (even if there is only one).

        Returns:
            WhatsAppChat: Merged chat.

        ..  seealso::

            * :func:`rename_users <whatstk.whatsapp.objects.WhatsAppChat.rename_users>`
            * :func:`merge_chats <whatstk.utils.chat_merge.merge_chats>`

        Example:
            Merging two chats can become handy when you have exported a chat in different times with your phone and
            hence each exported file might contain data that is unique to that file.

            In this example however, we merge files from different chats.

            ..  code-block:: python

                >>> from whatstk.whatsapp.objects import WhatsAppChat
                >>> from whatstk.data import whatsapp_urls
                >>> filepath_1 = whatsapp_urls.LOREM1
                >>> filepath_2 = whatsapp_urls.LOREM2
                >>> chat_1 = WhatsAppChat.from_source(filepath=filepath_1)
                >>> chat_2 = WhatsAppChat.from_source(filepath=filepath_2)
                >>> chat = chat_1.merge(chat_2)

        """
        self_ = deepcopy(self)
        self_._df = merge_chats([self.df, chat.df])
        if rename_users:
            self_ = self_.rename_users(mapping=rename_users)
        return self_

    def rename_users(self, mapping):
        """Rename users.

        This might be needed in multiple occations:

            - Change typos in user names stored in phone.
            - If a user appears multiple times with different usernames, group these under the same name (this might
                happen when multiple chats are merged).

        Args:
            mapping (dict): Dictionary mapping old names to new names, example:
                            {'John': ['Jon', 'J'], 'Ray': ['Raymond']} will map 'Jon' and 'J' to 'John', and 'Raymond'
                            to 'Ray'. Note that old names must come as list (even if there is only one).

        Returns:
            pandas.DataFrame: DataFrame with users renamed according to `mapping`.

        Raises:
            ValueError: Raised if mapping is not correct.

        Examples:
            Load LOREM2 chat and rename users `Maria` and `Maria2` to `Mary`.

            ..  code-block:: python

                >>> from whatstk.whatsapp.objects import WhatsAppChat
                >>> from whatstk.data import whatsapp_urls
                >>> chat = WhatsAppChat.from_source(filepath=whatsapp_urls.LOREM2)
                >>> chat.users
                ['+1 123 456 789', 'Giuseppe', 'John', 'Maria', 'Maria2']
                >>> chat = chat.rename_users(mapping={'Mary': ['Maria', 'Maria2']})
                >>> chat.users
                ['+1 123 456 789', 'Giuseppe', 'John', 'Mary']

        """
        self_ = deepcopy(self)
        for new_name, old_names in mapping.items():
            if not isinstance(old_names, list):
                raise ValueError("Old names must come as a list of str (even if there is only one).")
            for old_name in old_names:
                self_.df[COLNAMES_DF.USERNAME][self_.df[COLNAMES_DF.USERNAME] == old_name] = new_name
        return self_

    def to_csv(self, filepath):
        """Save chat as csv.

        Args:
            filepath (str): Name of file.

        """
        if not filepath.endswith('.csv'):
            raise ValueError("filepath must end with .csv")
        self.df.to_csv(filepath)

    def __len__(self):
        """Number of messages.

        Returns:
            int: Instance length, defined as number of samples.

        """
        return len(self.df)
