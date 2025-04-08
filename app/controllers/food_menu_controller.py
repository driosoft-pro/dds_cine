from typing import List, Optional, Dict
from models.food_menu import MenuItem, Combo, Snack, Drink, Candy

class FoodMenuController:
    def __init__(self, db):
        self.db = db
    
    def get_next_item_id(self) -> int:
        """Obtiene el próximo ID autoincremental"""
        items = self.db.get_all_food_items()
        return max(item.item_id for item in items) + 1 if items else 1
    
    def create_item(self, item_data: Dict) -> Optional[MenuItem]:
        """Crea un nuevo ítem en el menú"""
        try:
            item_id = self.get_next_item_id()
            item_type = item_data.get('type', 'base')
            
            if item_type == 'combo':
                item = Combo(
                    item_id=item_id,
                    code=item_data['code'],
                    product=item_data['product'],
                    size=item_data['size'],
                    price=item_data['price'],
                    included_items=item_data['included_items']
                )
            elif item_type == 'snack':
                item = Snack(
                    item_id=item_id,
                    code=item_data['code'],
                    product=item_data['product'],
                    size=item_data['size'],
                    price=item_data['price']
                )
            elif item_type == 'drink':
                item = Drink(
                    item_id=item_id,
                    code=item_data['code'],
                    product=item_data['product'],
                    size=item_data['size'],
                    price=item_data['price']
                )
            elif item_type == 'candy':
                item = Candy(
                    item_id=item_id,
                    code=item_data['code'],
                    product=item_data['product'],
                    price=item_data['price']
                )
            else:
                return None
                
            self.db.save_food_item(item)
            return item
            
        except Exception as e:
            print(f"Error creating menu item: {e}")
            return None
    
    def get_all_items(self) -> List[MenuItem]:
        """Obtiene todos los ítems del menú"""
        return self.db.get_all_food_items()
    
    def get_items_by_category(self, category: str) -> List[MenuItem]:
        """Obtiene ítems por categoría"""
        return [item for item in self.db.get_all_food_items() 
                if item.category.lower() == category.lower()]
    
    def get_active_items(self) -> List[MenuItem]:
        """Obtiene ítems activos"""
        return [item for item in self.db.get_all_food_items() 
                if item.status == 'active']
    
    def update_item(self, item_id: int, update_data: Dict) -> bool:
        """Actualiza un ítem del menú"""
        item = self.db.get_food_item(item_id)
        if not item:
            return False
            
        for key, value in update_data.items():
            if hasattr(item, key):
                setattr(item, key, value)
                
        return self.db.save_food_item(item)
    
    def change_item_status(self, item_id: int, status: str) -> bool:
        """Cambia el estado de un ítem"""
        item = self.db.get_food_item(item_id)
        if not item:
            return False
            
        item.status = status
        return self.db.save_food_item(item)