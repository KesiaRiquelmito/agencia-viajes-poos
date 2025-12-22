"""Controller for tourist package orchestration."""

from datetime import datetime

from tabulate import tabulate

from exceptions.database import AlreadyExistsError, DatabaseError
from services.destination_service import DestinationService
from services.package_service import PackageService


class PackageController:
    """Manage package creation, validation, and listing flows."""

    def __init__(self, db):
        """Initialize dependent services for package operations."""
        self.package_service = PackageService(db)
        self.destination_service = DestinationService(db)

    def _validate_data(self, data):
        """Ensure collected package data has mandatory values."""
        if not data["name"]:
            print("Error: el nombre es obligatorio para crear un paquete turistico")
            return False
        if not data["start_date"] or not data["end_date"]:
            print("Error: la fechas son obligatorias para crear un paquete turistico")
            return False
        return True

    def _tabulate_data(self, data):
        """Render packages into a table for CLI output."""
        headers = ["ID", "Nombre", "Fecha inicio", "Fecha termino", "Destinos", "Precio total"]
        table = []
        for package in data:
            destinations = package["destinations"]
            destinations_text = ", ".join(destinations) if destinations else "(Sin destinos)"

            table.append([
                package["id"],
                package["name"],
                package["start_date"],
                package["end_date"],
                destinations_text,
                package["total_price"],
            ])
        return tabulate(table, headers, tablefmt="grid")

    def _input_package_data(self):
        """Collect package fields from the CLI and compute totals."""
        name = input("Ingrese el nombre del paquete turistico: ").strip()
        start_date = datetime.strptime(input("Fecha inicio (dd-mm-YYYY): "), "%d-%m-%Y").date()
        end_date = datetime.strptime(input("Ingrese la fecha de termino (dd-mm-YYYY): "), "%d-%m-%Y").date()
        destinations = self.destination_service.get_all_destinations()
        if not destinations:
            print("No hay destinos creados. Cree destinos antes de crear un paquete turistico")
            return None

        print("Destinos disponibles:")
        for destination in destinations:
            print(f"{destination.id}: {destination.name}- ${destination.cost}")

        raw_ids = input("Ingrese los id de los destinos a agregar separados por comas: ").strip()
        ids = [int(x.strip()) for x in raw_ids.split(",")]
        selected = [destination for destination in destinations if destination.id in ids]

        if not selected:
            print("No seleccionaste destinos validos")
            return None

        total_price = sum(destination.cost for destination in selected)
        destination_ids = [destination.id for destination in selected]

        package_data = {"name": name, "start_date": start_date, "end_date": end_date,
                        "destinations": destination_ids, "total_price": total_price}

        if not self._validate_data(package_data):
            return None
        return package_data

    def create_package(self):
        """Prompt for package data and persist it via the service."""
        package_data = self._input_package_data()

        try:
            package_id = self.package_service.create_package(package_data)
        except AlreadyExistsError:
            print("El paquete ya existe")
            return None
        except DatabaseError:
            print("No se pudo crear el paquete debido a un error en la base de datos")
            return None
        print("Paquete creado exitosamente")
        return package_id

    def list_packages(self):
        """List package summaries ready for reservation."""
        try:
            print("---Paquetes disponibles para reservas---")
            packages = self.package_service.get_packages_summary()
        except DatabaseError:
            print("No se pudieron obtener los paquetes turisticos debido a un error en la base de datos")
            return
        if not packages:
            print("No hay paquetes turisticos disponibles")
            return
        table = self._tabulate_data(packages)
        print(table)
