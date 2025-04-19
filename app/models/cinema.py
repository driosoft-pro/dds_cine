from typing import Dict, List
class Cinema:
    """
    Clase que representa una sala de cine.
    
    Attributes:
        cinema_id (int): Identificador único de la sala.
        name (str): Nombre de la sala.
        room_type (str): Tipo de sala (2D, 3D).
        capacity (Dict): Capacidad por tipo de asiento.
        seats (List): Asientos disponibles por tipo.
    """    
    def __init__(self, cinema_id: int, name: str, room_type: str, 
                    capacity: Dict[str, int], seats: Dict[str, List[str]]):
        self.cinema_id = cinema_id
        self.name = name
        self.room_type = room_type
        self.capacity = capacity
        self.seats = seats  
        self.available_seats = self._init_available_seats()

    def _init_available_seats(self) -> Dict[str, List[str]]:
        """Inicializa todos los asientos como disponibles"""
        return {seat_type: seats.copy() for seat_type, seats in self.seats.items()}

    def to_dict(self) -> dict:
        return {
            "cinema_id": self.cinema_id,
            "name": self.name,
            "room_type": self.room_type,
            "capacity": self.capacity,
            "seats": self.seats,
            "available_seats": self.available_seats
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Cinema':
        return cls(
            cinema_id=data["cinema_id"],
            name=data["name"],
            room_type=data["room_type"],
            capacity=data["capacity"],
            seats=data["seats"]
        )