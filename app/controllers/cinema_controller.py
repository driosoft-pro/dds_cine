from typing import Dict, List, Optional
from datetime import datetime, timedelta
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
        cinema_id = self.db.get_next_id("cinemas.json", "cinema_id")
        
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
    
    def get_available_all_seats(self, cinema_id: int) -> Dict[str, List[str]]:
        """Obtiene asientos disponibles para una sala de cine."""
        cinema = self.get_cinema_by_id(cinema_id)
        if cinema:
            return cinema['available_seats']
        return {}
    
    def get_available_seats_by_type(self, cinema_id: int, seat_type: str) -> List[str]:
        """Obtiene asientos disponibles para un tipo específico."""
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
    
    def reserve_seat(self, cinema_id: int, seat_type: str, seat_number: str) -> bool:
        """Reserva un asiento con manejo transaccional."""
        cinemas = self.db.load_data(self.cinemas_file)
        for i, cinema in enumerate(cinemas):
            if cinema['cinema_id'] == cinema_id:
                if seat_type in cinema['available_seats']:
                    if seat_number in cinema['available_seats'][seat_type]:
                        # Remover el asiento de disponibles
                        cinemas[i]['available_seats'][seat_type].remove(seat_number)
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
    
    def temp_reserve_seat(self, cinema_id: int, seat_type: str, seat_number: str) -> bool:
        """Reserva temporalmente un asiento por 10 minutos."""
        cinemas = self.db.load_data(self.cinemas_file)
        
        for i, cinema in enumerate(cinemas):
            if cinema['cinema_id'] == cinema_id:
                if seat_type in cinema['available_seats']:
                    if seat_number in cinema['available_seats'][seat_type]:
                        # Remover de disponibles
                        cinemas[i]['available_seats'][seat_type].remove(seat_number)
                        
                        # Agregar a reservas temporales
                        if 'temp_reservations' not in cinemas[i]:
                            cinemas[i]['temp_reservations'] = {}
                        if seat_type not in cinemas[i]['temp_reservations']:
                            cinemas[i]['temp_reservations'][seat_type] = []
                            
                        cinemas[i]['temp_reservations'][seat_type].append({
                            'seat_number': seat_number,
                            'expires_at': (datetime.now() + timedelta(minutes=10)).isoformat()
                        })
                        
                        self.db.save_data(self.cinemas_file, cinemas)
                        return True
        return False
    
    def confirm_reservation(self, cinema_id: int, seat_type: str, seat_number: str) -> bool:
        """Confirma una reserva temporal como permanente."""
        cinemas = self.db.load_data(self.cinemas_file)
        
        for i, cinema in enumerate(cinemas):
            if cinema['cinema_id'] == cinema_id:
                # Verificar si existe en reservas temporales
                if 'temp_reservations' in cinema and seat_type in cinema['temp_reservations']:
                    # Remover de temporales
                    cinemas[i]['temp_reservations'][seat_type] = [
                        seat for seat in cinema['temp_reservations'][seat_type]
                        if seat['seat_number'] != seat_number
                    ]
                    
                    # Agregar a reservas confirmadas
                    if 'confirmed_seats' not in cinemas[i]:
                        cinemas[i]['confirmed_seats'] = {}
                    if seat_type not in cinemas[i]['confirmed_seats']:
                        cinemas[i]['confirmed_seats'][seat_type] = []
                        
                    cinemas[i]['confirmed_seats'][seat_type].append(seat_number)
                    self.db.save_data(self.cinemas_file, cinemas)
                    return True
        return False 
    
    def release_seat(self, cinema_id: int, seat_type: str, seat_number: str) -> bool:
        """Libera un asiento reservado (temporal o confirmado)."""
        try:
            cinemas = self.db.load_data(self.cinemas_file)
            seat_freed = False
            
            for i, cinema in enumerate(cinemas):
                if cinema['cinema_id'] == cinema_id:
                    # Liberar de reservas temporales
                    if 'temp_reservations' in cinema and seat_type in cinema['temp_reservations']:
                        before = len(cinema['temp_reservations'][seat_type])
                        cinemas[i]['temp_reservations'][seat_type] = [
                            r for r in cinema['temp_reservations'][seat_type]
                            if r['seat_number'] != seat_number
                        ]
                        if len(cinemas[i]['temp_reservations'][seat_type]) != before:
                            seat_freed = True
                    
                    # Liberar de reservas confirmadas
                    if 'confirmed_seats' in cinema and seat_type in cinema['confirmed_seats']:
                        before = len(cinema['confirmed_seats'][seat_type])
                        cinemas[i]['confirmed_seats'][seat_type] = [
                            s for s in cinema['confirmed_seats'][seat_type]
                            if s != seat_number
                        ]
                        if len(cinemas[i]['confirmed_seats'][seat_type]) != before:
                            seat_freed = True
                    
                    # Agregar a disponibles si se liberó
                    if seat_freed and seat_type in cinema['seats']:
                        if seat_number not in cinemas[i]['available_seats'].get(seat_type, []):
                            cinemas[i]['available_seats'].setdefault(seat_type, []).append(seat_number)
                            self.db.save_data(self.cinemas_file, cinemas)
                            return True
            
            return seat_freed
        except Exception as e:
            print(f"Error crítico al liberar asiento: {str(e)}")
            return False