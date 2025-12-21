from exceptions.database import DatabaseError, AlreadyExistsError
from models.destination import Destination
from dao.destination_dao import DestinationDAO


class DestinationService:
    def __init__(self, db):
        self.db = db
        self.destination_dao = DestinationDAO(db)

    def create_destination(self, destination_data):
        destination = Destination(
            destination_data["name"],
            destination_data["description"],
            destination_data["activities"],
            destination_data["cost"],
        )
        return self.destination_dao.save(destination)

    def get_all_destinations(self):
        return self.destination_dao.get_all()
