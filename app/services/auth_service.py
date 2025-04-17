import hashlib
from datetime import datetime
from typing import Optional, Dict
from core.database import Database
from models.user import Admin
from controllers.user_controller import UserController

class AuthService:
    """Servicio para manejar autenticación y autorización de usuarios."""
    
    def __init__(self, db: Database):
        self.user_controller = UserController(db)
        self.current_user = None
    
    def hash_password(self, password: str) -> str:
        """Encripta una contraseña usando SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, username: str, identification: str, name: str, 
                        email: str, birth_date: datetime, password: str, 
                        is_admin: bool = False) -> Dict:
        """Registra un nuevo usuario en el sistema."""
        hashed_password = self.hash_password(password)
        return self.user_controller.create_user(
            username=username,
            identification=identification,
            name=name,
            email=email,
            birth_date=birth_date,
            password=hashed_password,
            is_admin=is_admin
        )
    
    def login(self, username: str, password: str) -> Optional[Dict]:
        """Autentica a un usuario y establece la sesión actual."""
        hashed_password = self.hash_password(password)
        user = self.user_controller.authenticate(username, hashed_password)
        if user:
            self.current_user = user
            return user
        return None
    
    def logout(self) -> None:
        """Cierra la sesión del usuario actual."""
        self.current_user = None
    
    def is_authenticated(self) -> bool:
        """Verifica si hay un usuario autenticado."""
        return self.current_user is not None
    
    def is_admin(self) -> bool:
        """Verifica si el usuario actual es administrador."""
        if not self.is_authenticated():
            return False
        
        user_data = self.user_controller.get_user_by_id(self.current_user['user_id'])
        return user_data.get('is_admin', False) if user_data else False
    
    def get_current_user(self) -> Optional[Dict]:
        """Obtiene los datos del usuario actual."""
        return self.current_user