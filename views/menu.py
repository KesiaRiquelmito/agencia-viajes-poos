from controllers.destination_controller import DestinationController
from controllers.package_controller import PackageController
from controllers.reservation_controller import ReservationController
from controllers.user_controller import UserController
from db.database import Database


class Menu:
    def __init__(self):
        self.db = Database()
        self.user_controller = UserController(self.db)
        self.current_user = None
        self.destination_controller = DestinationController(self.db)
        self.package_controller = PackageController(self.db)
        self.reservation_controller = ReservationController(self.db)

    def login_flow(self):
        credentials = self.user_controller.signin()
        if credentials:
            self.current_user = credentials

    def require_role(self, current_user, allowed_roles):
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
        self.create_reservation_action()
        # self.destination_controller.list_destinations()
        # self.user_controller.signin()
        self.user_controller.register_user()
        self.package_controller.list_packages()

    def create_destination_action(self):
        if not self.require_role(self.current_user, ["admin"]):
            return
        self.destination_controller.create_destination()

    def create_reservation_action(self):
        if not self.require_role(self.current_user, ["user"]):
            return
        self.reservation_controller.create_reservation(self.current_user["id"])

    def create_package_action(self):
        if not self.require_role(self.current_user, ["admin"]):
            return
        self.package_controller.create_package()