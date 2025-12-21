from controllers.destination_controller import DestinationController
from db.database import Database


class Menu:
    def __init__(self):
        self.db = Database()
        self.destination_controller = DestinationController(self.db)

    def start(self):
        self.destination_controller.list_destinations()
