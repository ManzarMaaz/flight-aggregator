from dataclasses import dataclass


@dataclass
class FlightData:
    """
    A model representing the essential details of a potential flight,
    including target price goals and actual search results.
    """

    city_name: str
    iata_code: str
    target_price: float
    cheapest_price: float = None
    row_id: int = None
    stops: int = 0
