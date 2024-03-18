"""Library objects."""


from copy import deepcopy
import pandas as pd
from typing import Optional, List, Union, Dict, Any, Tuple
from datetime import datetime

from whatstk.utils.chat_merge import merge_chats
from whatstk.utils.utils import COLNAMES_DF


class BaseChat:
    """Base chat object.

    Attributes:
        df: Chat as pandas.DataFrame.

    ..  seealso::

        * :func:`WhatsAppChat <whatstk.whatsapp.objects.WhatsAppChat>`

    """

    def __init__(self, df: pd.DataFrame, platform: Optional[str] = None) -> None:
        """Constructor.

        Args:
            df (pandas.DataFrame): Chat.
            platform (str): Name of the platform, e.g. 'whatsapp'.

        """
        self._df_raw = df
        self._df, self._df_system, self._name = self._build_dfs(df.copy())
        self._platform = platform

    def _build_dfs(self, df_raw: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, str]:
        if (COLNAMES_DF.MESSAGE_TYPE in df_raw.columns) and self.is_group:
            mask = df_raw[COLNAMES_DF.MESSAGE_TYPE] == "system"
            # Get chat only with user messages
            df = df_raw.loc[~mask].drop(columns=COLNAMES_DF.MESSAGE_TYPE)
            # Get chat only with system messages
            df_system = df_raw.loc[mask].drop(columns=COLNAMES_DF.MESSAGE_TYPE)
            # Get system messages dataframe
            if len(set(df_system[COLNAMES_DF.USERNAME])) != 1:
                raise ValueError("System messages dataframe must contain only one username.")
            chat_name = df_system[COLNAMES_DF.USERNAME].iloc[0]
            # Drop 'username' from system dataframe
            df_system = df_system.drop(columns=COLNAMES_DF.USERNAME)
            return df, df_system, chat_name
        if (COLNAMES_DF.MESSAGE_TYPE in df_raw.columns) and not self.is_group:
            df_raw = df_raw.drop(columns=COLNAMES_DF.MESSAGE_TYPE)
        return df_raw, pd.DataFrame(), ""

    @property
    def df(self) -> pd.DataFrame:
        """Chat as DataFrame.

        Returns:
            pandas.DataFrame
        """
        return self._df

    @property
    def df_system(self) -> pd.DataFrame:
        """Chat as DataFrame.

        Returns:
            pandas.DataFrame
        """
        return self._df_system

    @property
    def is_group(self) -> bool:
        """True if the chart is a group.

        A chat is detected as a group if it has more than 2 users (including the 'system').
        Groups with one person will not be detected as groups.

        Returns:
            bool
        """
        if len(set(self._df_raw[COLNAMES_DF.USERNAME])) > 2:
            return True
        return False

    @property
    def users(self) -> List[str]:
        """List with users.

        Returns:
            list
        """
        return sorted(list(self.df[COLNAMES_DF.USERNAME].unique()))

    @property
    def name(self) -> Optional[str]:
        """Name of the chat.

        Returns None if no name could be found. The name is extracted from the username of with
        the first system message in the chat.

        Returns:
            list
        """
        return self._name

    @property
    def start_date(self) -> Union[str, datetime]:
        """Chat starting date.

        Returns:
            datetime

        """
        return self._df_raw[COLNAMES_DF.DATE].min()

    @property
    def end_date(self) -> Union[str, datetime]:
        """Chat end date.

        Returns:
            datetime

        """
        return self._df_raw[COLNAMES_DF.DATE].max()

    @classmethod
    def from_source(cls, **kwargs: Any) -> None:  # noqa: ANN401
        """Load chat.

        Args:
            kwargs: Specific to the child class.

        Raises:
            NotImplementedError: Must be implemented in children.

        ..  seealso::

            * :func:`WhatsAppChat.from_source <whatstk.WhatsAppChat.from_source>`

        """
        raise NotImplementedError

    def merge(self, chat: "BaseChat", rename_users: Optional[Dict[str, str]] = None) -> "BaseChat":
        """Merge current instance with ``chat``.

        Args:
            chat (WhatsAppChat): Another chat.
            rename_users (dict): Dictionary mapping old names to new names. Example: {'John':['Jon', 'J'], 'Ray':
                                 ['Raymond']} will map 'Jon' and 'J' to 'John', and 'Raymond' to 'Ray'. Note that old
                                 names must come as list (even if there is only one).

        Returns:
            BaseChat: Merged chat.

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
        # Can only merge from same platform
        if self._platform != chat._platform:
            raise ValueError("Both chats must come from the same platform.")
        # Merge
        self_ = deepcopy(self)
        self_._df_raw = merge_chats([self._df_raw, chat._df_raw])
        self_._df = merge_chats([self.df, chat.df])
        if (not self.df_system.empty) and (not chat.df_system.empty):
            self_._df_system = merge_chats([self.df_system, chat.df_system])
        if rename_users:
            self_ = self_.rename_users(mapping=rename_users)
        return self_

    def rename_users(self, mapping: Dict[str, str]) -> "BaseChat":
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

    def to_csv(self, filepath: str) -> None:
        """Save chat as csv.

        Args:
            filepath (str): Name of file.

        """
        if not filepath.endswith(".csv"):
            raise ValueError("filepath must end with .csv")
        self.df.to_csv(filepath, index=False)

    def __len__(self) -> int:
        """Number of messages.

        Returns:
            int: Instance length, defined as number of samples.

        """
        return len(self.df)
