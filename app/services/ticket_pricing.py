from datetime import datetime
from typing import Dict, Literal

def calculate_ticket_price(
    ticket_type: Literal['general', 'preferential', 'child', 'senior'],
    seat_type: Literal['standard', 'preferential'],
    showtime: Dict[str, str]
) -> float:
    """Calcula el precio del ticket basado en tipo, asiento y descuentos"""
    base_prices = {
        'general': {
            'standard': 18000,
            'preferential': 25000
        },
        'preferential': 25000,
        'child': 15000,
        'senior': 16000
    }

    # Precio base según tipo
    if ticket_type in ['child', 'senior']:
        price = base_prices[ticket_type]
    else:
        price = base_prices[ticket_type][seat_type]

    # Descuento 2x1 en asientos preferenciales martes/jueves
    showtime_date = datetime.strptime(f"{showtime['date']} {showtime['time']}", "%Y-%m-%d %H:%M")
    if (showtime_date.weekday() in [1, 3] and  # martes=1, jueves=3
        seat_type == 'preferential' and
        ticket_type != 'child'):
        price /= 2

    return price