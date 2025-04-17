import re
from datetime import datetime
from typing import Optional, Tuple

class ValidationService:
    """Servicio para validar datos de entrada."""
    
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        """Valida que un email tenga formato correcto."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, email):
            return True, "Email válido"
        return False, "El email no tiene un formato válido"
    
    @staticmethod
    def validate_password(password: str) -> Tuple[bool, str]:
        """Valida que una contraseña cumpla con los requisitos."""
        if len(password) < 8:
            return False, "La contraseña debe tener al menos 8 caracteres"
        if not any(c.isupper() for c in password):
            return False, "La contraseña debe contener al menos una mayúscula"
        if not any(c.isdigit() for c in password):
            return False, "La contraseña debe contener al menos un número"
        return True, "Contraseña válida"
    
    @staticmethod
    def validate_date(date_str: str, format: str = "%Y-%m-%d") -> Tuple[bool, str, Optional[datetime]]:
        """Valida que una fecha tenga el formato correcto."""
        try:
            date = datetime.strptime(date_str, format)
            return True, "Fecha válida", date
        except ValueError:
            return False, f"La fecha debe estar en formato {format}", None
    
    @staticmethod
    def validate_age(birth_date: datetime, min_age: int = 0, max_age: int = 120) -> Tuple[bool, str]:
        """Valida que la edad esté dentro de un rango."""
        today = datetime.now()
        age = today.year - birth_date.year - (
            (today.month, today.day) < (birth_date.month, birth_date.day))
        
        if age < min_age:
            return False, f"Debes tener al menos {min_age} años"
        if age > max_age:
            return False, f"La edad máxima permitida es {max_age} años"
        return True, "Edad válida"
    
    @staticmethod
    def validate_identification(identification: str) -> Tuple[bool, str]:
        """Valida que una identificación sea válida (solo números)."""
        if identification.isdigit():
            return True, "Identificación válida"
        return False, "La identificación debe contener solo números"
    
    @staticmethod
    def validate_movie_age_rating(user_age: int, age_rating: str) -> Tuple[bool, str]:
        """Valida que un usuario cumpla con la clasificación de edad de una película."""
        rating_rules = {
            'G': (0, None),
            'PG': (0, None),
            'PG-13': (13, None),
            'R': (17, None),
            'C': (18, None)
        }
        
        min_age, _ = rating_rules.get(age_rating, (0, None))
        
        if min_age is not None and user_age < min_age:
            return False, f"Esta película es clasificación {age_rating}. Edad mínima requerida: {min_age} años"
        return True, "Clasificación de edad válida"