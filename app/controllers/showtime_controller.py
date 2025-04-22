from datetime import datetime, time
from typing import Dict, List, Optional
from models.showtime import Showtime
from core.database import Database

# importando la clase CinemaController para manejar cines
from controllers.cinema_controller import CinemaController

class ShowtimeController:
    """Controlador para manejar operaciones relacionadas con horarios."""
    
    def __init__(self, db: Database):
        self.db = db
        self.showtimes_file = "showtimes.json"
        self.cinema_controller = CinemaController(db)
    
    def load_data(self, filename: str) -> List[Dict]: 
        """Carga datos desde un archivo JSON."""
        return self.db.load_data(filename)
    
    def get_available_seats(self, showtime_id: int, seat_type: str) -> List[str]:
        """Obtiene asientos disponibles para una función y tipo de asiento"""
        showtime = self.get_showtime_by_id(showtime_id)
        if not showtime:
            return []
        
        cinema = self.cinema_controller.get_cinema_by_id(showtime['cinema_id'])
        if not cinema:
            return []
        
        return cinema['available_seats'].get(seat_type, [])
        
    def create_showtime(self, movie_id: int, cinema_id: int,  # Añade cinema_id
                        date: datetime.date, start_time: time, end_time: time, 
                        jornada: str, available_seats: Dict[str, int]) -> Dict:
        """Crea un nuevo horario para una película."""
        showtimes = self.db.load_data(self.showtimes_file)
        showtime_id = self.db.get_next_id("showtimes.json", "showtime_id")
        
        new_showtime = Showtime(
            showtime_id=showtime_id,
            movie_id=movie_id,
            cinema_id=cinema_id,  # Nuevo campo
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
        """Versión con parseo robusto de fechas"""
        showtimes = self.db.load_data(self.showtimes_file)
        for showtime in showtimes:
            if showtime['showtime_id'] == showtime_id:
                # Asegurar que las fechas sean strings
                showtime['date'] = str(showtime.get('date', ''))
                showtime['start_time'] = str(showtime.get('start_time', ''))
                showtime['end_time'] = str(showtime.get('end_time', ''))
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