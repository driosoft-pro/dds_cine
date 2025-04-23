def handle_food_management(self):
    """Maneja la gestión del menú de comida (admin)."""
    while True:
        # Asegurémonos de que la opción sea válida, incluso si el usuario presiona Enter sin ingresar nada
        choice = self.food_view.show_food_menu(is_admin=True).strip()
        # Verificamos que la opción no esté vacía y que sea válida
        if choice in ["1", "2", "3", "4", "5", "0"]:
            if choice == "1":  # Listar items
                items = self.food_controller.list_food_items()
                self.food_view.show_food_items(items)
                self.menu_view.press_enter_to_continue()
            elif choice == "2":  # Buscar item
                name = self.console.input("Ingrese nombre o parte del nombre del producto: ")
                results = self.food_controller.search_food_items(name=name)
                self.food_view.show_food_items(results)
                self.menu_view.press_enter_to_continue()
            elif choice == "3":  # Agregar item
                item_data = self.food_view.get_food_item_data(include_id=False)
                if item_data is None:
                    self.menu_view.show_message("Operación cancelada.")
                else:
                    try:
                        new_item = self.food_controller.create_food_item(**item_data)
                        self.menu_view.show_message("Ítem agregado al menú con éxito!")
                    except Exception as e:
                        self.menu_view.show_message(str(e), is_error=True)
                self.menu_view.press_enter_to_continue()
            elif choice == "4":  # Actualizar item
                items = self.food_controller.list_food_items()
                self.food_view.show_food_items(items)
                item_id_input = self.console.input("Ingrese ID del ítem a actualizar (o 'volver' para cancelar): ").strip()
                if item_id_input.lower() == "volver":
                    self.menu_view.show_message("Operación cancelada.")
                    self.menu_view.press_enter_to_continue()
                    return
                if not item_id_input.isdigit():
                    self.menu_view.show_message("ID inválido. Debe ser un número.", is_error=True)
                    self.menu_view.press_enter_to_continue()
                    continue  # Volver a pedir la opción
                item_id = int(item_id_input)
                current_item = next((item for item in items if item["item_id"] == item_id), None)
                if not current_item:
                    self.menu_view.show_message("Ítem no encontrado.", is_error=True)
                    self.menu_view.press_enter_to_continue()
                    continue  # Volver a pedir la opción
                item_data = self.food_view.get_food_item_data(include_id= False,is_update=True, current_data=current_item)
                if item_data is None:
                    self.menu_view.show_message("Operación cancelada.")
                else:
                    if self.food_controller.update_food_item(item_id, **item_data):
                        self.menu_view.show_message("Ítem actualizado con éxito!")
                    else:
                        self.menu_view.show_message("Error al actualizar el ítem", is_error=True)
                self.menu_view.press_enter_to_continue()
            elif choice == "5":  # Desactivar item
                items = self.food_controller.list_food_items()
                self.food_view.show_food_items(items)
                item_id_input = self.console.input("Ingrese ID del ítem a desactivar: ").strip()
                if not item_id_input.isdigit():
                    self.menu_view.show_message("ID inválido. Debe ser un número.", is_error=True)
                    self.menu_view.press_enter_to_continue()
                    continue  # Volver a pedir la opción
                item_id = int(item_id_input)
                if self.food_controller.delete_food_item(item_id):
                    self.menu_view.show_message("Ítem desactivado con éxito!")
                else:
                    self.menu_view.show_message("Error al desactivar el ítem", is_error=True)
                self.menu_view.press_enter_to_continue()
            elif choice == "0":  # Volver al menú principal
                break  # Salir del ciclo y volver al menú principal
        else:
            # Mensaje si la opción no es válida, incluyendo el caso en el que no se ingresa nada
            self.menu_view.show_message("Opción no válida. Por favor, seleccione una opción válida.", is_error=True)
            self.menu_view.press_enter_to_continue()