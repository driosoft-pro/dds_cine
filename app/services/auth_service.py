from typing import Optional
from models.user import User, Client, Admin

class AuthService:
    """Servicio para manejar autenticación y registro de usuarios."""
    
    def __init__(self, db):
        from controllers.user_controller import UserController
        self.user_controller = UserController(db)
    
    def authenticate(self, username: str, password: str) -> Optional[User]:
        """
        Autentica un usuario basado en username y password.
        Valida primero los formatos antes de consultar la base de datos.
        """
        if not User.validate_username(username):
            return None
            
        if not User.validate_password(password):
            return None
            
        return self.user_controller.authenticate_user(username, password)
    
    def register(self, user_data: dict, user_type: str) -> Optional[User]:
        return self.user_controller.create_user(user_data, user_type)
    
    def get_current_user(self, user_id: int) -> Optional[User]:
        return self.user_controller.get_user(user_id)