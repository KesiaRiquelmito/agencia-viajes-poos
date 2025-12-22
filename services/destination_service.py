"""Service logic for destinations."""

from exceptions.database import DatabaseError, AlreadyExistsError
from models.destination import Destination
from dao.destination_dao import DestinationDAO


class DestinationService:
    """Coordinate DAO actions for destination entities."""

    def __init__(self, db):
        """Store DB connection and initialize DAO."""
        self.db = db
        self.destination_dao = DestinationDAO(db)

    def create_destination(self, destination_data):
        """Create a destination domain object and persist it."""
        destination = Destination(
            destination_data["name"],
            destination_data["description"],
            destination_data["activities"],
            destination_data["cost"],
        )
        return self.destination_dao.save(destination)

    def get_all_destinations(self):
        """Return every destination stored."""
        return self.destination_dao.get_all()

    def update_destination(self, target, destination_data):
        """Update an existing destination using new data."""
        destination = Destination(
            destination_data["name"],
            destination_data["description"],
            destination_data["activities"],
            destination_data["cost"],
        )
        return self.destination_dao.update(target, destination)

    def delete_destination(self, destination_id):
        """Delete a destination by identifier."""
        return self.destination_dao.delete(destination_id)
