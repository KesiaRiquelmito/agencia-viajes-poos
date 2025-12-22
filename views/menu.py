"""CLI menu orchestrating controllers."""

from controllers.destination_controller import DestinationController
from controllers.package_controller import PackageController
from controllers.reservation_controller import ReservationController
from controllers.user_controller import UserController
from db.database import Database


class Menu:
    """Handle navigation between user, admin, and public flows."""

    def __init__(self):
        """Instantiate controllers and database connection."""
        self.db = Database()
        self.user_controller = UserController(self.db)
        self.current_user = None
        self.destination_controller = DestinationController(self.db)
        self.package_controller = PackageController(self.db)
        self.reservation_controller = ReservationController(self.db)

    def login_flow(self):
        """Perform login and store resulting user."""
        credentials = self.user_controller.signin()
        if credentials:
            self.current_user = credentials

    def logout(self):
        """Clear the current user session."""
        self.current_user = None
        print("Sesión cerrada")

    def require_role(self, current_user, allowed_roles):
        """Validate current user has one of the allowed roles."""
        if not current_user:
            print("Debes iniciar sesión primero")
            self.login_flow()

        if not self.current_user:
            return False

        if self.current_user["role"] not in allowed_roles:
            print("No tienes permisos para esta accion")
            return False
        return True

    def start(self):
        """Entry point for the interactive menu loop."""
        while True:
            print("Bienvenido al sistema de reserva de paquetes turísticos")
            if not self.current_user:
                self.show_public_menu()
                option = input("Elige una opción: ").strip()

                if option == "1":
                    self.get_tourist_packages_action()
                elif option == "2":
                    self.action_register()
                elif option == "3":
                    self.action_login()
                elif option == "0":
                    break
                else:
                    print("Opción invalida")
            else:
                role = self.current_user.get("role")

                if role == "user":
                    self.show_user_menu()
                    option = input("Elige una opcion: ").strip()

                    if option == "1":
                        self.get_tourist_packages_action()
                    elif option == "2":
                        self.create_reservation_action()
                    elif option == "3":
                        self.get_user_reservations()
                    elif option == "4":
                        self.logout()
                    elif option == "0":
                        break
                    else:
                        print("Opcion invalida")
                elif role == "admin":
                    self.show_admin_menu()
                    option = input("Elige una opcion: ").strip()

                    if option == "1":
                        self.get_tourist_packages_action()
                    elif option == "2":
                        self.create_destination_action()
                    elif option == "3":
                        self.create_package_action()
                    elif option == "4":
                        self.manage_destination_action()
                    elif option == "5":
                        self.manage_package_action()
                    elif option == "6":
                        self.logout()
                    elif option == "0":
                        break
                    else:
                        print("Opcion invalida")
                else:
                    print("Rol invalido. Finalizando programa")

    def show_public_menu(self):
        """Display the menu accessible without authentication."""
        print(
            "\nMenú principal\n"
            "1. Ver paquetes turísticos\n"
            "2. Registrarse\n"
            "3. Iniciar sesión\n"
            "0. Salir"
        )

    def show_user_menu(self):
        """Display options available to standard users."""
        print(
            f"\nMenú usuario ({self.current_user['email']})\n"
            "1. Ver paquetes turísticos\n"
            "2. Reservar paquete\n"
            "3. Ver mis reservas\n"
            "4. Cerrar sesion\n"
            "0. Salir"
        )

    def show_admin_menu(self):
        """Display administrative options."""
        print(
            f"\nMenú admin ({self.current_user['email']})\n"
            "1. Ver paquetes turísticos\n"
            "2. Crear destino\n"
            "3. Crear paquete\n"
            "4. Editar o eliminar destino\n"
            "5. Editar o eliminar paquete\n"
            "6. Cerrar sesion\n"
            "0. Salir"
        )

    def action_register(self):
        """Handle registration action."""
        self.user_controller.register_user()

    def action_login(self):
        """Trigger login workflow."""
        self.login_flow()

    def create_destination_action(self):
        """Ensure admin role and invoke destination creation."""
        if not self.require_role(self.current_user, ["admin"]):
            return
        self.destination_controller.create_destination()

    def create_reservation_action(self):
        """Ensure user role and create reservation."""
        if not self.require_role(self.current_user, ["user"]):
            return
        self.reservation_controller.create_reservation(self.current_user["id"])

    def create_package_action(self):
        """Ensure admin role then create packages."""
        if not self.require_role(self.current_user, ["admin"]):
            return
        self.package_controller.create_package()

    def manage_destination_action(self):
        """Ensure admin role before destination edits/deletions."""
        if not self.require_role(self.current_user, ["admin"]):
            return

        print("\n1. Editar destino\n2. Eliminar destino")
        action = input("Selecciona una opción: ").strip()
        if action == "1":
            self.destination_controller.update_destination()
        elif action == "2":
            self.destination_controller.delete_destination()
        else:
            print("Opción invalida")

    def manage_package_action(self):
        """Ensure admin role before package edits/deletions."""
        if not self.require_role(self.current_user, ["admin"]):
            return

        print("\n1. Editar paquete\n2. Eliminar paquete")
        action = input("Selecciona una opción: ").strip()
        if action == "1":
            self.package_controller.update_package()
        elif action == "2":
            self.package_controller.delete_package()
        else:
            print("Opción invalida")

    def get_tourist_packages_action(self):
        """List packages for display."""
        self.package_controller.list_packages()

    def get_user_reservations(self):
        """List reservations for the current user."""
        self.reservation_controller.list_reservations_by_user(self.current_user["id"])
