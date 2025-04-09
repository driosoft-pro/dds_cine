from typing import Literal
from datetime import datetime
import re

class User:
    """Clase base para usuarios del sistema"""
    def __init__(self, user_id: int, username: str, identification: str, 
                    name: str, email: str, birth_date: str, password: str,
                    status: Literal['active', 'inactive'] = 'active'):
        self._user_id = user_id
        self._username = username
        self._identification = identification
        self._name = name
        self._email = email
        self._birth_date = birth_date
        self._password = password
        self._status = status

    # Propiedades (encapsulamiento)
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
    def status(self) -> str:
        return self._status
        
    @property
    def password(self) -> str:
        return self._password

    def get_age(self) -> int:
        """Calcula la edad del usuario"""
        birth_date = datetime.strptime(self._birth_date, "%Y-%m-%d")
        today = datetime.now()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    def to_dict(self) -> dict:
        """Serializa el usuario a diccionario"""
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

    # Métodos estáticos para validación
    @staticmethod
    def validate_username(username: str) -> bool:
        """Valida que el username tenga entre 4 y 20 caracteres alfanuméricos"""
        return 4 <= len(username) <= 20 and username.isalnum()

    @staticmethod
    def validate_email(email: str) -> bool:
        return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email))
        
    @staticmethod
    def validate_password(password: str) -> bool:
        return len(password) >= 6
        
    @staticmethod
    def validate_birth_date(date: str) -> bool:
        try:
            datetime.strptime(date, "%Y-%m-%d")
            return True
        except ValueError:
            return False

class Client(User):
    """Clase para usuarios clientes"""
    def __init__(self, user_id: int, username: str, identification: str, 
                    name: str, email: str, birth_date: str, password: str,
                    status: Literal['active', 'inactive'] = 'active'):
        super().__init__(user_id, username, identification, name, email, birth_date, password, status)

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "client"
        return data

class Admin(User):
    """Clase para usuarios administradores"""
    def __init__(self, user_id: int, username: str, identification: str, 
                    name: str, email: str, birth_date: str, password: str,
                    status: Literal['active', 'inactive'] = 'active'):
        super().__init__(user_id, username, identification, name, email, birth_date, password, status)

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "admin"
        return data