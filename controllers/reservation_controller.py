from datetime import date

from controllers.package_controller import PackageController
from exceptions.database import DatabaseError
from services.reservation_service import ReservationService


class ReservationController:
    def __init__(self, db):
        self.reservation_service = ReservationService(db)
        self.package_controller = PackageController(db)

    def _input_reservation_data(self):
        print("---Sistema de reservas---")
        print("Paquetes disponibles para reservas")
        self.package_controller.list_packages()
        package_id = int(input("Escribe el id del paquete turistico a reservar: ").strip())
        reservation_date = date.today()
        status = "active"
        reservation_data = {"package_id": package_id, "reservation_date": reservation_date, "status": status}
        return reservation_data

    def create_reservation(self, user_id):
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
