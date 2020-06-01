"""Python wrapper and analysis tools for WhatsApp chats.

This library provides a powerful wrapper for multiple Languages and OS. In addition, analytics tools are provided.

"""


from whatstk.core import df_from_txt, df_from_multiple_txt


name = "whatstk"

__version__ = "0.3.0dev0"

__all__ = [
    'df_from_txt',
    'df_from_multiple_txt'
]
