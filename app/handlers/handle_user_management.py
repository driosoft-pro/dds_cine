def handle_user_management(self):
    """Maneja la gestión de usuarios (admin)."""
    while True:
        choice = self.user_view.show_user_menu(is_admin=True)
        
        if choice == "1":  # Listar usuarios
            users = self.user_controller.list_users(active_only=False)
            self.user_view.show_users(users)
            self.menu_view.press_enter_to_continue()
        
        elif choice == "2":  # Buscar usuario
            criteria = self.user_view.get_user_search_criteria()
            if not criteria:
                self.menu_view.show_message("Volviendo al menú anterior...", is_error=False)
                return
            if 'id' in criteria:
                user = self.user_controller.get_user_by_id(int(criteria['id']))
                if user:
                    self.user_view.show_user_details(user, is_admin=True)
                else:
                    self.menu_view.show_message("Usuario no encontrado", is_error=True)
            elif 'username' in criteria:
                user = self.user_controller.get_user_by_username(criteria['username'])
                if user:
                    self.user_view.show_user_details(user, is_admin=True)
                else:
                    self.menu_view.show_message("Usuario no encontrado", is_error=True)
            else:
                users = [u for u in self.user_controller.list_users(active_only=False) 
                        if criteria['name'].lower() in u['name'].lower()]
                if users:
                    self.user_view.show_users(users)
                else:
                    self.menu_view.show_message("No se encontraron usuarios", is_error=True)
            self.menu_view.press_enter_to_continue()
        
        elif choice == "3":  # Crear usuario
            user_data = self.user_view.get_user_data()
            if user_data is None:
                self.menu_view.show_message("Operación cancelada. Volviendo al menú...")
                return
            try:
                # Convertir birth_date de string a datetime
                from datetime import datetime
                user_data['birth_date'] = datetime.strptime(user_data['birth_date'], "%Y-%m-%d")
                new_user = self.user_controller.create_user(
                    username=user_data['username'],
                    identification=user_data['identification'],
                    name=user_data['name'],
                    email=user_data['email'],
                    birth_date=user_data['birth_date'],
                    password=user_data['password'],
                    is_admin=user_data['is_admin']
                )
                self.menu_view.show_message("Usuario creado con éxito!")
            except Exception as e:
                self.menu_view.show_message(str(e), is_error=True)
            self.menu_view.press_enter_to_continue()
        elif choice == "4":  # Actualizar usuario
            users = self.user_controller.list_users(active_only=False)
            self.user_view.show_users(users)
            while True:
                user_id_input = self.console.input("Ingrese ID del usuario a actualizar (escriba 'volver' para regresar al menú): ").strip()
                if user_id_input.lower() == "volver":
                    return
                if not user_id_input.isdigit():
                    self.menu_view.show_message("Por favor, ingrese un número válido de ID o 'volver'.", is_error=True)
                    continue
                user_id = int(user_id_input)
                break
            user_data = self.user_view.get_user_data(for_update=True)
            if user_data is None:
                return 
            if self.user_controller.update_user(user_id, **user_data):
                self.menu_view.show_message("Usuario actualizado con éxito!")
            else:
                self.menu_view.show_message("Error al actualizar el usuario", is_error=True)
            self.menu_view.press_enter_to_continue()
        
        elif choice == "5":  # Desactivar usuario
            users = self.user_controller.list_users(active_only=False)
            self.user_view.show_users(users)
            while True:
                user_id_input = self.console.input("Ingrese ID del usuario a desactivar (presione Enter para volver al menú): ").strip()
                
                # Si presiona solo Enter, vuelve al menú
                if user_id_input == "":
                    return
                if not user_id_input.isdigit():
                    self.menu_view.show_message("Por favor, ingrese un número de ID válido o presione Enter para volver.", is_error=True)
                    continue
                user_id = int(user_id_input)
                break
            if self.user_controller.delete_user(user_id):
                self.menu_view.show_message("Usuario desactivado con éxito!")
            else:
                self.menu_view.show_message("Error al desactivar el usuario", is_error=True)
                
            self.menu_view.press_enter_to_continue()
        
        elif choice == "0": #Volver al menu principal
            return