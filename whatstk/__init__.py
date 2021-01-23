"""Python wrapper and analysis tools for WhatsApp chats.

This library provides a powerful wrapper for multiple Languages and OS. In addition, analytics tools are provided.

"""


from whatstk.whatsapp.objects import WhatsAppChat
from whatstk.graph import FigureBuilder


name = "whatstk"

__version__ = "0.4.0.dev0"

__all__ = [
    'WhatsAppChat',
    'FigureBuilder'
]
