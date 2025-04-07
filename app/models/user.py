from datetime import datetime
from typing import Literal
import re

class User:
    """Clase base que representa un usuario del sistema."""
    
    def __init__(self, user_id: int, username: str, identification: str, name: str, 
                    email: str, birth_date: str, password: str, 
                    status: Literal['active', 'inactive'] = 'active'):
        """
        Inicializa un usuario con los datos básicos.
        """
        self._user_id = user_id  # ID autoincremental del sistema
        self._username = username  # Nombre de usuario para login
        self._identification = identification  # Identificación personal (cédula, etc.)
        self._name = name  # Nombre completo
        self._email = email
        self._birth_date = birth_date
        self._password = password
        self._status = status
    
    @property
    def user_id(self) -> int:
        return self._user_id
    
    @property
    def username(self) -> str:
        return self._username
    
    @property
    def identification(self) -> str:
        return self._identification
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def email(self) -> str:
        return self._email
    
    @property
    def birth_date(self) -> str:
        return self._birth_date
    
    @property
    def password(self) -> str:
        return self._password
    
    @property
    def status(self) -> str:
        return self._status
    
    def get_age(self) -> int:
        """Calcula la edad del usuario basado en su fecha de nacimiento."""
        birth_date = datetime.strptime(self._birth_date, "%Y-%m-%d")
        today = datetime.now()
        age = today.year - birth_date.year
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1
        return age
    
    def to_dict(self) -> dict:
        """Convierte el objeto User a un diccionario para serialización."""
        return {
            "user_id": self._user_id,
            "username": self._username,
            "identification": self._identification,
            "name": self._name,
            "email": self._email,
            "birth_date": self._birth_date,
            "password": self._password,
            "status": self._status,
            "type": "user"
        }

    @staticmethod
    def validate_username(username: str) -> bool:
        """Valida que el username tenga entre 4 y 20 caracteres alfanuméricos."""
        return 3 <= len(username) <= 20 and username.isalnum()

    @staticmethod
    def validate_email(email: str) -> bool:
        """Valida que el email tenga un formato correcto."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def validate_password(password: str) -> bool:
        """Valida que la contraseña tenga al menos 6 caracteres."""
        return len(password) >= 6

    @staticmethod
    def validate_identification(identification: str) -> bool:
        """Valida que la identificación tenga entre 5 y 20 caracteres."""
        return 5 <= len(identification) <= 20

    @staticmethod
    def validate_name(name: str) -> bool:
        """Valida que el nombre tenga al menos 3 caracteres."""
        return len(name.strip()) >= 3

class Client(User):
    """Clase que representa un usuario cliente del cinema."""
    
    def __init__(self, user_id: int, username: str, identification: str, name: str, 
                    email: str, birth_date: str, password: str, 
                    status: Literal['active', 'inactive'] = 'active'):
        super().__init__(user_id, username, identification, name, email, birth_date, password, status)
    
    def to_dict(self) -> dict:
        user_dict = super().to_dict()
        user_dict["type"] = "client"
        return user_dict

class Admin(User):
    """Clase que representa un usuario administrador del sistema."""
    
    def __init__(self, user_id: int, username: str, identification: str, name: str, 
                    email: str, birth_date: str, password: str, 
                    status: Literal['active', 'inactive'] = 'active'):
        super().__init__(user_id, username, identification, name, email, birth_date, password, status)
    
    def to_dict(self) -> dict:
        user_dict = super().to_dict()
        user_dict["type"] = "admin"
        return user_dict