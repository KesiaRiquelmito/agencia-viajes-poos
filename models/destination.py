"""Destination domain model."""


class Destination:
    """Represent a travel destination."""

    def __init__(self, name: str, description: str, activities: dict, cost: float):
        self.name = name
        self.description = description
        self.activities = activities
        self.cost = cost
