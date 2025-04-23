def handle_food_menu(self):
    """Muestra el menú de comida y permite realizar pedidos (cliente)."""
    choice = self.food_view.show_food_menu(is_admin=False)
    
    if choice == "1":  # Ver menú completo
        items = self.food_controller.list_food_items()
        self.food_view.show_food_items(items)
        self.menu_view.press_enter_to_continue()
    
    elif choice == "2":  # Buscar por categoría
        items = self.food_controller.list_food_items()
        self.food_view.show_food_items(items, by_category=True)
        self.menu_view.press_enter_to_continue()