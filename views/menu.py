from controllers.destination_controller import DestinationController
from controllers.package_controller import PackageController
from controllers.user_controller import UserController
from db.database import Database


class Menu:
    def __init__(self):
        self.db = Database()
        self.destination_controller = DestinationController(self.db)
        self.user_controller = UserController(self.db)
        self.package_controller = PackageController(self.db)

    def start(self):
        self.destination_controller.list_destinations()
