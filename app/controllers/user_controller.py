from typing import Optional, Dict, Literal
from datetime import datetime
from models.user import User, Client, Admin

class UserController:
    """Controlador para gestionar usuarios del sistema."""
    
    def __init__(self, db):
        self.db = db
    
    def get_next_user_id(self) -> int:
        """Obtiene el próximo ID autoincremental para un nuevo usuario."""
        users = self.db.get_all_users()
        return max(user.user_id for user in users) + 1 if users else 1
    
    def create_user(self, user_data: Dict, user_type: Literal['client', 'admin']) -> Optional[User]:
        """
        Crea un nuevo usuario en el sistema con validación de datos.
        """
        try:
            # Validar datos requeridos
            required_fields = ['username', 'identification', 'name', 'email', 'birth_date', 'password']
            if not all(field in user_data for field in required_fields):
                return None
            
            # Validar formato de fecha
            try:
                datetime.strptime(user_data['birth_date'], "%Y-%m-%d")
            except ValueError:
                return None
            
            # Validar otros campos
            if not User.validate_username(user_data['username']):
                return None
            if not User.validate_identification(user_data['identification']):
                return None
            if not User.validate_name(user_data['name']):
                return None
            if not User.validate_email(user_data['email']):
                return None
            if not User.validate_password(user_data['password']):
                return None
            
            # Verificar si el username ya existe
            if self.db.get_user_by_username(user_data['username']):
                return None
            
            # Obtener próximo ID
            user_id = self.get_next_user_id()
            
            # Crear instancia según el tipo de usuario
            if user_type == 'client':
                user = Client(
                    user_id=user_id,
                    username=user_data['username'],
                    identification=user_data['identification'],
                    name=user_data['name'],
                    email=user_data['email'],
                    birth_date=user_data['birth_date'],
                    password=user_data['password']
                )
            else:
                user = Admin(
                    user_id=user_id,
                    username=user_data['username'],
                    identification=user_data['identification'],
                    name=user_data['name'],
                    email=user_data['email'],
                    birth_date=user_data['birth_date'],
                    password=user_data['password']
                )
            
            self.db.save_user(user)
            return user
            
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """
        Autentica un usuario basado en su username y contraseña.
        """
        user = self.db.get_user_by_username(username)
        if user and user.password == password and user.status == 'active':
            return user
        return None
    
    def get_user(self, user_id: int) -> Optional[User]:
        return self.db.get_user(user_id)
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        return self.db.get_user_by_username(username)
    
    def get_user_by_identification(self, identification: str) -> Optional[User]:
        return self.db.get_user_by_identification(identification)