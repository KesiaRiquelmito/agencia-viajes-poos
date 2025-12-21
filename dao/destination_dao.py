import json

from exceptions.database import DatabaseError, AlreadyExistsError, DestinationNotFound
from models.destination import Destination


class DestinationDAO:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def get_all(self):
        try:
            rows = self.db_connection.fetch_all("SELECT id, name, description, activities, cost FROM destinations")
            destinations = []
            for row in rows:
                id_, name, description, activities_json, cost = row

                activities = json.loads(activities_json)

                destination = Destination(
                    name=name,
                    description=description,
                    activities=activities,
                    cost=cost,
                )
                destination.id = id_
                destinations.append(destination)
            return destinations
        except DatabaseError:
            raise

    def update(self, destination_id, destination: Destination):
        try:
            existent_destination = self.db_connection.fetch_all(
                "SELECT id FROM destinations WHERE id=%s",
                (destination_id,)
            )
            if not existent_destination:
                raise DestinationNotFound
            update = self.db_connection.execute(
                "UPDATE destinations SET name=%s, description=%s,activities=%s, cost=%s WHERE id=%s",
                (destination.name, destination.description, destination.activities, destination.cost, destination_id)
            )
            return update
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
