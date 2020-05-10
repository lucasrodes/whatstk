from whatstk.utils.parser import generate_regex, parse_chat, remove_alerts_from_df
from whatstk.utils.auto_header import extract_header_from_text
from whatstk.utils.exceptions import RegexError, HFormatError


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

        if hformat:
            # Bracket is reserved character in RegEx, add backslash before them.
            hformat = hformat.replace('[', '\[').replace(']', '\]')
        if not hformat and auto_header:
            hformat = extract_header_from_text(text)
            if not hformat:
                raise RuntimeError("Header automatic extraction failed. Please specify the format manually by setting"
                                   " input argument `hformat`.")
        elif not (hformat or auto_header):
            raise ValueError("If auto_header is False, hformat can't be None.")
        
        # Prepare DataFrame
        df = cls._prepare_df(text, hformat)

        return cls(df)

    @staticmethod
    def _prepare_df(text, hformat):
        """Get a DataFrame-formatted chat.

        Args:
            text (str): Loaded chat as plain text.
            hformat (str): Format of the header. Ude the following keywords:
                            - %y: for year (%Y is equivalent).
                            - %m: for month.
                            - %d: for day.
                            - %H: for 24h-hour.
                            - %I: for 12h-hour.
                            - %M: for minutes.
                            - %S: for seconds.
                            - %P: for "PM"/"AM" or "p.m."/"a.m." characters.
                            - %name: for the username.

                            Example 1: To the header '12/08/2016, 16:20 - username:' corresponds the `hformat`
                            '%d/%m/%y, %H:%M - %name:'.

                            Example 2: To the header '2016-08-12, 4:20 PM - username:' corresponds the `hformat`
                            '%y-%m-%d, %I:%M %P - %name:'.
        Returns:
            pandas.DataFrame: DataFrame containing the chat.

        """
        # generate regex
        r, r_x = generate_regex(hformat=hformat)

        # Parse chat to DataFrame
        try:
            df = parse_chat(text, r)
        except RegexError:
            raise HFormatError("hformat '{}' did not match the provided text. No match was found".format(hformat))
        # get rid of wp warning messages
        return remove_alerts_from_df(r_x, df)

    def to_txt(self, filename, hformat=None):
        """Export chat as txt file.

        Usefull to export the chat to different formats.

        Args:
            hformat (str, optional): Header format. Defaults to "%y-%m-%d, %H:%M - %name:".
            filename (str): Name of the file to export.

        """
        if not filename.endswith('.txt'):
            raise ValueError("filename must end with .txt")
        if not hformat:
            hformat = "%Y-%m-%d, %H:%M - %name:"
        lines = []
        raw_lines = self.df.reset_index().values.tolist()
        for line in raw_lines:
            date, user, text = line
            hformat = hformat.replace('%name', '{name}')
            header = date.strftime(hformat).format(name=user)
            formatted_line = '{} {}'.format(header, text)
            lines.append(formatted_line)
        text = '\n'.join(lines)
        with open(filename, 'w') as f:
            f.write(text)

    def to_csv(self, filename):
        """Save data as csv.

        Args:
            filename (str): Name of file.

        """
        if not filename.endswith('.csv'):
            raise ValueError("filename must end with .csv")
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