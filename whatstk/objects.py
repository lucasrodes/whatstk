from whatstk.utils.parser import generate_regex, parse_chat, remove_alerts_from_df
from whatstk.utils.auto_header import extract_header_from_text



class WhatsAppChat:
    """Use this class to load and play with your chat log."""

    def __init__(self, df):
        """Constructor."""
        self.df = df
        self.users = self.df.username.unique().tolist()

    @classmethod
    def from_txt(cls, filename, auto_header=True, hformat=None, encoding='utf-8'):
        """Create instance from chat log txt file hosted locally.
        
        Args:

            filename (str): Name to the txt chat log file.
            auto_header (bool): Set to True to detect header automatically, otherwise set to False. Defaults to True. If
                                False, you have to provide a value to `hformat`.
            hformat (str): Format of the header. Check `whatstk.WhatsAppChat.prepare_df` docs.
            encoding (str): Required to load file. Default is 'utf-8'. Should be working. Report any incidence.
            
        Returns:
            WhatsAppChat: Class instance with loaded and parsed chat.

        """
        # Read file
        with open(filename, encoding=encoding) as f:
            text = f.read()

        if not hformat and auto_header:
            hformat = extract_header_from_text(text)
            if not hformat:
                raise RuntimeError("Header automatic extraction failed. Please specify the format manually by setting"
                                   " input argument `hformat`.")
        elif not (hformat or auto_header):
            raise ValueError("If auto_header is False, hformat can't be None.")

        # Bracket is reserved character in RegEx, add backslash before them.
        hformat.replace('[', '\[').replace(']', '\]')
        # Prepare DataFrame
        df = cls._prepare_df(text, hformat)

        return cls(df)

    @staticmethod
    def _prepare_df(text, hformat):
        """Get a DataFrame-formatted chat.

        Args:
            text (str): Loaded chat as plain text.
            hformat (str): Format of the header. Ude the following keywords:
                            - %y: for year.
                            - %m: for month.
                            - %d: for day.
                            - %H: for hour.
                            - %M: for minutes.
                            - %S: for seconds.
                            - %P: To denote 12h clock.
                            - %name: for the username

                            Example 1: To the header '12/08/2016, 16:20 - username:' corresponds the syntax
                            '%d/%m/%y, %H:%M - %name:'.

                            Example 2: To the header '2016-08-12, 4:20 PM - username:' corresponds the syntax
                            '%y-%m-%d, %H:%M %P - %name:'.
        Returns:
            pandas.DataFrame: DataFrame containing the chat.

        """
        # generate regex
        r, r_x = generate_regex(hformat=hformat)
        # print(r)

        # Parse chat to DataFrame
        df = parse_chat(text, r)

        # get rid of wp warning messages
        return remove_alerts_from_df(r_x, df)

    def to_csv(self, filename):
        """Save data as csv.

        Args:
            filename (str): Name of file.

        """
        self.df.to_csv(filename)

    def __len__(self):
        """Get length of DataFrame

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