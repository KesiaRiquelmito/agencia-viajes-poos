from exceptions.database import DatabaseError, AlreadyExistsError
from services.destination_service import DestinationService


class DestinationController:
    def __init__(self, db):
        self.destination_service = DestinationService(db)

    def _validate_data(self, data):
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

    def create_destination(self):
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

        destination_data = {"name": name, "description": description, "activities": activities, "cost": cost}

        if not self._validate_data(destination_data):
            return None

        try:
            destination_id = self.destination_service.create_destination(destination_data)
        except AlreadyExistsError:
            print(f"El destino con nombre '{name}' ya existe.")
            return None
        except DatabaseError:
            print("No se pudo crear el destino debido a un error en la base de datos.")
            return None

        print(f"Destino '{name}' creado exitosamente.")
        return destination_id
