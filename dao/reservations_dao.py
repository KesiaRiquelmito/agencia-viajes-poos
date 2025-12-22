"""Reservation DAO for CRUD operations."""

from exceptions.database import DatabaseError, ReservationNotFound, AlreadyExistsError
from models.reservation import Reservation


class ReservationDAO:
    """Encapsulate persistence logic for reservations."""

    def __init__(self, db_connection):
        """Store DB connection."""
        self.db_connection = db_connection

    def get_reservations_by_user(self, user_id: int):
        """List reservations for a user id."""
        try:
            rows = self.db_connection.fetch_all(
                "SELECT id, user_id, package_id, reservation_date, status FROM reservations WHERE user_id = %s",
                (user_id,),
            )
            if not rows:
                raise ReservationNotFound
            reservations = []
            for row in rows:
                reservation = Reservation(
                    user_id=row[1],
                    package_id=row[2],
                    reservation_date=row[3],
                    status=row[4],
                )
                reservation.id = row[0]
                reservations.append(reservation)
            return reservations
        except DatabaseError:
            raise

    def save(self, reservation: Reservation):
        """Insert a reservation record and return its id."""
        user_id = reservation.user_id
        package_id = reservation.package_id
        reservation_date = reservation.reservation_date
        status = reservation.status

        try:
            exists = self.db_connection.fetch_all(
                "SELECT id FROM reservations WHERE user_id = %s AND package_id = %s",
                (user_id, package_id),
            )
            if exists:
                raise AlreadyExistsError
            cursor = self.db_connection.execute(
                "INSERT INTO reservations (user_id, package_id, reservation_date, status) VALUES (%s, %s, %s, %s)",
                (user_id, package_id, reservation_date, status),
            )
            return cursor.lastrowid
        except DatabaseError:
            raise
