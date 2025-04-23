import pwinput
import hashlib
def handle_user_perfil(self):
    """Maneja la gestión de perfil de usuario."""
    while True:
        choice = self.user_view.show_user_menu(is_admin=False)
        
        # 0) Volver al menú principal
        if choice == "0":
            return
        
        user_id = self.current_user['user_id']
        current = self.user_controller.get_user_by_id(user_id)
        if not current:
            self.menu_view.show_message("No se encontró su perfil", is_error=True)
            return
        
        # 1) Ver mi perfil
        if choice == "1":
            self.user_view.show_user_details(current, is_admin=False)
            self.menu_view.press_enter_to_continue()
        
        # 2) Editar mi perfil (nombre, email, etc.)
        elif choice == "2":
            # Pedimos sólo los campos de datos básicos (no username ni contraseña)
            user_data = self.user_view.get_user_data(
                for_update=True,
                current_data=current
            )
            if user_data is None:
                # Usuario canceló con 'volver'
                continue

            updated = self.user_controller.update_user(user_id, **user_data)
            if updated:
                self.menu_view.show_message("✅ Perfil actualizado con éxito!")
                # Refrescar current_user en memoria
                self.current_user = self.user_controller.get_user_by_id(user_id)
            else:
                self.menu_view.show_message("❌ Error al actualizar el perfil", is_error=True)
            self.menu_view.press_enter_to_continue()
        
        # 3) Cambiar contraseña
        elif choice == "3":
            # 3.1 Pedir contraseña actual
            self.console.print("[cyan]Contraseña actual:[/]", end=" ")
            old_pw = pwinput.pwinput(prompt="", mask="*").strip()
            if not self.user_controller.check_password_user(current['username'], old_pw):
                self.menu_view.show_message("❌ Contraseña actual incorrecta", is_error=True)
                self.menu_view.press_enter_to_continue()
                continue

            # 3.2 Pedir nueva contraseña y confirmación
            self.console.print("[cyan]Nueva contraseña:[/]", end=" ")
            new_pw = pwinput.pwinput(prompt="", mask="*").strip()
            self.console.print("[cyan]Confirma nueva contraseña:[/]", end=" ")
            confirm_pw = pwinput.pwinput(prompt="", mask="*").strip()
            if new_pw != confirm_pw:
                self.menu_view.show_message("❌ Las contraseñas no coinciden", is_error=True)
                self.menu_view.press_enter_to_continue()
                continue

            # 3.3 Actualizar la contraseña (almacenamos el hash)
            hashed = hashlib.sha256(new_pw.encode()).hexdigest()
            updated = self.user_controller.update_user(user_id, password=hashed)
            if updated:
                self.menu_view.show_message("✅ Contraseña cambiada con éxito")
            else:
                self.menu_view.show_message("❌ Error al cambiar contraseña", is_error=True)
            self.menu_view.press_enter_to_continue()
        
        # 4) Desactivar mi cuenta
        elif choice == "4":
            confirm = self.menu_view.confirm_action("¿Seguro que desea desactivar su cuenta?")
            if not confirm:
                continue
            success = self.user_controller.delete_user(user_id)
            if success:
                self.menu_view.show_message("✅ Tu cuenta ha sido desactivada")
                # Forzar logout
                self.auth_service.logout()
                return
            else:
                self.menu_view.show_message("❌ Error al desactivar tu cuenta", is_error=True)
                self.menu_view.press_enter_to_continue()
