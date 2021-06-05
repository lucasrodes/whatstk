"""Python wrapper and analysis tools for WhatsApp chats.

This library provides a powerful wrapper for multiple Languages and OS. In addition, analytics tools are provided.

"""


from whatstk.whatsapp.objects import WhatsAppChat
from whatstk.graph import FigureBuilder
from whatstk.whatsapp.parser import df_from_txt_whatsapp


name = "whatstk"

__version__ = "0.5.0.rc1"

__all__ = [
    'WhatsAppChat',
    'df_from_txt_whatsapp',
    'FigureBuilder',
]
