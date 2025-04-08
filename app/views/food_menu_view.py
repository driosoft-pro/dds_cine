from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from typing import List

def display_food_menu_management(console: Console, food_controller, is_admin: bool):
    """Menú principal de gestión de comidas"""
    while True:
        console.clear()
        console.print(Panel.fit("🍿 GESTIÓN DE MENÚ DE COMIDAS", style="bold blue"))
        
        if is_admin:
            console.print("\n1. Agregar nuevo ítem")
            console.print("2. Editar ítem existente")
            console.print("3. Cambiar estado de ítem")
            console.print("4. Ver todos los ítems")
            console.print("5. Buscar ítems")
            console.print("6. Volver al menú principal\n")
            
            option = Prompt.ask("Seleccione una opción", choices=["1", "2", "3", "4", "5", "6"])
            
            if option == "1":
                handle_add_food_item(console, food_controller)
            elif option == "4":
                display_all_food_items(console, food_controller, is_admin)
            elif option == "6":
                return
            else:
                console.print("\n[bold yellow]Opción en desarrollo...[/bold yellow]")
                Prompt.ask("\nPresione Enter para continuar...")
        else:
            console.print("\n1. Ver menú completo")
            console.print("2. Ver combos")
            console.print("3. Ver snacks")
            console.print("4. Ver bebidas")
            console.print("5. Ver dulces")
            console.print("6. Volver\n")
            
            option = Prompt.ask("Seleccione una opción", choices=["1", "2", "3", "4", "5", "6"])
            
            if option == "1":
                display_all_food_items(console, food_controller, is_admin)
            elif option == "2":
                display_food_category(console, food_controller, "Combo")
            elif option == "3":
                display_food_category(console, food_controller, "Snack")
            elif option == "4":
                display_food_category(console, food_controller, "Drink")
            elif option == "5":
                display_food_category(console, food_controller, "Candy")
            elif option == "6":
                return

def handle_add_food_item(console: Console, food_controller):
    """Maneja la adición de nuevos ítems al menú"""
    console.clear()
    console.print(Panel.fit("AGREGAR NUEVO ÍTEM AL MENÚ", style="bold green"))
    
    # Selección de tipo de ítem
    console.print("\n[bold]Tipo de ítem:[/bold]")
    console.print("1: Combo")
    console.print("2: Snack")
    console.print("3: Bebida")
    console.print("4: Dulce")
    item_type = Prompt.ask("Seleccione el tipo", choices=["1", "2", "3", "4"])
    
    item_data = {'type': ['combo', 'snack', 'drink', 'candy'][int(item_type)-1]}
    
    # Datos comunes
    item_data['code'] = Prompt.ask("\nCódigo del producto (ej: CP-001)")
    item_data['product'] = Prompt.ask("Nombre del producto")
    
    if item_data['type'] != 'candy':
        item_data['size'] = Prompt.ask("Tamaño (Pequeño/Mediano/Grande/Familiar)", 
                                        default="Mediano")
    
    # Precio con validación
    while True:
        try:
            price = float(Prompt.ask("Precio (ej: 15000)"))
            item_data['price'] = price
            break
        except ValueError:
            console.print("[red]Error: Ingrese un número válido[/red]")
    
    # Datos específicos para combos
    if item_data['type'] == 'combo':
        item_data['included_items'] = []
        console.print("\n[bold]Ítems incluidos en el combo:[/bold]")
        while True:
            item = Prompt.ask("Agregar producto incluido (deje vacío para terminar)")
            if not item:
                break
            item_data['included_items'].append(item)
    
    # Crear el ítem
    item = food_controller.create_item(item_data)
    if item:
        console.print(f"\n[bold green]¡Ítem '{item.product}' agregado exitosamente![/bold green]")
    else:
        console.print("\n[bold red]Error al crear el ítem[/bold red]")
    
    Prompt.ask("\nPresione Enter para continuar...")

"""def display_all_food_items(console: Console, food_controller, is_admin: bool):
    #Muestra todos los ítems del menú
    console.clear()
    items = food_controller.get_active_items() if not is_admin else food_controller.get_all_items()
    
    if not items:
        console.print("[yellow]No hay ítems en el menú[/yellow]")
        Prompt.ask("\nPresione Enter para continuar...")
        return
    
    table = Table(title="🍿 MENÚ DEL CINEMA", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=4)
    table.add_column("Código", width=10)
    table.add_column("Categoría", width=12)
    table.add_column("Producto", min_width=20)
    table.add_column("Tamaño", width=10)
    table.add_column("Precio", justify="right", width=10)
    
    if is_admin:
        table.add_column("Estado", width=8)
    
    for item in sorted(items, key=lambda x: (x.category, x.product)):
        row = [
            str(item.item_id),
            item.code,
            item.category,
            item.product,
            item.size,
            f"${item.price:,.0f}"
        ]
        if is_admin:
            status = "[green]✔[/green]" if item.status == 'active' else "[red]✖[/red]"
            row.append(status)
        
        table.add_row(*row)
    
    console.print(table)
    
    if is_admin:
        console.print("\n[dim]Nota: ✔ = Activo, ✖ = Inactivo[/dim]")
    
    Prompt.ask("\nPresione Enter para continuar...")

def display_food_category(console: Console, food_controller, category: str):
    console.clear()
    items = food_controller.get_items_by_category(category)
    
    if not items:
        console.print(f"[yellow]No hay ítems en la categoría {category}[/yellow]")
        Prompt.ask("\nPresione Enter para continuar...")
        return
    
    table = Table(title=f"🍿 MENÚ DE {category.upper()}", show_header=True, header_style="bold magenta")
    table.add_column("Producto", min_width=25)
    table.add_column("Descripción", min_width=40)
    table.add_column("Precio", justify="right", width=12)
    
    for item in items:
        if item.category == 'Combo':
            description = f"Incluye: {', '.join(item.included_items)}"
        else:
            description = f"Tamaño: {item.size}" if hasattr(item, 'size') else "Dulce individual"
        
        table.add_row(
            item.product,
            description,
            f"${item.price:,.0f}"
        )
    
    console.print(table)
    Prompt.ask("\nPresione Enter para continuar...")"""

def display_all_food_items(console: Console, food_controller, is_admin: bool):
    """Muestra todos los ítems con diseño mejorado para clientes"""
    console.clear()
    items = food_controller.get_active_items() if not is_admin else food_controller.get_all_items()
    
    if not items:
        console.print(Panel.fit("El menú está vacío", style="bold yellow"))
        Prompt.ask("\nPresione Enter para continuar...")
        return
    
    # Diseño especial para clientes
    if not is_admin:
        console.print(Panel.fit("🍔 MENÚ COMPLETO 🍿", style="bold blue"))
        console.print("[dim]Seleccione ítems para agregar a su compra[/dim]\n")
        
        # Agrupar por categoría
        categories = {
            "Combo": [],
            "Snack": [],
            "Drink": [],
            "Candy": []
        }
        
        for item in items:
            if item.category in categories:
                categories[item.category].append(item)
        
        # Mostrar por categorías
        for category, items_in_category in categories.items():
            if items_in_category:
                console.print(Panel.fit(
                    f"[bold]{category.upper()}[/bold]",
                    style="bold green"
                ))
                
                for item in items_in_category:
                    price = f"[bold green]${item.price:,.0f}[/bold green]"
                    if item.category == "Combo":
                        desc = f"Incluye: {', '.join(item.included_items[:2])}"
                        if len(item.included_items) > 2:
                            desc += f" y {len(item.included_items)-2} más"
                    else:
                        desc = f"Tamaño: {item.size}" if hasattr(item, 'size') else "Dulce"
                    
                    console.print(f"• {item.product} - {desc} ({price})")
                
                console.print("")
        
        Prompt.ask("\nPresione Enter para continuar...")
        return
    
    # Vista para administradores (tabla detallada)
    table = Table(title="🍽️ MENÚ COMPLETO", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=4)
    table.add_column("Código", width=10)
    table.add_column("Categoría", width=12)
    table.add_column("Producto", min_width=20)
    table.add_column("Tamaño", width=10)
    table.add_column("Precio", justify="right", width=10)
    table.add_column("Estado", width=8)
    
    for item in sorted(items, key=lambda x: (x.category, x.product)):
        status = "[green]✔[/green]" if item.status == 'active' else "[red]✖[/red]"
        table.add_row(
            str(item.item_id),
            item.code,
            item.category,
            item.product,
            item.size,
            f"${item.price:,.0f}",
            status
        )
    
    console.print(table)
    console.print("\n[dim]Nota: ✔ = Activo, ✖ = Inactivo[/dim]")
    Prompt.ask("\nPresione Enter para continuar...")
        
def display_food_category(console: Console, food_controller, category: str):
    """Muestra ítems de una categoría específica con diseño mejorado"""
    console.clear()
    items = food_controller.get_items_by_category(category)
    
    if not items:
        console.print(Panel.fit(f"No hay ítems en la categoría {category}", style="bold yellow"))
        Prompt.ask("\nPresione Enter para continuar...")
        return
    
    # Configuración de estilos por categoría
    category_styles = {
        "Combo": ("bold green", "🍟 COMBOS ESPECIALES 🥤", "📦"),
        "Snack": ("bold orange3", "🍿 SNACKS Y APERITIVOS", "🍿"),
        "Drink": ("bold dodger_blue1", "🥤 BEBIDAS REFRESCANTES", "🥤"),
        "Candy": ("bold purple4", "🍫 DULCES Y GOLOSINAS", "🍬")
    }
    
    style, title, emoji = category_styles.get(category, ("bold", f"MENÚ DE {category.upper()}", "🍽️"))
    
    console.print(Panel.fit(title, style=style))
    console.print("")
    
    for item in items:
        # Descripción detallada según categoría
        if category == "Combo":
            desc = f"Incluye: {', '.join(item.included_items)}"
            extra = f"[dim](Ahorras ${sum(15000 for _ in item.included_items)-item.price:,.0f})[/dim]"
        elif category == "Snack":
            desc = f"Tamaño: {item.size} | Crujiente y delicioso"
            extra = ""
        elif category == "Drink":
            desc = f"Tamaño: {item.size} | Refrescante"
            extra = "[dim](Recarga gratis)[/dim]" if "Mediano" in item.size else ""
        elif category == "Candy":
            desc = "Dulce individual | Perfecto para compartir"
            extra = "[dim](2x1 los miércoles)[/dim]"
        
        # Verificar si el ítem está activo
        item_style = None if item.status == 'active' else "dim"
        border_style = style if item.status == 'active' else "red"
        
        # Panel para cada ítem
        console.print(Panel.fit(
            f"{emoji} [bold]{item.product}[/bold]\n"
            f"{desc}\n"
            f"[bold green]${item.price:,.0f}[/bold green] {extra}",
            style=item_style,
            border_style=border_style
        ))
        console.print("")
    
    Prompt.ask("\nPresione Enter para continuar...")