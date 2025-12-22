"""User domain representation."""


class User:
    """Represent a person interacting with the platform."""

    def __init__(self, name, last_name, email, hashed_password, role):
        self.name = name
        self.last_name = last_name
        self.email = email
        self.hashed_password = hashed_password
        self.role = role
