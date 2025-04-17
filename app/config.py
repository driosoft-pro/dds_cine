import os
from pathlib import Path
from typing import Dict, Any

class Config:
    """Clase de configuración para la aplicación."""
    
    # Directorios y archivos
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = BASE_DIR / "app/data"
    LOGS_DIR = BASE_DIR / "app/logs"
    
    # Archivos de datos
    DATA_FILES = {
        'users': "users.json",
        'movies': "movies.json",
        'cinemas': "cinemas.json",
        'food_menu': "food_menu.json",
        'tickets': "tickets.json",
        'reservations': "reservations.json",
        'payments': "payments.json",
        'showtimes': "showtimes.json"
    }
    
    # Configuración de la aplicación
    APP_NAME = "DDS-CINE"
    APP_VERSION = "1.0.0"
    
    # Precios y configuraciones de negocio
    TICKET_PRICES = {
        '2D': {'general': 18000},
        '3D': {'general': 18000, 'preferencial': 25000}
    }
    DISCOUNT_PRICES = {
        'child': 15000,    # Menores de 12 años
        'senior': 16000    # Mayores de 60 años
    }
    
    # Configuración de salas
    CINEMA_CAPACITY = {
        '2D': {'general': 100},
        '3D': {'general': 80, 'preferencial': 20}
    }
    
    # Configuración de reservas
    RESERVATION_DAYS_MIN = 2
    RESERVATION_DAYS_MAX = 7
    CANCELLATION_DAYS_MIN = 1
    CANCELLATION_DAYS_MAX = 2
    
    @classmethod
    def get_data_file_path(cls, key: str) -> Path:
        """Obtiene la ruta completa a un archivo de datos."""
        return cls.DATA_DIR / cls.DATA_FILES.get(key, "")
    
    @classmethod
    def initialize_directories(cls):
        """Crea los directorios necesarios si no existen."""
        os.makedirs(cls.DATA_DIR, exist_ok=True)
        os.makedirs(cls.LOGS_DIR, exist_ok=True)
    
    @classmethod
    def to_dict(cls) -> Dict[str, Any]:
        """Devuelve la configuración como diccionario."""
        return {
            'app_name': cls.APP_NAME,
            'app_version': cls.APP_VERSION,
            'data_dir': str(cls.DATA_DIR),
            'ticket_prices': cls.TICKET_PRICES,
            'cinema_capacity': cls.CINEMA_CAPACITY
        }