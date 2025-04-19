from datetime import datetime

# impiortando las librerías necesarias
from typing import List, Dict

# importando el servicio de precios de entradas
from services.ticket_pricing_service import TicketPricingService

class DiscountService:
    """Servicio para aplicar descuentos y promociones."""
    
    @staticmethod
    def apply_2x1_promotion(showtime: datetime, ticket_type: str, price: float) -> float:
        """Aplica la promoción 2x1 para asientos preferenciales los martes y jueves por la tarde."""
        if (ticket_type == 'preferencial' and 
            showtime.weekday() in [1, 3] and  # Martes=1, Jueves=3
            12 <= showtime.hour < 18):        # Tarde
            return price / 2
        return price
    
    @staticmethod
    def apply_age_discount(birth_date: datetime, room_type: str, seat_type: str) -> float:
        """Aplica descuentos por edad (niños y adultos mayores)."""
        age = DiscountService.calculate_age(birth_date)
        base_price = TicketPricingService.get_base_price(room_type, seat_type)
        
        if age < 12:
            return TicketPricingService.DISCOUNT_PRICES['child']
        elif age >= 60:
            return TicketPricingService.DISCOUNT_PRICES['senior']
        return base_price
    
    @staticmethod
    def calculate_age(birth_date: datetime) -> int:
        """Calcula la edad basada en la fecha de nacimiento."""
        today = datetime.now()
        return today.year - birth_date.year - (
            (today.month, today.day) < (birth_date.month, birth_date.day))
    
    @staticmethod
    def apply_group_discount(quantity: int, total: float) -> float:
        """Aplica descuento por grupo (5% para más de 5 personas)."""
        if quantity >= 5:
            return total * 0.95
        return total
    
    @staticmethod
    def apply_food_combo_discount(ticket_quantity: int, food_items: List[Dict]) -> float:
        """Aplica descuento por combos de comida con entradas."""
        combo_count = sum(1 for item in food_items if 'combo' in item['category'].lower())
        if combo_count >= ticket_quantity:
            return sum(item['price'] for item in food_items) * 0.9  # 10% de descuento
        return sum(item['price'] for item in food_items)