class DatabaseError(Exception):
    pass


class AlreadyExistsError(Exception):
    pass

class UserNotFound(Exception):
    pass

class InvalidPassword(Exception):
    pass

class DestinationNotFound(Exception):
    pass
