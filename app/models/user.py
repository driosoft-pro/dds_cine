from datetime import datetime
from typing import Optional

class User:
    """
    Clase que representa a un usuario del sistema.
    
    Attributes:
        user_id (int): Identificador único del usuario.
        username (str): Nombre de usuario para login.
        identification (str): Número de identificación.
        name (str): Nombre completo del usuario.
        email (str): Correo electrónico.
        birth_date (datetime): Fecha de nacimiento.
        password (str): Contraseña encriptada.
        status (str): Estado del usuario (activo/inactivo).
    """
    
    def __init__(self, user_id: int, username: str, identification: str, name: str, 
                    email: str, birth_date: datetime, password: str, status: str = "activo", is_admin: bool = False):
        self.user_id = user_id
        self.username = username
        self.identification = identification
        self.name = name
        self.email = email
        self.birth_date = birth_date
        self.password = password
        self.status = status
        self.is_admin = is_admin
    
    def to_dict(self) -> dict:
        """Convierte el objeto User a un diccionario para serialización."""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "identification": self.identification,
            "name": self.name,
            "email": self.email,
            "birth_date": self.birth_date.strftime("%Y-%m-%d"),
            "password": self.password,
            "status": self.status,
            "is_admin": self.is_admin
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """Crea un objeto User desde un diccionario."""
        return cls(
            user_id=data["user_id"],
            username=data["username"],
            identification=data["identification"],
            name=data["name"],
            email=data["email"],
            birth_date=datetime.strptime(data["birth_date"], "%Y-%m-%d"),
            password=data["password"],
            status=data.get("status", "activo"),
            is_admin=data.get("is_admin", False)
        )

class Admin(User):
    """Clase que representa a un administrador, hereda de User."""
    
    def __init__(self, user_id: int, username: str, identification: str, name: str, 
                    email: str, birth_date: datetime, password: str, status: str = "activo", is_admin: bool = True):
        super().__init__(user_id, username, identification, name, email, birth_date, password, status, is_admin)
        self.is_admin = True
    
    def to_dict(self) -> dict:
        """Convierte el objeto Admin a un diccionario."""
        data = super().to_dict()
        data['is_admin'] = True
        return data