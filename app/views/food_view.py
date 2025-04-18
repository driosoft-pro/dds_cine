from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich import box

class FoodView:
    """Vista para el menú de comida."""
    
    def __init__(self):
        self.console = Console()
    
    def show_food_menu(self, is_admin: bool):
        """Muestra el menú de comida según el tipo de usuario."""
        self.console.print("\n[bold]Menú de Comida[/]" if not is_admin else "[bold]Gestión de Menú[/]")
        
        if is_admin:
            self.console.print("1. Listar items")
            self.console.print("2. Buscar item")
            self.console.print("3. Agregar item")
            self.console.print("4. Actualizar item")
            self.console.print("5. Desactivar item")
            self.console.print("0. Volver al menú principal")
            return Prompt.ask("Seleccione una ID", choices=["0", "1", "2", "3", "4", "5"])
        else:
            self.console.print("1. Ver menú completo")
            self.console.print("2. Buscar por categoría")
            self.console.print("0. Volver al menú principal")
            return Prompt.ask("Seleccione una ID", choices=["0", "1", "2"])
    
    def show_food_items(self, items: list, by_category: bool = False):
        """Muestra los items del menú de comida."""
        if by_category:
            categories = {item['category'] for item in items}
            for category in categories:
                self.console.print(f"\n[bold]{category}[/]")
                table = Table(box=box.SIMPLE)
                table.add_column("ID", style="cyan")
                table.add_column("Código", style="yellow")
                table.add_column("Producto", style="magenta")
                table.add_column("Tamaño", style="white")
                table.add_column("Precio", style="green")
                
                for item in [i for i in items if i['category'] == category]:
                    table.add_row(
                        item['code'],
                        item['product'],
                        item.get('size', '-'),
                        f"${item['price']:,.0f}"
                    )
                
                self.console.print(table)
        else:
            table = Table(title="[bold]Menú de Comida[/]", box=box.ROUNDED)
            table.add_column("ID", style="cyan")
            table.add_column("Código", style="yellow")
            table.add_column("Categoría", style="blue")
            table.add_column("Producto", style="magenta")
            table.add_column("Tamaño", style="white")
            table.add_column("Precio", style="green")
            
            for item in items:
                table.add_row(
                    str(item['item_id']),
                    item['code'],
                    item['category'],
                    item['product'],
                    item.get('size', '-'),
                    f"${item['price']:,.0f}"
                )
            
            self.console.print(table)
    
    def get_food_item_data(self):
        """Obtiene datos para crear/actualizar un item de comida."""
        data = {
            'item_id': Prompt.ask("ID del producto"),
            'code': Prompt.ask("Código del producto"),
            'category': Prompt.ask("Categoría"),
            'product': Prompt.ask("Nombre del producto"),
            'price': float(Prompt.ask("Precio")),
            'description': Prompt.ask("Descripción")
        }
        
        if Prompt.ask("Tiene tamaño? (s/n)", choices=["s", "n"]) == "s":
            data['size'] = Prompt.ask("Tamaño", choices=["Pequeño", "Mediano", "Grande"])
        
        return data
    
    def select_food_items(self, items: list) -> list:
        """Permite seleccionar items del menú para agregar a una compra."""
        self.show_food_items(items)
        selected_items = []
        
        while True:
            code = Prompt.ask(
                "Ingrese código del producto (o 'fin' para terminar)", 
                default="fin"
            )
            
            if code.lower() == 'fin':
                break
            
            item = next((i for i in items if i['code'].lower() == code.lower()), None)
            if item:
                quantity = int(Prompt.ask(f"Cantidad para '{item['product']}'", default="1"))
                selected_items.append({'item': item, 'quantity': quantity})
            else:
                self.console.print("[red]Código no encontrado. Intente nuevamente.[/]")
        
        return selected_items
    
    def show_order_summary(self, items: list, total: float):
        """Muestra un resumen del pedido de comida."""
        table = Table(title="[bold]Resumen de Pedido[/]", box=box.ROUNDED)
        table.add_column("Producto", style="magenta")
        table.add_column("Cantidad", style="white")
        table.add_column("Precio Unit.", style="green")
        table.add_column("Subtotal", style="yellow")
        
        for item in items:
            table.add_row(
                item['item']['product'],
                str(item['quantity']),
                f"${item['item']['price']:,.0f}",
                f"${item['item']['price'] * item['quantity']:,.0f}"
            )
        
        self.console.print(table)
        self.console.print(f"\n[bold]Total a pagar:[/] [yellow]${total:,.0f}[/]")