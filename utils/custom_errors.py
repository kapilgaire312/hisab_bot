class DatabaseCreationFailedError(Exception):
    """Error raised when it fails to create databse and tables."""

    pass


class UserTableInitializeError(Exception):
    """Error raised when it fails to add users to the users table."""

    pass


class UserIdsFetchError(Exception):
    """Error raised when it fails to fetch the users ids."""

    pass


class ExpenseSaveError(Exception):
    """Errror raised when it fails to save the expense or participants"""

    pass
