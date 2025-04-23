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
    
    def get_food_item_data(self, include_id: bool = True, is_update: bool = False, current_data: Dict = None) -> Optional[Dict]:
        data = {}

        def cancelar(valor):
            return valor.strip().lower() == "volver"

        if include_id:
            valor = Prompt.ask("ID del producto")
            if cancelar(valor):
                return None
            if not valor.isdigit():
                print("ID inválido.")
                return None
            data['item_id'] = int(valor)

        # --- Código del producto ---
        code_actual = current_data.get("code") if is_update else ""
        prompt_code = f"Código del producto [{code_actual}]" if is_update else "Código del producto"
        while True:
            valor = Prompt.ask(prompt_code)
            if cancelar(valor):
                return None
            if valor:
                data['code'] = valor
                break
            elif is_update:
                data['code'] = code_actual
                break
            else:
                print("El código es obligatorio.")

        # --- Categoría ---
        cat_actual = current_data.get("category") if is_update else ""
        prompt_cat = f"Categoría [{cat_actual}]" if is_update else "Categoría"
        while True:
            valor = Prompt.ask(prompt_cat)
            if cancelar(valor):
                return None
            if valor:
                data['category'] = valor
                break
            elif is_update:
                data['category'] = cat_actual
                break
            else:
                print("La categoría es obligatoria.")

        # --- Nombre del producto ---
        prod_actual = current_data.get("product") if is_update else ""
        prompt_prod = f"Nombre del producto [{prod_actual}]" if is_update else "Nombre del producto"
        while True:
            valor = Prompt.ask(prompt_prod)
            if cancelar(valor):
                return None
            if valor:
                data['product'] = valor
                break
            elif is_update:
                data['product'] = prod_actual
                break
            else:
                print("El nombre es obligatorio.")

        # --- Precio ---
        price_actual = str(current_data.get("price")) if is_update else ""
        prompt_price = f"Precio [{price_actual}]" if is_update else "Precio"
        while True:
            valor = Prompt.ask(prompt_price)
            if cancelar(valor):
                return None
            if valor:
                try:
                    data['price'] = float(valor)
                    break
                except ValueError:
                    print("Precio inválido. Debe ser un número.")
            elif is_update:
                data['price'] = current_data.get('price')
                break
            else:
                print("El precio es obligatorio.")

        # --- Descripción ---
        desc_actual = current_data.get("description") if is_update else ""
        prompt_desc = f"Descripción [{desc_actual}]" if is_update else "Descripción"
        valor = Prompt.ask(prompt_desc)
        if cancelar(valor):
            return None
        data['description'] = valor or desc_actual

        # --- Tamaño (opcional) ---
        tiene_tamano = Prompt.ask("¿Tiene tamaño? (s/n)", choices=["s", "n"])
        if cancelar(tiene_tamano):
            return None

        if tiene_tamano == "s":
            opciones = {"1": "Pequeño", "2": "Mediano", "3": "Grande"}
            size_actual = current_data.get("size") if is_update else ""
            prompt_size = "Seleccione tamaño:\n  1. Pequeño\n  2. Mediano\n  3. Grande\nIngrese número"
            if is_update and size_actual:
                prompt_size += f" (ENTER para mantener actual [{size_actual}])"
            while True:
                valor = Prompt.ask(prompt_size)
                if cancelar(valor):
                    return None
                if valor == "":
                    data['size'] = size_actual if is_update else None
                    break
                elif valor in opciones:
                    data['size'] = opciones[valor]
                    break
                else:
                    print("Opción inválida.")
        else:
            data['size'] = None

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