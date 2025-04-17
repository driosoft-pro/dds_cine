from datetime import datetime

class TicketPricingService:
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
    def calculate_ticket_price(room_type: str, seat_type: str, birth_date: datetime, 
                                showtime: datetime) -> float:
        """Calcula el precio de un ticket aplicando descuentos y promociones."""
        # Determinar si aplica descuento por edad
        age = TicketPricingService.calculate_age(birth_date)
        price = TicketPricingService.get_base_price(room_type, seat_type)
        
        # Aplicar descuentos por edad
        if age < 12:
            price = TicketPricingService.DISCOUNT_PRICES['child']
        elif age >= 60:
            price = TicketPricingService.DISCOUNT_PRICES['senior']
        
        # Aplicar promoción 2x1 en preferencial los martes y jueves por la tarde
        if (seat_type == 'preferencial' and 
            showtime.weekday() in [1, 3] and  # Martes=1, Jueves=3
            12 <= showtime.hour < 18):        # Tarde
            price = price / 2
        
        return price
    
    @staticmethod
    def get_base_price(room_type: str, seat_type: str) -> float:
        """Obtiene el precio base según tipo de sala y asiento."""
        return TicketPricingService.BASE_PRICES.get(room_type, {}).get(seat_type, 0)
    
    @staticmethod
    def calculate_age(birth_date: datetime) -> int:
        """Calcula la edad basada en la fecha de nacimiento."""
        today = datetime.now()
        return today.year - birth_date.year - (
            (today.month, today.day) < (birth_date.month, birth_date.day))