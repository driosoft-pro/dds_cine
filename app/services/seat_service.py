from typing import Dict, List
from datetime import datetime, timedelta
from core.database import Database

class SeatService:
    """Servicio completo para gestión de asientos con reservas temporales."""
    
    def __init__(self, db: Database):
        self.db = db
        self.cinemas_file = "cinemas.json"
    
    def get_available_seats(self, cinema_id: int, showtime_id: int) -> Dict[str, List[str]]:
        """Obtiene asientos disponibles reales (excluyendo reservados)."""
        # Primero limpiar reservas expiradas
        self.clean_expired_reservations()
        
        cinema = self._get_cinema_by_id(cinema_id)
        if not cinema:
            return {}
        
        available = {}
        for seat_type in cinema.get('seats', {}):
            # Obtener todos los asientos del tipo
            all_seats = cinema['seats'].get(seat_type, [])
            
            # Obtener asientos ocupados (reservas confirmadas + temporales activas)
            reserved = set()
            
            # Asientos en reservas confirmadas
            if 'confirmed_seats' in cinema and seat_type in cinema['confirmed_seats']:
                reserved.update(cinema['confirmed_seats'][seat_type])
            
            # Asientos en reservas temporales no expiradas
            if 'temp_reservations' in cinema and seat_type in cinema['temp_reservations']:
                reserved.update(
                    r['seat_number'] for r in cinema['temp_reservations'][seat_type]
                )
            
            # Calcular disponibles
            available[seat_type] = [seat for seat in all_seats if seat not in reserved]
        
        return available
    
    def temp_reserve_seat(self, cinema_id: int, seat_type: str, seat_number: str) -> bool:
        """Reserva temporalmente un asiento por 10 minutos."""
        cinemas = self.db.load_data(self.cinemas_file)
        
        for i, cinema in enumerate(cinemas):
            if cinema['cinema_id'] == cinema_id:
                if seat_type in cinema.get('seats', {}):
                    # Verificar que el asiento existe y está disponible
                    if seat_number in cinema['seats'][seat_type]:
                        # Verificar que no está ya reservado
                        reserved = False
                        
                        # En reservas confirmadas
                        if 'confirmed_seats' in cinema and seat_type in cinema['confirmed_seats']:
                            if seat_number in cinema['confirmed_seats'][seat_type]:
                                reserved = True
                        
                        # En reservas temporales activas
                        if not reserved and 'temp_reservations' in cinema and seat_type in cinema['temp_reservations']:
                            for res in cinema['temp_reservations'][seat_type]:
                                if res['seat_number'] == seat_number:
                                    reserved = True
                                    break
                        
                        if not reserved:
                            # Crear estructura si no existe
                            if 'temp_reservations' not in cinemas[i]:
                                cinemas[i]['temp_reservations'] = {}
                            if seat_type not in cinemas[i]['temp_reservations']:
                                cinemas[i]['temp_reservations'][seat_type] = []
                            
                            # Agregar reserva temporal
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
                # Verificar que existe en reservas temporales
                if 'temp_reservations' in cinema and seat_type in cinema['temp_reservations']:
                    # Buscar y remover la reserva temporal
                    temp_reservations = [
                        r for r in cinema['temp_reservations'][seat_type]
                        if r['seat_number'] != seat_number
                    ]
                    
                    # Si se encontró y removió la reserva
                    if len(temp_reservations) != len(cinema['temp_reservations'][seat_type]):
                        cinemas[i]['temp_reservations'][seat_type] = temp_reservations
                        
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
        """Libera un asiento reservado (temporal o permanente)."""
        cinemas = self.db.load_data(self.cinemas_file)
        
        for i, cinema in enumerate(cinemas):
            if cinema['cinema_id'] == cinema_id:
                changed = False
                
                # Liberar de reservas temporales
                if 'temp_reservations' in cinema and seat_type in cinema['temp_reservations']:
                    original_count = len(cinema['temp_reservations'][seat_type])
                    cinemas[i]['temp_reservations'][seat_type] = [
                        r for r in cinema['temp_reservations'][seat_type]
                        if r['seat_number'] != seat_number
                    ]
                    if len(cinemas[i]['temp_reservations'][seat_type]) != original_count:
                        changed = True
                
                # Liberar de reservas confirmadas
                if 'confirmed_seats' in cinema and seat_type in cinema['confirmed_seats']:
                    original_count = len(cinema['confirmed_seats'][seat_type])
                    cinemas[i]['confirmed_seats'][seat_type] = [
                        s for s in cinema['confirmed_seats'][seat_type]
                        if s != seat_number
                    ]
                    if len(cinemas[i]['confirmed_seats'][seat_type]) != original_count:
                        changed = True
                
                if changed:
                    self.db.save_data(self.cinemas_file, cinemas)
                    return True
        return False
    
    def clean_expired_reservations(self):
        """Limpia automáticamente las reservas temporales expiradas."""
        cinemas = self.db.load_data(self.cinemas_file)
        changed = False
        
        for i, cinema in enumerate(cinemas):
            if 'temp_reservations' in cinema:
                for seat_type in list(cinema['temp_reservations'].keys()):
                    valid_reservations = []
                    
                    for reservation in cinema['temp_reservations'][seat_type]:
                        try:
                            expires_at = datetime.fromisoformat(reservation['expires_at'])
                            if datetime.now() < expires_at:
                                valid_reservations.append(reservation)
                            else:
                                changed = True  # Reserva expirada
                        except ValueError:
                            continue  # Fecha inválida, la removemos
                    
                    # Actualizar solo si hubo cambios
                    if len(valid_reservations) != len(cinema['temp_reservations'][seat_type]):
                        cinemas[i]['temp_reservations'][seat_type] = valid_reservations
                        changed = True
        
        if changed:
            self.db.save_data(self.cinemas_file, cinemas)
    
    def _get_cinema_by_id(self, cinema_id: int) -> Dict:
        """Helper para obtener cine por ID."""
        cinemas = self.db.load_data(self.cinemas_file)
        for cinema in cinemas:
            if cinema['cinema_id'] == cinema_id:
                return cinema
        return None