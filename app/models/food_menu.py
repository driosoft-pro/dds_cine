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