from datetime import date


class TouristPackage:
    def __init__(self, name: str, start_date: date, end_date: date,
                 total_price: int):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.total_price = total_price
