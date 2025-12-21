from exceptions.database import ReservationNotFound
from services.reservation_service import ReservationService
from tabulate import tabulate


class ReservationController:
    def __init__(self, db):
        self.reservation_service = ReservationService(db)

    def _tabulate_reservations(self, reservations):
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
        pass

    def create_reservation(self, param):
        pass

    def list_reservations_by_user(self, user_id):
        try:
            reservations = self.reservation_service.get_reservations_by_user(user_id)
            table = self._tabulate_reservations(reservations)
            print(table)
        except ReservationNotFound:
            print("No tienes reservas realizadas")
        except Exception as e:
            print(f"Error al obtener las reservas: {str(e)}")
