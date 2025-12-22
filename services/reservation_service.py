"""Reservation service bridging controllers and DAOs."""

from dao.reservations_dao import ReservationDAO
from models.reservation import Reservation


class ReservationService:
    """Encapsulate reservation-specific data manipulation."""

    def __init__(self, db):
        """Keep DB reference and build DAO."""
        self.db = db
        self.reservation_dao = ReservationDAO(db)

    def get_reservations_by_user(self, user_id):
        """Fetch reservations belonging to a user."""
        return self.reservation_dao.get_reservations_by_user(user_id)

    def create_reservation(self, reservation_data):
        """Persist a reservation record."""
        reservation = Reservation(
            reservation_data["user_id"],
            reservation_data["package_id"],
            reservation_data["reservation_date"],
            reservation_data["status"]
        )
        return self.reservation_dao.save(reservation)
