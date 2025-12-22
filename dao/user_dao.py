"""DAO for user persistence and credential retrieval."""

from exceptions.database import AlreadyExistsError, DatabaseError, UserNotFound
from models.user import User


class UserDAO:
    """Implement create and lookup operations for users."""

    def __init__(self, db_connection):
        """Cache DB connection."""
        self.db_connection = db_connection

    def create_user(self, user: User):
        """Create a user row from a domain object."""
        name = user.name
        last_name = user.last_name
        email = user.email
        hashed_password = user.hashed_password
        role = user.role

        try:
            exist = self.db_connection.fetch_all(
                "SELECT id FROM users WHERE email = %s", (email,)
            )
            if exist:
                raise AlreadyExistsError
            cursor = self.db_connection.execute(
                "INSERT INTO users (name, last_name, email, hashed_password, role) VALUES (%s, %s, %s, %s, %s)",
                (name, last_name, email, hashed_password, role)
            )
            return cursor.lastrowid
        except DatabaseError:
            raise

    def get_credentials(self, email):
        """Return credentials tuple for authentication."""
        try:
            rows = self.db_connection.fetch_all(
                "SELECT id, email, hashed_password, role FROM users WHERE email = %s",
                (email,),
            )
            return rows[0]
        except UserNotFound:
            raise
