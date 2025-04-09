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
            elif option == "2":
                handle_edit_food_item(console, food_controller)
            elif option == "3":
                handle_change_item_status(console, food_controller)
            elif option == "4":
                display_all_food_items(console, food_controller, is_admin)
            elif option == "5":
                handle_search_food_items(console, food_controller)
            elif option == "6":
                return
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


def handle_edit_food_item(console: Console, food_controller):
    """Maneja la edición de un ítem del menú"""
    console.clear()
    console.print(Panel.fit("EDITAR ÍTEM DEL MENÚ", style="bold yellow"))
    
    try:
        item_id = int(Prompt.ask("Ingrese el ID del ítem a editar"))
        item = food_controller.db.get_food_item(item_id)
        
        if not item:
            console.print("[red]Ítem no encontrado.[/red]")
            Prompt.ask("\nPresione Enter para continuar...")
            return
        
        console.print(f"\nEditando ítem: [bold]{item.product}[/bold]")
        update_data = {}
        
        # Solicitar datos a actualizar
        if Confirm.ask("¿Desea actualizar el nombre del producto?"):
            update_data['product'] = Prompt.ask("Nuevo nombre del producto")
        if Confirm.ask("¿Desea actualizar el tamaño?"):
            update_data['size'] = Prompt.ask("Nuevo tamaño (Pequeño/Mediano/Grande/Familiar)")
        if Confirm.ask("¿Desea actualizar el precio?"):
            update_data['price'] = float(Prompt.ask("Nuevo precio"))
        
        # Actualizar el ítem
        updated = food_controller.update_item(item_id, update_data)
        if updated:
            console.print("[green]Ítem actualizado exitosamente.[/green]")
        else:
            console.print("[red]Error al actualizar el ítem.[/red]")
    except ValueError:
        console.print("[red]Error: ID inválido.[/red]")
    
    Prompt.ask("\nPresione Enter para continuar...")


def handle_change_item_status(console: Console, food_controller):
    """Maneja el cambio de estado de un ítem del menú"""
    console.clear()
    console.print(Panel.fit("CAMBIAR ESTADO DE ÍTEM", style="bold cyan"))
    
    try:
        item_id = int(Prompt.ask("Ingrese el ID del ítem a cambiar estado"))
        item = food_controller.db.get_food_item(item_id)
        
        if not item:
            console.print("[red]Ítem no encontrado.[/red]")
            Prompt.ask("\nPresione Enter para continuar...")
            return
        
        console.print(f"\nCambiando estado del ítem: [bold]{item.product}[/bold]")
        new_status = Prompt.ask("Nuevo estado (active/inactive)", choices=["active", "inactive"])
        
        # Cambiar el estado
        status_changed = food_controller.change_item_status(item_id, new_status)
        if status_changed:
            console.print("[green]Estado del ítem cambiado exitosamente.[/green]")
        else:
            console.print("[red]Error al cambiar el estado del ítem.[/red]")
    except ValueError:
        console.print("[red]Error: ID inválido.[/red]")
    
    Prompt.ask("\nPresione Enter para continuar...")


def handle_search_food_items(console: Console, food_controller):
    """Maneja la búsqueda de ítems en el menú"""
    console.clear()
    console.print(Panel.fit("BUSCAR ÍTEMS EN EL MENÚ", style="bold magenta"))
    
    console.print("\n[bold]Criterios de búsqueda:[/bold]")
    console.print("1. Por categoría")
    console.print("2. Por estado (active/inactive)")
    console.print("3. Por nombre del producto")
    console.print("4. Volver\n")
    
    option = Prompt.ask("Seleccione un criterio", choices=["1", "2", "3", "4"])
    
    if option == "4":
        return
    
    criteria = {}
    if option == "1":
        criteria['category'] = Prompt.ask("Ingrese la categoría (Combo/Snack/Drink/Candy)")
    elif option == "2":
        criteria['status'] = Prompt.ask("Ingrese el estado (active/inactive)", choices=["active", "inactive"])
    elif option == "3":
        criteria['product'] = Prompt.ask("Ingrese el nombre del producto")
    
    # Buscar ítems
    results = food_controller.search_items(**criteria)
    if not results:
        console.print("[yellow]No se encontraron ítems que coincidan con los criterios.[/yellow]")
    else:
        table = Table(title="🍿 RESULTADOS DE BÚSQUEDA", show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim", width=4)
        table.add_column("Código", width=10)
        table.add_column("Categoría", width=12)
        table.add_column("Producto", min_width=20)
        table.add_column("Tamaño", width=10)
        table.add_column("Precio", justify="right", width=10)
        table.add_column("Estado", width=8)
        
        for item in results:
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
    
    Prompt.ask("\nPresione Enter para continuar...")


def display_all_food_items(console: Console, food_controller, is_admin: bool):
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
    Prompt.ask("\nPresione Enter para continuar...")