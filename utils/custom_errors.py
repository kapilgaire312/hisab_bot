class DatabaseCreationFailedError(Exception):
    """Error raised when it fails to create databse and tables."""
    pass

class UserTableInitializeError(Exception):
    """Error raised when it fails to add users to the users table."""
    pass
