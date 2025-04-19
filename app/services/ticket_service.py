from datetime import datetime, date

class TicketService:
    """Servicio para calcular precios de tickets con descuentos y promociones."""
    
    BASE_PRICES = {
        '2D': {'general': 18000},
        '3D': {'general': 18000, 'preferencial': 25000}
    }
    
    DISCOUNT_PRICES = {
        'child': 15000,    # Menores de 12 años
        'senior': 16000    # Mayores de 60 años
    }
    
    @staticmethod
    def calculate_ticket_price(room_type: str, seat_type: str, 
                                birth_date: date, showtime: datetime) -> float:
        """
        Calcula el precio de un ticket aplicando descuentos y promociones.
        
        Args:
            room_type: Tipo de sala (2D/3D)
            seat_type: Tipo de asiento (general/preferencial)
            birth_date: Fecha de nacimiento como date
            showtime: Fecha y hora de la función como datetime
            
        Returns:
            Precio calculado del ticket
        """
        # Validaciones de tipo
        if not isinstance(showtime, datetime):
            raise TypeError(f"showtime debe ser datetime, no {type(showtime)}")
        if not isinstance(birth_date, date):
            raise TypeError(f"birth_date debe ser date, no {type(birth_date)}")
        
        try:
            # Determinar si aplica descuento por edad
            age = TicketService.calculate_age(birth_date)
            price = TicketService.get_base_price(room_type, seat_type)
            
            # Aplicar descuentos por edad
            if age < 12:
                price = TicketService.DISCOUNT_PRICES['child']
            elif age >= 60:
                price = TicketService.DISCOUNT_PRICES['senior']
            
            # Aplicar promoción 2x1 en preferencial los martes y jueves por la tarde
            if (seat_type == 'preferencial' and 
                showtime.weekday() in [1, 3] and  # Martes=1, Jueves=3
                12 <= showtime.hour < 18):        # Tarde (12pm-6pm)
                price = price / 2
            
            return price
        except Exception as e:
            raise ValueError(f"Error al calcular precio: {str(e)}")
    
    @staticmethod
    def get_base_price(room_type: str, seat_type: str) -> float:
        """Obtiene el precio base según tipo de sala y asiento."""
        return TicketService.BASE_PRICES.get(room_type, {}).get(seat_type, 0)
    
    @staticmethod
    def calculate_age(birth_date: datetime) -> int:
        """Calcula la edad basada en la fecha de nacimiento."""
        today = datetime.now()
        return today.year - birth_date.year - (
            (today.month, today.day) < (birth_date.month, birth_date.day))
        
    @staticmethod
    def format_cop(amount: float) -> str:
        """Formatea un monto como moneda colombiana con validación."""
        try:
            # Asegurar que es numérico
            amount_float = float(amount)
            # Formatear con separador de miles y sin decimales
            return f"${amount_float:,.0f}".replace(",", ".")
        except (ValueError, TypeError):
            return f"${amount}"  # Fallback si no se puede formatear