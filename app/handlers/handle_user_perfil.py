def handle_user_perfil(self):
    """Maneja la gestión de perfil de usuario."""
    while True:
        choice = self.user_view.show_user_menu(is_admin=False)  
        
        # Salir
        if choice == "0":
            return
        
        # Ver mi perfil
        if choice == "1":
            user_id = self.current_user['user_id']
            user = self.user_controller.get_user_by_id(user_id)
            if user:
                self.user_view.show_user_details(user, is_admin=False)
            else:
                self.menu_view.show_message("No se encontró su perfil", is_error=True)
            self.menu_view.press_enter_to_continue()
        
        # Editar perfil
        elif choice == "2":
            user_id = self.current_user['user_id']
            user = self.user_controller.get_user_by_id(user_id)

            self.menu_view.press_enter_to_continue()
        
        # Cambiar contraseña
        elif choice == "3":
            user_id = self.current_user['user_id']
            user = self.user_controller.get_user_by_id(user_id)

            self.menu_view.press_enter_to_continue()
        
        # Desactivar cuenta    
        elif choice == "4":
            user_id = self.current_user['user_id']
            user = self.user_controller.get_user_by_id(user_id)
            if self.user_controller.delete_user(user_id):
                self.menu_view.show_message("Usuario desactivado con éxito!")
            else:
                self.menu_view.show_message("Error al desactivar el usuario", is_error=True)