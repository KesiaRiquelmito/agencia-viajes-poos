"""Controller handling user authentication flows."""

import bcrypt
import pwinput

from exceptions.database import AlreadyExistsError, DatabaseError, UserNotFound, InvalidPassword
from services.user_service import UserService


class UserController:
    """Expose registration and login actions."""

    def __init__(self, db):
        """Initialize controller with the user service."""
        self.user_service = UserService(db)

    def _validate_data(self, data):
        """Ensure user registration payload respects rules."""
        valid_roles = ["admin", "user"]

        if not data["name"]:
            print("El nombre es obligatorio")
            return False
        if not data["last_name"]:
            print("El apellido es obligatorio")
            return False
        if not data["email"]:
            print("El email es obligatorio")
            return False
        if data["role"] not in valid_roles or not data["role"]:
            print("Ingrese un rol valido: admin o user")
            return False
        if not data["password"]:
            print("Debe crear una contraseña")
            return False
        if len(data["password"]) < 8:
            print("La contraseña debe tener 8 carácteres minimo")
            return False
        return True

    def register_user(self):
        """Prompt for and register a new user."""
        print("Registrar usuario")
        name = input("Nombre: ").strip()
        last_name = input("Apellido: ").strip()
        email = input("Email: ").strip()
        role = input("Rol (admin/user): ").strip()
        password = pwinput.pwinput("Ingrese una contraseña: ", mask="*")
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(14))
        hashed_password = hashed_password.decode('utf-8')

        user_data_to_validate = {"name": name, "last_name": last_name, "email": email, "password": password,
                     "role": role}

        if not self._validate_data(user_data_to_validate):
            return None

        user_data = {"name": name, "last_name": last_name, "email": email, "hashed_password": hashed_password,
                     "role": role}

        try:
            user_id = self.user_service.register_user(user_data)
        except AlreadyExistsError:
            print(f"No se puede crear el usuario. El usuario con el email '{email}' ya existe")
            return None
        except DatabaseError:
            print("No se pudo registrar el usuario debido a un error en la base de datos")
            return None

        print(f"Usuario {name} {last_name} registrado exitosamente")
        return user_id

    def signin(self):
        """Authenticate an existing user."""
        print("---Inicio de sesión---")
        email = input("Ingresa tu email: ")
        password = pwinput.pwinput("Ingresa tu contraseña: ", mask="*")

        try:
            user_credentials = self.user_service.login(email, password)
        except DatabaseError:
            return None
        except UserNotFound:
            print(f"El usuario con el email {email} no existe")
            return None
        except InvalidPassword:
            print("La contraseña no es correcta, intenta nuevamente")
            return None
        print("Inicio de sesión exitoso")
        return user_credentials
