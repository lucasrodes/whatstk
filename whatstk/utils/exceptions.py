"""Library exceptions."""


class RegexError(Exception):
    """To be raised when regex match is not possible."""
    pass


class HFormatError(Exception):
    """To be raised when hformat could not be found."""
    pass
