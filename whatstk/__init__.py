"""Python wrapper and analysis tools for WhatsApp chats.

This library provides a powerful wrapper for multiple Languages and OS. In addition, analytics tools are provided.

"""

from typing import TYPE_CHECKING, Any

from whatstk.whatsapp.objects import WhatsAppChat
from whatstk.whatsapp.parser import df_from_whatsapp

if TYPE_CHECKING:  # pragma: no cover
    from whatstk.graph import FigureBuilder  # noqa: F401


name = "whatstk"

__version__ = "0.9.1"

__all__ = [
    "WhatsAppChat",
    "df_from_whatsapp",
    "FigureBuilder",
]


def __getattr__(name: str) -> Any:  # noqa: ANN401
    """Resolve FigureBuilder on first use.

    Plotting lives behind the ``viz`` extra, so importing it eagerly would make ``import whatstk``
    fail for anyone who installed the library just to parse chats.
    """
    if name == "FigureBuilder":
        from whatstk.graph import FigureBuilder

        return FigureBuilder
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
