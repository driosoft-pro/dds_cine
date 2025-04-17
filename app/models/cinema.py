from typing import Dict, List

class Cinema:
    """
    Clase que representa una sala de cine.
    
    Attributes:
        cinema_id (int): Identificador único de la sala.
        name (str): Nombre de la sala.
        room_type (str): Tipo de sala (2D, 3D).
        capacity (Dict): Capacidad por tipo de asiento.
        available_seats (Dict): Asientos disponibles por tipo.
    """
    
    def __init__(self, cinema_id: int, name: str, room_type: str, 
                    capacity: Dict[str, int], available_seats: Dict[str, int]):
        self.cinema_id = cinema_id
        self.name = name
        self.room_type = room_type
        self.capacity = capacity
        self.available_seats = available_seats
    
    def to_dict(self) -> dict:
        """Convierte el objeto Cinema a un diccionario."""
        return {
            "cinema_id": self.cinema_id,
            "name": self.name,
            "room_type": self.room_type,
            "capacity": self.capacity,
            "available_seats": self.available_seats
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Cinema':
        """Crea un objeto Cinema desde un diccionario."""
        return cls(
            cinema_id=data["cinema_id"],
            name=data["name"],
            room_type=data["room_type"],
            capacity=data["capacity"],
            available_seats=data["available_seats"]
        )