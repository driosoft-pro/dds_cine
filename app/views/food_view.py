from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich import box
from typing import Optional, Dict

class FoodView:
    """Vista para el menú de comida."""
    
    def __init__(self):
        self.console = Console()
    

    def show_food_menu(self, is_admin: bool):
        """Muestra el menú de comida según el tipo de usuario con estilo uniforme."""
        titulo = "Gestión de Menú de Comida" if is_admin else "Menú de Comida"
        table = Table(
            title=titulo,
            border_style="magenta",
            box=box.ROUNDED,
        )
        table.add_column("ID", justify="center")
        table.add_column("Descripción")

        if is_admin:
            opciones = [
                ("1", "Listar items"),
                ("2", "Buscar item"),
                ("3", "Agregar item"),
                ("4", "Actualizar item"),
                ("5", "Desactivar item"),
                ("0", "Volver al menú principal"),
            ]
            valid_choices = ["1", "2", "3", "4", "5", "0"]
        else:
            opciones = [
                ("1", "Ver menú completo"),
                ("2", "Buscar por categoría"),
                ("0", "Volver al menú principal"),
            ]
            valid_choices = ["1", "2", "0"]

        for id, descripcion in opciones:
            table.add_row(id, descripcion)

        self.console.print(table)

        # Solicita la entrada del usuario y verifica si es válida
        while True:
            opcion = Prompt.ask("Escriba 0 o 'volver' para regresar al menú \nSeleccione una ID ").strip()
            if opcion in valid_choices:
                return opcion
            else:
                self.console.print("[red]ID inválida. Intente nuevamente.[/]")

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
    
    def get_food_item_data(self,include_id: bool = True,is_update: bool = False,
        current_data: Dict = None) -> Optional[Dict]:
        data: Dict = {}

        def ask_text(label: str, key: str, required: bool = True) -> Optional[str]:
            default = None
            if is_update and current_data and key in current_data:
                default = str(current_data[key] or "")
            prompt = label + (f" [{default}]" if default else "")
            val = Prompt.ask(prompt, default=default).strip()
            if val.lower() == "volver":
                return None
            if required and val == "":
                # campo obligatorio
                self.console.print("[red]Este campo es obligatorio.[/]")
                return ask_text(label, key, required)
            return val or default

        def ask_float(label: str, key: str) -> Optional[float]:
            while True:
                txt = ask_text(label, key, required=not is_update)
                if txt is None:
                    return None
                try:
                    return float(txt)
                except ValueError:
                    self.console.print("[red]Ingresa un número válido.[/]")

        def ask_int(label: str, key: str) -> Optional[int]:
            while True:
                txt = ask_text(label, key, required=not is_update)
                if txt is None:
                    return None
                if txt.isdigit():
                    return int(txt)
                self.console.print("[red]Ingresa un entero válido.[/]")

        # --- ID (solo en admin y si include_id) ---
        if include_id:
            id_label = "ID del producto"
            default_id = str(current_data.get("item_id")) if (is_update and current_data) else None
            val = Prompt.ask(id_label, default=default_id).strip()
            if val.lower() == "volver":
                return None
            if not val.isdigit():
                self.console.print("[red]ID inválido.[/]")
                return None
            data["item_id"] = int(val)

        # --- Código ---
        code = ask_text("Código del producto", "code")
        if code is None: return None
        data["code"] = code

        # --- Categoría ---
        category = ask_text("Categoría", "category")
        if category is None: return None
        data["category"] = category

        # --- Producto ---
        product = ask_text("Nombre del producto", "product")
        if product is None: return None
        data["product"] = product

        # --- Precio ---
        price = ask_float("Precio", "price")
        if price is None: return None
        data["price"] = price

        # --- Descripción (opcional) ---
        desc = ask_text("Descripción", "description", required=False)
        if desc is None and not is_update:
            desc = ""
        if desc is None:
            return None
        data["description"] = desc

        # --- Tamaño (opcional) ---
        size_default = ""
        if is_update and current_data:
            size_default = current_data.get("size") or ""
        # Usamos default="" para que Prompt.ask nunca devuelva None
        has_size = Prompt.ask(
            f"¿Tiene tamaño? (s/n){' ['+size_default+']' if size_default else ''}",
            choices=["s","n"],
            default="s" if size_default else "n"
        ).strip()
        if has_size.lower() == "volver":
            return None

        if has_size == "s":
            opts = {"1": "Pequeño", "2": "Mediano", "3": "Grande"}
            prompt = "Selecciona tamaño:\n" + "\n".join(f"{k}. {v}" for k,v in opts.items())
            if size_default:
                prompt += f" (ENTER para mantener [{size_default}])"
            while True:
                # <-- aquí cambiamos default=None a default=""
                raw = Prompt.ask(prompt, default="")  
                choice = raw.strip()
                if choice.lower() == "volver":
                    return None
                if choice == "" and size_default:
                    data["size"] = size_default
                    break
                if choice in opts:
                    data["size"] = opts[choice]
                    break
                self.console.print("[red]Opción inválida.[/]")

        else:
            data["size"] = None

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