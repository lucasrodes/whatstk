"""Library objects."""


from copy import deepcopy
from whatstk.utils.chat_merge import merge_chats
from whatstk.utils.utils import COLNAMES_DF


class BaseChat:
    """Use this class to load and process your chat text file.

    Attributes:
        df: Chat as pandas.DataFrame.

    """

    def __init__(self, df, platform=None):
        """Constructor.

        Args:
            df (pandas.DataFrame): Chat.
            platform (str): Name of the platform, e.g. 'whatsapp'.

        """
        self.df = df
        self._platform = platform

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
        return self.df.index.min()

    @property
    def end_date(self):
        """Chat end date.

        Returns:
            list

        """
        return self.df.index.max()

    def merge(self, chat, rename_users=None):
        """Merge current instance with `chat`.

        Args:
            chat (WhatsAppChat): Another chat.
            rename_users (dict): Dictionary mapping old names to new names,
                                    example: {'John':['Jon', 'J'], 'Ray': ['Raymond']} will map 'Jon' and 'J' to
                                    'John', and 'Raymond' to 'Ray'.

        Returns:
            WhatsAppChat: Merged chat.

        """
        self_ = deepcopy(self)
        self_.df = merge_chats([self.df, chat.df])
        if rename_users:
            self_ = self_.rename_users(mapping=rename_users)
        return self_

    def rename_users(self, mapping):
        """Rename users.

        Args:
            mapping (dict): Dictionary mapping old names to new names, example:
                            {'John':['Jon', 'J'], 'Ray': ['Raymond']} will map 'Jon' and 'J' to 'John', and 'Raymond'
                            to 'Ray'.

        Returns:
            pandas.DataFrame: DataFrame with users renamed according to `mapping`.

        Raises:
            ValueError: Raised if mapping is not correct.

        """
        self_ = deepcopy(self)
        for new_name, old_names in mapping.items():
            if not isinstance(old_names, list):
                raise ValueError("Old names must come as a list of str (even if there is only one).")
            for old_name in old_names:
                self_.df[COLNAMES_DF.USERNAME][self_.df[COLNAMES_DF.USERNAME] == old_name] = new_name
        return self_

    def to_csv(self, filename):
        """Save data as csv.

        Args:
            filename (str): Name of file.

        """
        if not filename.endswith('.csv'):
            raise ValueError("filename must end with .csv")
        self.df.to_csv(filename)

    def __len__(self):
        """Get length of DataFrame.

        Returns:
            int: Instance length, defined as number of samples.

        """
        return len(self.df)

    @property
    def shape(self):
        """Get shape of DataFrame-formatted chat.

        Returns:
            tuple: Shape.

        """
        return self.df.shape
