class DatabaseError(Exception):
    pass


class AlreadyExistsError(Exception):
    pass


class DestinationNotFound(Exception):
    pass

class DeletionNotCompleted(Exception):
    pass
