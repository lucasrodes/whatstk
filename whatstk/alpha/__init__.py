"""Will be deprecated"""


import sys
import warnings
from whatstk.utils import parser, auto_header, exceptions


warnings.warn("whatstk.alpha is deprecated, use whatstk.utils instead.", FutureWarning)

# Or simply
__all__ = [
    'parser',
    'auto_header',
    'exceptions'
]