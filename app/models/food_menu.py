from typing import Literal
from dataclasses import dataclass

@dataclass
class MenuItem:
    """Clase base para items del menú"""
    item_id: int
    code: str
    category: str
    product: str
    size: str
    price: float
    status: Literal['active', 'inactive'] = 'active'
    
    def to_dict(self) -> dict:
        """Convierte el objeto a diccionario para serialización"""
        return {
            'item_id': self.item_id,
            'code': self.code,
            'category': self.category,
            'product': self.product,
            'size': self.size,
            'price': self.price,
            'status': self.status,
            'type': 'base'
        }

class Combo(MenuItem):
    """Clase para combos especiales"""
    def __init__(self, item_id: int, code: str, product: str, 
                    size: str, price: float, included_items: list,
                    status: Literal['active', 'inactive'] = 'active'):
        super().__init__(item_id, code, 'Combo', product, size, price, status)
        self.included_items = included_items
        
    def to_dict(self) -> dict:
        """Convierte el objeto a diccionario para serialización"""
        data = super().to_dict()
        data.update({
            'included_items': self.included_items,
            'type': 'combo'
        })
        return data

class Snack(MenuItem):
    """Clase para snacks individuales"""
    def __init__(self, item_id: int, code: str, product: str, 
                    size: str, price: float, 
                    status: Literal['active', 'inactive'] = 'active'):
        super().__init__(item_id, code, 'Snack', product, size, price, status)

class Drink(MenuItem):
    """Clase para bebidas"""
    def __init__(self, item_id: int, code: str, product: str, 
                    size: str, price: float, 
                    status: Literal['active', 'inactive'] = 'active'):
        super().__init__(item_id, code, 'Drink', product, size, price, status)

class Candy(MenuItem):
    """Clase para dulces"""
    def __init__(self, item_id: int, code: str, product: str, 
                    price: float, 
                    status: Literal['active', 'inactive'] = 'active'):
        super().__init__(item_id, code, 'Candy', product, 'Único', price, status)

def edit_menu_item(menu_items: list, item_id: int, **kwargs) -> bool:
    """
    Edita un ítem del menú basado en su item_id.
    
    Args:
        menu_items (list): Lista de ítems del menú.
        item_id (int): ID del ítem a editar.
        **kwargs: Atributos a actualizar (ej. product, price, status).
    
    Returns:
        bool: True si el ítem fue editado exitosamente, False si no se encontró.
    """
    for item in menu_items:
        if item.item_id == item_id:
            # Actualizar los atributos proporcionados en kwargs
            for key, value in kwargs.items():
                if hasattr(item, key):
                    setattr(item, key, value)
            return True
    return False

def search_menu_items(menu_items: list, **criteria) -> list:
    """
    Busca ítems en el menú basado en criterios específicos.
    
    Args:
        menu_items (list): Lista de ítems del menú.
        **criteria: Criterios de búsqueda (ej. category='Snack', status='active').
    
    Returns:
        list: Lista de ítems que coinciden con los criterios.
    """
    results = menu_items
    for key, value in criteria.items():
        results = [item for item in results if hasattr(item, key) and getattr(item, key) == value]
    return results

def change_menu_item_status(menu_items: list, item_id: int, new_status: Literal['active', 'inactive']) -> bool:
    """
    Cambia el estado de un ítem del menú (active/inactive).
    
    Args:
        menu_items (list): Lista de ítems del menú.
        item_id (int): ID del ítem cuyo estado se desea cambiar.
        new_status (Literal['active', 'inactive']): Nuevo estado del ítem.
    
    Returns:
        bool: True si el estado fue cambiado exitosamente, False si no se encontró el ítem.
    """
    for item in menu_items:
        if item.item_id == item_id:
            if new_status in ['active', 'inactive']:
                item.status = new_status
                return True
    return False