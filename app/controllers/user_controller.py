from typing import List, Optional, Dict, Literal
from models.user import User, Client, Admin

class UserController:
    def __init__(self, db):
        self.db = db

    def get_next_user_id(self) -> int:
        users = self.db.get_all_users()
        return max(u.user_id for u in users) + 1 if users else 1

    def create_user(self, user_data: Dict, user_type: Literal['client', 'admin']) -> Optional[User]:
        try:
            # Validación de datos
            required = ['username', 'identification', 'name', 'email', 'birth_date', 'password']
            if not all(field in user_data for field in required):
                return None

            if not User.validate_email(user_data['email']):
                return None

            if not User.validate_password(user_data['password']):
                return None

            if not User.validate_birth_date(user_data['birth_date']):
                return None

            user_id = self.get_next_user_id()

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

    def get_user(self, user_id: int) -> Optional[User]:
        return self.db.get_user(user_id)

    def get_user_by_username(self, username: str) -> Optional[User]:
        return self.db.get_user_by_username(username)

    def get_user_by_identification(self, identification: str) -> Optional[User]:
        return self.db.get_user_by_identification(identification)

    def get_all_users(self) -> List[User]:
        return self.db.get_all_users()

    def update_user(self, user_id: int, update_data: Dict) -> Optional[User]:
        user = self.get_user(user_id)
        if not user:
            return None

        # Validar campos actualizables
        valid_fields = ['name', 'email', 'birth_date', 'status']
        updates = {k: v for k, v in update_data.items() if k in valid_fields}

        # Validación específica
        if 'email' in updates and not User.validate_email(updates['email']):
            return None

        if 'birth_date' in updates and not User.validate_birth_date(updates['birth_date']):
            return None

        for field, value in updates.items():
            setattr(user, f"_{field}", value)

        self.db.save_user(user)
        return user

    def change_password(self, user_id: int, new_password: str) -> bool:
        if not User.validate_password(new_password):
            return False

        user = self.get_user(user_id)
        if not user:
            return False

        user._password = new_password
        self.db.save_user(user)
        return True

    def change_status(self, user_id: int, status: str) -> bool:
        user = self.get_user(user_id)
        if not user:
            return False

        user._status = status
        self.db.save_user(user)
        return True

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Autentica un usuario basado en username y password."""
        user = self.get_user_by_username(username)
        if user and user.password == password and user.status == 'active':
            return user
        return None
    
    def search_user(self, term: str) -> Optional[User]:
        """Busca un usuario por username, email o identificación"""
        for user in self.get_all_users():
            if term.lower() in user.username.lower() or \
                term.lower() in user.email.lower() or \
                term == user.identification:
                return user
        return None
