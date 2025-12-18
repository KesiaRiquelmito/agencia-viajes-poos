import json

from exceptions.database import DatabaseError, AlreadyExistsError
from models.destination import Destination


class DestinationDAO:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    @staticmethod
    def list_destinations(db):
        try:
            rows = db.fetch_all("SELECT id, name, description, activities, cost FROM destinations")
            destinations = []
            for row in rows:
                destination_id, name, description, activities_json, cost = row
                activities = json.loads(activities_json)
                destination = Destination(name, description, activities, cost)
                destinations.append((destination_id, destination))
            return destinations
        except DatabaseError:
            raise

    def save(self, destination: Destination):
        name = destination.name
        description = destination.description
        activities = destination.activities
        cost = destination.cost
        activities_json = json.dumps(activities)

        try:
            exists = self.db_connection.fetch_all(
                "SELECT id FROM destinations WHERE name = %s", (name,)
            )
            if exists:
                raise AlreadyExistsError
            cursor = self.db_connection.execute(
                "INSERT INTO destinations (name, description, activities, cost) VALUES (%s, %s, %s, %s)",
                (name, description, activities_json, cost),
            )
            return cursor.lastrowid
        except DatabaseError:
            raise
