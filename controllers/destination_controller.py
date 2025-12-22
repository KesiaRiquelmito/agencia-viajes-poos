"""Controller layer for destination CLI operations."""

import json

from exceptions.database import DatabaseError, AlreadyExistsError, DestinationNotFound, DeletionNotCompleted
from services.destination_service import DestinationService
from tabulate import tabulate


class DestinationController:
    """Handle user interactions related to destinations."""

    def __init__(self, db):
        """Initialize the controller with its backing service."""
        self.destination_service = DestinationService(db)

    def _validate_data(self, data):
        """Validate CLI input for a destination before persisting it."""
        if not data["name"] or not data["description"]:
            print("Nombre y descripción son obligatorios.")
            return False
        if not data["activities"]:
            print("Debe ingresar al menos una actividad.")
            return False
        if data["cost"] is None or data["cost"] < 0:
            print("El costo debe ser un número >= 0.")
            return False
        return True

    def _tabulate_data(self, data):
        """Format a list of destinations into a printable table string."""
        headers = ["ID", "Nombre", "Descripción", "Actividades", "Costo"]
        table = []
        for dest in data:
            table.append([
                dest.id,
                dest.name,
                dest.description,
                ", ".join(dest.activities),
                dest.cost
            ])
        return tabulate(table, headers, tablefmt="grid")

    def _input_destination_data(self):
        """Collect destination attributes from user input."""
        name = input("Ingrese el nombre del destino: ").strip()
        description = input("Ingrese la descripción del destino: ").strip()

        raw_activities = input("Ingrese separadas por comas las actividades disponibles: ")
        activities = [a.strip() for a in raw_activities.split(",") if a.strip()]

        cost_raw = input("Ingrese el costo del destino: ").strip()
        try:
            cost = float(cost_raw)
        except ValueError:
            print("El costo debe ser un número.")
            return None

        destination_data = {"name": name, "description": description, "activities": json.dumps(activities),
                            "cost": cost}

        if not self._validate_data(destination_data):
            return None
        return destination_data

    def update_destination(self):
        """Interactive flow to update a destination record."""
        self.list_destinations()
        target = int(input("Ingrese el ID del destino que desea actualizar: ").strip())
        destination_data = self._input_destination_data()

        try:
            updated = self.destination_service.update_destination(target, destination_data)
        except DestinationNotFound:
            print("El destino a actualizar no existe en la base de datos.")
            return None
        except DatabaseError:
            print("No se pudo actualizar el destino debido a un error en la base de datos.")
            return None

        print(f"Destino actualizado exitosamente.")
        return updated

    def create_destination(self):
        """Interactive flow to create a new destination."""
        destination_data = self._input_destination_data()

        try:
            destination_id = self.destination_service.create_destination(destination_data)
        except AlreadyExistsError:
            print(f"El destino ya existe.")
            return None
        except DatabaseError:
            print("No se pudo crear el destino debido a un error en la base de datos.")
            return None

        print(f"Destino creado exitosamente.")
        return destination_id

    def delete_destination(self):
        """Interactive flow to delete an existing destination."""
        self.list_destinations()
        destination_id = int(input("Ingrese el ID del destino que desea eliminar").strip())
        try:
            deleted = self.destination_service.delete_destination(destination_id)
        except DestinationNotFound:
            print("No se encontró el destino ingresado")
            return None
        except DeletionNotCompleted:
            print("No se pudo eliminar el destino")
            return None
        except DatabaseError:
            print("No se pudo eliminar el destino debido a un error en la base de datos.")
            return None
        print("Destino eliminado.")
        return deleted

    def list_destinations(self):
        """Print all destinations available in the system."""
        try:
            destinations = self.destination_service.get_all_destinations()
        except DatabaseError:
            print("No se pudieron obtener los destinos debido a un error en la base de datos.")
            return

        if not destinations:
            print("No hay destinos disponibles.")
            return

        table = self._tabulate_data(destinations)
        print(table)
