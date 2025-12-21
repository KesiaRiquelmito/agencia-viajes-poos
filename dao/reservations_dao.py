from exceptions.database import DatabaseError
from models.reservation import Reservation


class ReservationDAO:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def save(self, reservation: Reservation):
        user_id = reservation.user_id
        package_id = reservation.package_id
        reservation_date = reservation.reservation_date
        status = reservation.status

        try:
            cursor = self.db_connection.execute(
                "INSERT INTO reservations (user_id, package_id, reservation_date, status) VALUES (%s, %s, %s, %s)", (user_id, package_id, reservation_date, status),
            )
            return cursor.lastrowid
        except DatabaseError:
            raise