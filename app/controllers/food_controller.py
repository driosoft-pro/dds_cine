from typing import Dict, List, Optional
from models.food import Food
from core.database import Database

class FoodController:
    """Controlador para manejar operaciones relacionadas con el menú de comida."""
    
    def __init__(self, db: Database):
        self.db = db
        self.food_file = "food_menu.json"
    
    def create_food_item(self, code: str, category: str, product: str, 
                        price: float, description: str, size: str = None) -> Dict:
        """Crea un nuevo ítem en el menú de comida."""
        food_items = self.db.load_data(self.food_file)
        item_id = self.db.get_next_id(self.food_file)
        
        new_item = Food(
            item_id=item_id,
            code=code,
            category=category,
            product=product,
            size=size,
            price=price,
            description=description
        )
        
        food_items.append(new_item.to_dict())
        self.db.save_data(self.food_file, food_items)
        return new_item.to_dict()
    
    def get_food_item_by_id(self, item_id: int) -> Optional[Dict]:
        """Obtiene un ítem de comida por su ID."""
        food_items = self.db.load_data(self.food_file)
        for item in food_items:
            if item['item_id'] == item_id:
                return item
        return None
    
    def update_food_item(self, item_id: int, **kwargs) -> Optional[Dict]:
        """Actualiza los datos de un ítem de comida."""
        food_items = self.db.load_data(self.food_file)
        for i, item in enumerate(food_items):
            if item['item_id'] == item_id:
                for key, value in kwargs.items():
                    if key in item and key != 'item_id':
                        food_items[i][key] = value
                self.db.save_data(self.food_file, food_items)
                return food_items[i]
        return None
    
    def delete_food_item(self, item_id: int) -> bool:
        """Elimina un ítem de comida (cambia su estado a inactivo)."""
        food_items = self.db.load_data(self.food_file)
        for i, item in enumerate(food_items):
            if item['item_id'] == item_id:
                food_items[i]['status'] = 'inactivo'
                self.db.save_data(self.food_file, food_items)
                return True
        return False
    
    def list_food_items(self, active_only: bool = True) -> List[Dict]:
        """Lista todos los ítems de comida."""
        food_items = self.db.load_data(self.food_file)
        if active_only:
            return [i for i in food_items if i['status'] == 'activo']
        return food_items
    
    def search_food_items(self, name: str = None, category: str = None) -> List[Dict]:
        """Busca ítems de comida por nombre o categoría."""
        food_items = self.db.load_data(self.food_file)
        results = []
        
        for item in food_items:
            if item['status'] != 'activo':
                continue
                
            match = True
            if name and name.lower() not in item['product'].lower():
                match = False
            if category and category.lower() != item['category'].lower():
                match = False
            
            if match:
                results.append(item)
        
        return results