"""Library exceptions."""


class RegexError(Exception):
    """Raised when regex match is not possible."""
    pass


class HFormatError(Exception):
    """Raised when hformat could not be found."""
    pass
