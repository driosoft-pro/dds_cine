from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from typing import Optional

from models.user import User, Admin, Client


def display_user_management(console: Console, user_controller, current_user):
    """Menú principal de gestión de usuarios"""
    is_admin = isinstance(current_user, Admin)

    while True:
        console.clear()
        console.print(Panel.fit("GESTIÓN DE USUARIOS", style="bold blue"))

        if is_admin:
            console.print("\n1. Listar todos los usuarios")
            console.print("2. Buscar usuario")
            console.print("3. Crear nuevo usuario")
            console.print("4. Editar usuario")
            console.print("5. Cambiar estado de usuario")
            console.print("6. Volver\n")
            
            option = Prompt.ask("Seleccione una opción", choices=["1", "2", "3", "4", "5", "6"])
            
            if option == "1":
                display_all_users(console, user_controller, is_admin=True)
            elif option == "2":
                handle_search_user(console, user_controller)
            elif option == "3":
                handle_create_user(console, user_controller)
            elif option == "4":
                handle_edit_user(console, user_controller, current_user.user_id)
            elif option == "5":
                handle_change_status(console, user_controller, current_user.user_id)
            elif option == "6":
                return
            else:
                console.print("\n[bold yellow]Opción en desarrollo...[/bold yellow]")
                Prompt.ask("\nPresione Enter para continuar...")
        else:
            console.print("\n1. Ver mi perfil")
            console.print("2. Editar mis datos")
            console.print("3. Cambiar mi contraseña")
            console.print("4. Volver\n")
            
            option = Prompt.ask("Seleccione una opción", choices=["1", "2", "3", "4"])
            
            if option == "1":
                display_user_profile(console, current_user)
            elif option == "2":
                handle_edit_user(console, user_controller, current_user.user_id)
            elif option == "3":
                handle_change_password(console, user_controller, current_user.user_id)
            elif option == "4":
                return

def display_all_users(console: Console, user_controller, is_admin: bool):
    """Muestra todos los usuarios"""
    console.clear()
    users = user_controller.get_all_users()
    
    table = Table(title="👥 LISTA DE USUARIOS", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=4)
    table.add_column("Usuario", width=15)
    table.add_column("Nombre", width=20)
    table.add_column("Email", width=25)
    table.add_column("Tipo", width=10)
    table.add_column("Estado", width=10)
    
    for user in users:
        user_type = "Admin" if isinstance(user, Admin) else "Cliente"
        status = "[green]Activo[/green]" if user.status == 'active' else "[red]Inactivo[/red]"
        
        table.add_row(
            str(user.user_id),
            user.username,
            user.name,
            user.email,
            user_type,
            status
        )
    
    console.print(table)
    Prompt.ask("\nPresione Enter para continuar...")

def display_user_profile(console: Console, user: User):
    """Muestra el perfil de un usuario"""
    console.clear()
    
    user_type = "Administrador" if isinstance(user, Admin) else "Cliente"
    age = user.get_age()
    status = "[green]Activo[/green]" if user.status == 'active' else "[red]Inactivo[/red]"
    
    profile = Table(show_header=False, box=None)
    profile.add_column("Campo", style="bold", width=15)
    profile.add_column("Valor", width=40)
    
    profile.add_row("Usuario:", user.username)
    profile.add_row("Nombre:", user.name)
    profile.add_row("Identificación:", user.identification)
    profile.add_row("Email:", user.email)
    profile.add_row("Fecha Nacimiento:", f"{user.birth_date} ({age} años)")
    profile.add_row("Tipo:", user_type)
    profile.add_row("Estado:", status)
    
    console.print(Panel.fit(profile, title="👤 PERFIL DE USUARIO"))
    Prompt.ask("\nPresione Enter para continuar...")

def handle_create_user(console: Console, user_controller):
    """Maneja la creación de nuevos usuarios"""
    console.clear()
    console.print(Panel.fit("CREAR NUEVO USUARIO", style="bold green"))
    
    user_data = {}
    
    # Tipo de usuario
    user_type = Prompt.ask("Tipo de usuario", choices=["admin", "client"], default="client")
    
    # Datos comunes
    while True:
        username = Prompt.ask("Nombre de usuario")
        if not user_controller.get_user_by_username(username):
            break
        console.print("[red]Este nombre de usuario ya está en uso[/red]")
    
    user_data['username'] = username
    
    # Resto de campos con validación
    user_data['identification'] = Prompt.ask("Identificación (cédula/pasaporte)")
    user_data['name'] = Prompt.ask("Nombre completo")
    
    while True:
        email = Prompt.ask("Email")
        if User.validate_email(email):
            user_data['email'] = email
            break
        console.print("[red]Email inválido[/red]")
    
    while True:
        birth_date = Prompt.ask("Fecha nacimiento (YYYY-MM-DD)", default="2000-01-01")
        if User.validate_birth_date(birth_date):
            user_data['birth_date'] = birth_date
            break
        console.print("[red]Fecha inválida. Use formato YYYY-MM-DD[/red]")
    
    while True:
        password = Prompt.ask("Contraseña", password=True)
        if User.validate_password(password):
            user_data['password'] = password
            break
        console.print("[red]La contraseña debe tener al menos 6 caracteres[/red]")
    
    # Crear usuario
    user = user_controller.create_user(user_data, user_type)
    if user:
        console.print(f"\n[green]Usuario {user.username} creado exitosamente![/green]")
    else:
        console.print("\n[red]Error al crear el usuario[/red]")
    
    Prompt.ask("\nPresione Enter para continuar...")

def handle_edit_user(console: Console, user_controller, user_id: int):
    """Maneja la edición de un usuario"""
    console.clear()
    console.print(Panel.fit("EDITAR USUARIO", style="bold yellow"))
    
    user = user_controller.get_user(user_id)
    if not user:
        console.print("[red]Usuario no encontrado[/red]")
        Prompt.ask("\nPresione Enter para continuar...")
        return
    
    # Mostrar datos actuales
    display_user_profile(console, user)
    
    # Preguntar qué campos editar
    fields_to_edit = ["username", "name", "identification", "email", "birth_date"]
    edited_fields = {}
    
    for field in fields_to_edit:
        if Confirm.ask(f"¿Desea editar el campo {field}?"):
            new_value = Prompt.ask(f"Nuevo valor para {field}", default=getattr(user, field))
            edited_fields[field] = new_value
    
    # Actualizar usuario
    if edited_fields:
        user_controller.update_user(user_id, **edited_fields)
        console.print("\n[green]Usuario actualizado exitosamente![/green]")
    else:
        console.print("\n[red]No se realizaron cambios[/red]")
    
    Prompt.ask("\nPresione Enter para continuar...")    
    
def handle_change_password(console: Console, user_controller, user_id: int):
    """Permite al usuario cambiar su contraseña"""
    console.clear()
    console.print(Panel.fit("🔐 CAMBIAR CONTRASEÑA", style="bold red"))

    user = user_controller.get_user(user_id)
    if not user:
        console.print("[red]Usuario no encontrado[/red]")
        Prompt.ask("\nPresione Enter para continuar...")
        return

    current_password = Prompt.ask("Ingrese su contraseña actual", password=True)
    
    # Verifica que la contraseña actual coincida
    if not user.change_password(current_password):
        console.print("[red]Contraseña incorrecta[/red]")
        Prompt.ask("\nPresione Enter para continuar...")
        return

    # Solicita y valida la nueva contraseña
    while True:
        new_password = Prompt.ask("Ingrese nueva contraseña", password=True)
        confirm_password = Prompt.ask("Confirme nueva contraseña", password=True)

        if new_password != confirm_password:
            console.print("[red]Las contraseñas no coinciden[/red]")
            continue

        if not User.validate_password(new_password):
            console.print("[red]La contraseña debe tener al menos 6 caracteres[/red]")
            continue

        break

    # Actualiza la contraseña
    success = user_controller.update_password(user_id, new_password)
    if success:
        console.print("[green]¡Contraseña actualizada exitosamente![/green]")
    else:
        console.print("[red]Ocurrió un error al actualizar la contraseña[/red]")

    Prompt.ask("\nPresione Enter para continuar...")
    
def handle_search_user(console: Console, user_controller):
    """Permite buscar un usuario por username, email o identificación"""
    console.clear()
    console.print(Panel.fit("🔍 BUSCAR USUARIO", style="bold cyan"))

    search_term = Prompt.ask("Ingrese nombre de usuario, email o identificación a buscar")

    user = user_controller.search_user(search_term)

    if not user:
        console.print(f"[red]No se encontró ningún usuario con el término: {search_term}[/red]")
    else:
        display_user_profile(console, user)

    Prompt.ask("\nPresione Enter para continuar...")
    
def handle_change_status(console: Console, user_controller, user_id: int):
    """Permite cambiar el estado de un usuario"""
    console.clear()
    console.print(Panel.fit("⚙️ CAMBIAR ESTADO DE USUARIO", style="bold magenta"))

    user = user_controller.get_user(user_id)
    if not user:
        console.print("[red]Usuario no encontrado[/red]")
        Prompt.ask("\nPresione Enter para continuar...")
        return

    new_status = Prompt.ask("Ingrese nuevo estado (active/inactive)", choices=["active", "inactive"], default=user.status)

    # Actualiza el estado
    success = user_controller.update_status(user_id, new_status)
    if success:
        console.print("[green]¡Estado actualizado exitosamente![/green]")
    else:
        console.print("[red]Ocurrió un error al actualizar el estado[/red]")

    Prompt.ask("\nPresione Enter para continuar...")