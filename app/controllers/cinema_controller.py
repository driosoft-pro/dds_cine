from typing import Dict, List, Optional
from models.cinema import Cinema
from core.database import Database

class CinemaController:
    """Controlador para manejar operaciones relacionadas con las salas de cine."""
    
    def __init__(self, db: Database):
        self.db = db
        self.cinemas_file = "cinemas.json"
    
    def load_data(self, filename: str) -> List[Dict]:
        """Carga datos desde un archivo JSON."""
        return self.db.load_data(filename)
    
    def create_cinema(self, name: str, room_type: str, 
                        capacity: Dict[str, int], seats: Dict[str, List[str]]) -> Dict:
        """Crea una nueva sala de cine con asientos definidos"""
        cinemas = self.db.load_data(self.cinemas_file)
        cinema_id = self.db.get_next_id(self.cinemas_file)
        
        new_cinema = Cinema(
            cinema_id=cinema_id,
            name=name,
            room_type=room_type,
            capacity=capacity,
            seats=seats
        )
        
        cinemas.append(new_cinema.to_dict())
        self.db.save_data(self.cinemas_file, cinemas)
        return new_cinema.to_dict()

    def get_available_seats_by_type(self, cinema_id: int, seat_type: str) -> List[str]:
        """Obtiene asientos disponibles para un tipo específico"""
        cinema = self.get_cinema_by_id(cinema_id)
        if cinema and seat_type in cinema['available_seats']:
            return cinema['available_seats'][seat_type]
        return []

    def reserve_seat(self, cinema_id: int, seat_type: str, seat_number: str) -> bool:
        """Reserva un asiento específico"""
        cinemas = self.db.load_data(self.cinemas_file)
        for i, cinema in enumerate(cinemas):
            if cinema['cinema_id'] == cinema_id:
                if seat_type in cinema['available_seats']:
                    if seat_number in cinema['available_seats'][seat_type]:
                        cinemas[i]['available_seats'][seat_type].remove(seat_number)
                        self.db.save_data(self.cinemas_file, cinemas)
                        return True
        return False
    
    def get_cinema_by_id(self, cinema_id: int) -> Optional[Dict]:
        """Obtiene una sala de cine por su ID."""
        cinemas = self.db.load_data(self.cinemas_file)
        for cinema in cinemas:
            if cinema['cinema_id'] == cinema_id:
                return cinema
        return None
    
    def update_cinema(self, cinema_id: int, **kwargs) -> Optional[Dict]:
        """Actualiza los datos de una sala de cine."""
        cinemas = self.db.load_data(self.cinemas_file)
        for i, cinema in enumerate(cinemas):
            if cinema['cinema_id'] == cinema_id:
                for key, value in kwargs.items():
                    if key in cinema and key != 'cinema_id':
                        cinemas[i][key] = value
                self.db.save_data(self.cinemas_file, cinemas)
                return cinemas[i]
        return None
    
    def list_cinemas(self) -> List[Dict]:
        """Lista todas las salas de cine."""
        return self.db.load_data(self.cinemas_file)
    
    def get_available_seats(self, cinema_id: int) -> Dict[str, int]:
        """Obtiene los asientos disponibles por tipo para una sala."""
        cinema = self.get_cinema_by_id(cinema_id)
        if cinema:
            return cinema['available_seats']
        return {}
    
    def update_available_seats(self, cinema_id: int, seat_type: str, 
                                quantity: int) -> bool:
        """Actualiza la cantidad de asientos disponibles para una sala."""
        cinemas = self.db.load_data(self.cinemas_file)
        for i, cinema in enumerate(cinemas):
            if cinema['cinema_id'] == cinema_id:
                if seat_type in cinemas[i]['available_seats']:
                    cinemas[i]['available_seats'][seat_type] += quantity
                    self.db.save_data(self.cinemas_file, cinemas)
                    return True
        return False
    
    def delete_cinema(self, cinema_id: int) -> bool:
        """Elimina una sala de cine."""
        cinemas = self.db.load_data(self.cinemas_file)
        for i, cinema in enumerate(cinemas):
            if cinema['cinema_id'] == cinema_id:
                cinemas.pop(i)
                self.db.save_data(self.cinemas_file, cinemas)
                return True
        return False