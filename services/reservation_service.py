from dao.reservations_dao import ReservationDAO
from models.reservation import Reservation


class ReservationService:
    def __init__(self, db):
        self.db = db
        self.reservation_dao = ReservationDAO

    def get_reservations_by_user(self, user_id):
        return self.reservation_dao.get_reservations_by_user(user_id)

    def create_reservation(self, reservation_data):
        reservation = Reservation(
            reservation_data["user_id"],
            reservation_data["package_id"],
            reservation_data["reservation_date"],
            reservation_data["status"]
        )
        return self.reservation_dao.save(reservation)
