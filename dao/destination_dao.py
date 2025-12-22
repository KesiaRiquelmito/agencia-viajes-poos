"""Persistence helpers for destinations."""

import json

from exceptions.database import DatabaseError, AlreadyExistsError, DestinationNotFound, DeletionNotCompleted
from models.destination import Destination


class DestinationDAO:
    """Provide CRUD operations for Destination entities."""

    def __init__(self, db_connection):
        """Store DB connection layer."""
        self.db_connection = db_connection

    def get_all(self):
        """Return every destination row as model instances."""
        try:
            rows = self.db_connection.fetch_all("SELECT id, name, description, activities, cost FROM destinations")
            destinations = []
            for row in rows:
                id_, name, description, activities_json, cost = row

                activities = json.loads(activities_json)
                if isinstance(activities, str):
                    try:
                        activities = json.loads(activities)
                    except json.JSONDecodeError:
                        activities = [activities]

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
        """Update the target destination with new details."""
        try:
            existent_destination = self.db_connection.fetch_all(
                "SELECT id FROM destinations WHERE id=%s",
                (destination_id,)
            )
            if not existent_destination:
                raise DestinationNotFound
            update = self.db_connection.execute(
                "UPDATE destinations SET name=%s, description=%s,activities=%s, cost=%s WHERE id=%s",
                (destination.name, destination.description, json.dumps(destination.activities), destination.cost, destination_id)
            )
            return update
        except DatabaseError:
            raise

    def delete(self, destination_id):
        """Delete destination by id raising domain errors if needed."""
        try:
            exists = self.db_connection.fetch_all(
                "SELECT id FROM destinations WHERE id = %s", (destination_id,)
            )
            if not exists:
                raise DestinationNotFound
            deleted = self.db_connection.execute(
                "DELETE FROM destinations WHERE id = %s",
                (destination_id,)
            )
            if not deleted:
                raise DeletionNotCompleted
            return deleted
        except DatabaseError:
            raise

    def save(self, destination: Destination):
        """Persist a new destination and return its id."""
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
