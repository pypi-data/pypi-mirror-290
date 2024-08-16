"""
This module defines exceptions for ClapDB operations. It follows the structure defined in pep-0249.
"""


class Warning(Exception):
    """Warning exception"""


class Error(Exception):
    """Base exception"""


class InterfaceError(Error):
    pass


class DatabaseError(Error):
    pass


class InternalError(DatabaseError):
    pass


class NotSupportedError(DatabaseError):
    pass
