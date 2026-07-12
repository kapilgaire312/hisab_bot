class DatabaseCreationFailedError(Exception):
    """Error raised when it fails to create databse and tables."""

    pass


class UserTableInitializeError(Exception):
    """Error raised when it fails to add users to the users table."""

    pass


class TimestampInitializeError(Exception):
    """Error raised when it fails to initialize the cleard_timestamp."""

    pass


class UserIdsFetchError(Exception):
    """Error raised when it fails to fetch the users ids."""

    pass


class ExpenseSaveError(Exception):
    """Errror raised when it fails to save the expense or participants"""

    pass


class RepaymentSaveError(Exception):
    """Error raised when it fails to save the repayment to databse"""

    pass


class BalanceFetchError(Exception):
    """Error raised when it fails to retrieve the balance info of the member."""

    pass


class HistoryFetchError(Exception):
    """Error raised when it fails to retrieve history of expenses and payments from db."""

    pass
