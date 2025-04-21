import hashlib
from datetime import datetime
from typing import Dict, List, Optional
from models.user import User, Admin
from core.database import Database

class UserController:
    """Controlador para manejar operaciones relacionadas con usuarios."""
    
    def __init__(self, db: Database):
        self.db = db
        self.users_file = "users.json"
    
    def create_user(self, username: str, identification: str, name: str, 
                    email: str, birth_date: datetime, password: str, 
                    is_admin: bool = False) -> Dict:
        """Crea un nuevo usuario."""
        users = self.db.load_data(self.users_file)
        user_id = self.db.get_next_id(self.users_file)
        
        if any(u['username'] == username for u in users):
            raise ValueError("El nombre de usuario ya existe")
        
        if any(u['email'] == email for u in users):
            raise ValueError("El correo electrónico ya está registrado")
        
        user_class = Admin if is_admin else User
        new_user = user_class(
            user_id=user_id,
            username=username,
            identification=identification,
            name=name,
            email=email,
            birth_date=birth_date,
            password=password
        )
        
        users.append(new_user.to_dict())
        self.db.save_data(self.users_file, users)
        return new_user.to_dict()
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Obtiene un usuario por su ID."""
        users = self.db.load_data(self.users_file)
        for user in users:
            if user['user_id'] == user_id:
                return user
        return None
    
    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """Obtiene un usuario por su nombre de usuario."""
        users = self.db.load_data(self.users_file)
        for user in users:
            if user['username'] == username:
                return user
        return None
    
    def get_password_user(self, username: str) -> Optional[str]:
        """Obtiene la contraseña de un usuario."""
        users = self.db.load_data(self.users_file)
        for user in users:
            if user['username'] == username:
                return user['password']
        return None
    
    def update_user(self, user_id: int, **kwargs) -> Optional[Dict]:
        """Actualiza los datos de un usuario."""
        users = self.db.load_data(self.users_file)
        for i, user in enumerate(users):
            if user['user_id'] == user_id:
                for key, value in kwargs.items():
                    if key in user and key != 'user_id':
                        users[i][key] = value
                self.db.save_data(self.users_file, users)
                return users[i]
        return None
    
    def delete_user(self, user_id: int) -> bool:
        """Elimina un usuario (cambia su estado a inactivo)."""
        users = self.db.load_data(self.users_file)
        for i, user in enumerate(users):
            if user['user_id'] == user_id:
                users[i]['status'] = 'inactivo'
                self.db.save_data(self.users_file, users)
                return True
        return False
    
    def list_users(self, active_only: bool = True) -> List[Dict]:
        """Lista todos los usuarios."""
        users = self.db.load_data(self.users_file)
        if active_only:
            return [u for u in users if u['status'] == 'activo']
        return users
    
    def authenticate(self, username: str, password: str) -> Optional[Dict]:
        """Autentica a un usuario."""
        user = self.get_user_by_username(username)
        if user and user['password'] == password and user['status'] == 'activo':
            return user
        return None
    
    def exists_user(self, username: str) -> bool:
        """Verifica si un usuario existe."""
        return self.get_user_by_username(username) is not None
    
    def check_password_user(self, username: str, password: str) -> bool:
        """Verifica si la contraseña de un usuario es correcta."""
        user = self.get_user_by_username(username)
        if user is None or user.get('password') is None:
            return False
        # Comparación segura incluso si password es None
        return user['password'] == hashlib.sha256(password.encode()).hexdigest()