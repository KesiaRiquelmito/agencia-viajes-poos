from services.reservation_service import ReservationService


class ReservationController:
    def __init__(self,db):
        self.reservation_service = ReservationService(db)

    def _input_reservation_data(self):
        pass

    def create_reservation(self, param):
        pass