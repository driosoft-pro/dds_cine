from datetime import datetime, time
from typing import Dict, List, Optional
from models.showtime import Showtime
from core.database import Database

class ShowtimeController:
    """Controlador para manejar operaciones relacionadas con horarios."""
    
    def __init__(self, db: Database):
        self.db = db
        self.showtimes_file = "showtimes.json"
    
    def load_data(self, filename: str) -> List[Dict]: 
        """Carga datos desde un archivo JSON."""
        return self.db.load_data(filename)
    
    def create_showtime(self, movie_id: int, date: datetime.date, 
                        start_time: time, end_time: time, jornada: str, 
                        available_seats: Dict[str, int]) -> Dict:
        """Crea un nuevo horario para una película."""
        showtimes = self.db.load_data(self.showtimes_file)
        showtime_id = self.db.get_next_id(self.showtimes_file)
        
        new_showtime = Showtime(
            showtime_id=showtime_id,
            movie_id=movie_id,
            date=date,
            start_time=start_time,
            end_time=end_time,
            jornada=jornada,
            available_seats=available_seats
        )
        
        showtimes.append(new_showtime.to_dict())
        self.db.save_data(self.showtimes_file, showtimes)
        return new_showtime.to_dict()
    
    def get_showtime_by_id(self, showtime_id: int) -> Optional[Dict]:
        """Obtiene un horario por su ID."""
        showtimes = self.db.load_data(self.showtimes_file)
        for showtime in showtimes:
            if showtime['showtime_id'] == showtime_id:
                return showtime
        return None
    
    def get_showtimes_by_movie(self, movie_id: int) -> List[Dict]:
        """Obtiene todos los horarios de una película."""
        showtimes = self.db.load_data(self.showtimes_file)
        return [st for st in showtimes if st['movie_id'] == movie_id]
    
    def update_showtime(self, showtime_id: int, **kwargs) -> Optional[Dict]:
        """Actualiza los datos de un horario."""
        showtimes = self.db.load_data(self.showtimes_file)
        for i, showtime in enumerate(showtimes):
            if showtime['showtime_id'] == showtime_id:
                for key, value in kwargs.items():
                    if key in showtime and key != 'showtime_id':
                        showtimes[i][key] = value
                self.db.save_data(self.showtimes_file, showtimes)
                return showtimes[i]
        return None
    
    def delete_showtime(self, showtime_id: int) -> bool:
        """Elimina un horario."""
        showtimes = self.db.load_data(self.showtimes_file)
        for i, showtime in enumerate(showtimes):
            if showtime['showtime_id'] == showtime_id:
                del showtimes[i]
                self.db.save_data(self.showtimes_file, showtimes)
                return True
        return False
    
    def update_available_seats(self, showtime_id: int, seat_type: str, 
                                quantity: int) -> bool:
        """Actualiza la cantidad de asientos disponibles para un horario."""
        showtimes = self.db.load_data(self.showtimes_file)
        for i, showtime in enumerate(showtimes):
            if showtime['showtime_id'] == showtime_id:
                if seat_type in showtimes[i]['available_seats']:
                    showtimes[i]['available_seats'][seat_type] += quantity
                    self.db.save_data(self.showtimes_file, showtimes)
                    return True
        return False
    
    def list_showtimes(self) -> List[Dict]:
        """Lista todos los horarios."""
        return self.db.load_data(self.showtimes_file)    