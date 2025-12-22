"""Controller managing reservation flows."""

from datetime import date

from tabulate import tabulate

from controllers.package_controller import PackageController
from exceptions.database import DatabaseError
from exceptions.database import ReservationNotFound
from services.reservation_service import ReservationService


class ReservationController:
    """Provide reservation creation and listing CLI actions."""

    def __init__(self, db):
        """Initialize reservation service and package controller."""
        self.reservation_service = ReservationService(db)
        self.package_controller = PackageController(db)

    def _tabulate_reservations(self, reservations):
        """Format reservation data for display."""
        headers = ["ID", "Usuario ID", "Paquete ID", "Fecha de reserva", "Estado"]
        table = []
        for reservation in reservations:
            table.append([
                reservation.id,
                reservation.user_id,
                reservation.package_id,
                reservation.reservation_date,
                reservation.status,
            ])
        return tabulate(table, headers, tablefmt="grid")

    def _input_reservation_data(self):
        """Collect reservation details through CLI prompts."""
        print("---Sistema de reservas---")
        self.package_controller.list_packages()
        package_id = int(input("Escribe el id del paquete turistico a reservar: ").strip())
        reservation_date = date.today()
        status = "active"
        reservation_data = {"package_id": package_id, "reservation_date": reservation_date, "status": status}
        return reservation_data

    def create_reservation(self, user_id):
        """Create a reservation for the provided user."""
        reservation_data = self._input_reservation_data()

        reservation_data["user_id"] = user_id
        try:
            reservation_id = self.reservation_service.create_reservation(reservation_data)
        except DatabaseError:
            print("No se pudo crear la reserva debido a un error en la base de datos")
            return None
        if not reservation_id:
            print("No se pudo crear la reserva (paquete no existe o datos invalidos")
            return None
        print("Reserva creada exitosamente")
        return reservation_id

    def list_reservations_by_user(self, user_id):
        """List reservations tied to a specific user."""
        try:
            reservations = self.reservation_service.get_reservations_by_user(user_id)
            table = self._tabulate_reservations(reservations)
            print(table)
        except ReservationNotFound:
            print("No tienes reservas realizadas")
        except DatabaseError:
            print("No se pudieron obtener las reservas debido a un error en la base de datos")
