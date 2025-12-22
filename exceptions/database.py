class DatabaseError(Exception):
    """Generic database error."""
    pass


class AlreadyExistsError(Exception):
    """Raised when an entity uniqueness constraint fails."""
    pass


class UserNotFound(Exception):
    """Raised when looking up a user that does not exist."""
    pass


class InvalidPassword(Exception):
    """Raised when password verification fails."""
    pass


class DestinationNotFound(Exception):
    """Raised when destination retrieval fails."""
    pass


class ReservationNotFound(Exception):
    """Raised when reservation retrieval fails."""
    pass


class DeletionNotCompleted(Exception):
    """Raised when deletion operation returns no affected rows."""
    pass
