from typing import Optional

class Food:
    """
    Clase que representa un ítem del menú de comida.
    
    Attributes:
        item_id (int): Identificador único del ítem.
        code (str): Código del producto.
        category (str): Categoría (combos, snacks, bebidas, dulces).
        product (str): Nombre del producto.
        size (Optional[str]): Tamaño (pequeño, mediano, grande).
        price (float): Precio del ítem.
        description (str): Descripción del producto.
        status (str): Estado (activo/inactivo).
    """
    
    def __init__(self, item_id: int, code: str, category: str, product: str, 
                    price: float, description: str, size: Optional[str] = None, 
                    status: str = "activo"):
        self.item_id = item_id
        self.code = code
        self.category = category
        self.product = product
        self.size = size
        self.price = price
        self.description = description
        self.status = status
    
    def to_dict(self) -> dict:
        """Convierte el objeto Food a un diccionario."""
        return {
            "item_id": self.item_id,
            "code": self.code,
            "category": self.category,
            "product": self.product,
            "size": self.size,
            "price": self.price,
            "description": self.description,
            "status": self.status
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Food':
        """Crea un objeto Food desde un diccionario."""
        return cls(
            item_id=data["item_id"],
            code=data["code"],
            category=data["category"],
            product=data["product"],
            size=data.get("size"),
            price=data["price"],
            description=data["description"],
            status=data.get("status", "activo")
        )