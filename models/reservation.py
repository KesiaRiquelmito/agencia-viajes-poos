from datetime import date

class Reservation:
    def __init__(self, user_id: int, package_id: int, reservation_date: date, status: str):
        self.user_id = user_id
        self.package_id = package_id
        self.reservation_date = reservation_date
        self.status = status