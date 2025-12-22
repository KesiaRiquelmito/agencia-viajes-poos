"""Service containing user registration and auth logic."""

import bcrypt

from dao.user_dao import UserDAO
from exceptions.database import InvalidPassword
from models.user import User


class UserService:
    """Persist and authenticate users."""

    def __init__(self, db):
        """Cache DB connection and DAO instance."""
        self.db = db
        self.user_dao = UserDAO(db)

    def register_user(self, user_data):
        """Create a user and return its identifier."""
        user = User(
            user_data["name"],
            user_data["last_name"],
            user_data["email"],
            user_data["hashed_password"],
            user_data["role"],
        )
        return self.user_dao.create_user(user)

    def login(self, email, password):
        """Validate user credentials and return auth payload."""
        user_id, user_email, user_hashed_password, role = self.user_dao.get_credentials(email)
        is_valid_password = bcrypt.checkpw(password.encode('utf-8'), user_hashed_password.encode('utf-8'))
        if not is_valid_password:
            raise InvalidPassword
        return {"id": user_id, "email": user_email, "role": role}
