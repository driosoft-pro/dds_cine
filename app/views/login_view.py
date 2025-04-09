from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from typing import Optional
from datetime import datetime

from models.user import User
from views.menu import display_main_menu

def display_login(console: Console, auth_service):
    """
    Muestra el menú de login y maneja la autenticación del usuario.
    """
    while True:
        console.clear()
        console.print(Panel.fit("SISTEMA DE VENTA DE ENTRADAS - CINEMA", 
                                style="bold blue"))
        
        console.print("\n1. Iniciar sesión")
        console.print("2. Registrarse como cliente")
        console.print("3. Salir\n")
        
        option = Prompt.ask("Seleccione una opción", choices=["1", "2", "3"])
        
        if option == "1":
            user = handle_login(console, auth_service)
            if user:
                display_main_menu(console, auth_service, user)
        elif option == "2":
            handle_register(console, auth_service)
        elif option == "3":
            console.print("\n¡Gracias por usar nuestro sistema!")
            return

def handle_login(console: Console, auth_service) -> Optional[User]:
    """
    Maneja el proceso de login de un usuario.
    """
    console.clear()
    console.print(Panel.fit("INICIAR SESIÓN", style="bold green"))
    
    while True:
        username = Prompt.ask("Ingrese su nombre de usuario")
        if not User.validate_username(username):
            console.print("[red]Error: Usuario inválido (4-20 caracteres alfanuméricos)[/red]")
            continue
        break
    
    password = Prompt.ask("Ingrese su contraseña", password=True)
    
    user = auth_service.authenticate(username, password)
    
    if user:
        console.print(f"\n[bold green]¡Bienvenido, {user.name}![/bold green]")
        return user
    else:
        console.print("\n[bold red]Error: Usuario o contraseña incorrecta[/bold red]")
        return None

def handle_register(console: Console, auth_service):
    """
    Maneja el proceso de registro de un nuevo cliente.
    """
    console.clear()
    console.print(Panel.fit("REGISTRO DE NUEVO CLIENTE", style="bold green"))
    
    user_data = {}
    
    # Validación de username
    while True:
        username = Prompt.ask("Ingrese un nombre de usuario (3-20 caracteres alfanuméricos)")
        if not User.validate_username(username):
            console.print("[bold red]Error: Usuario inválido (3-20 caracteres alfanuméricos)[/bold red]")
            continue
        if auth_service.user_controller.get_user_by_username(username):
            console.print("[bold red]Error: Este nombre de usuario ya está en uso[/bold red]")
            continue
        user_data['username'] = username
        break
    
    # Validación de identificación
    while True:
        identification = Prompt.ask("Ingrese su identificación (cédula, pasaporte, etc.)")
        if not User.get_user_by_identification(identification):
            console.print("[bold red]Error: Identificación inválida (5-20 caracteres)[/bold red]")
            continue
        if auth_service.user_controller.get_user_by_identification(identification):
            console.print("[bold red]Error: Esta identificación ya está registrada[/bold red]")
            continue
        user_data['identification'] = identification
        break
    
    # Validación de nombre
    while True:
        name = Prompt.ask("Ingrese su nombre completo")
        if not User.validate_name(name):
            console.print("[bold red]Error: Nombre debe tener al menos 3 caracteres[/bold red]")
            continue
        user_data['name'] = name
        break
    
    # Validación de email
    while True:
        email = Prompt.ask("Ingrese su correo electrónico")
        if not User.validate_email(email):
            console.print("[bold red]Error: Formato de email inválido[/bold red]")
            continue
        user_data['email'] = email
        break
    
    # Validación de fecha de nacimiento
    while True:
        birth_date = Prompt.ask("Ingrese su fecha de nacimiento (YYYY-MM-DD)")
        try:
            datetime.strptime(birth_date, "%Y-%m-%d")
            user_data['birth_date'] = birth_date
            break
        except ValueError:
            console.print("[bold red]Error: Formato de fecha inválido (YYYY-MM-DD)[/bold red]")
    
    # Validación de contraseña
    while True:
        password = Prompt.ask("Ingrese una contraseña (mínimo 6 caracteres)", password=True)
        if not User.validate_password(password):
            console.print("[bold red]Error: La contraseña debe tener al menos 6 caracteres[/bold red]")
            continue
        
        confirm_password = Prompt.ask("Confirme su contraseña", password=True)
        if password != confirm_password:
            console.print("[bold red]Error: Las contraseñas no coinciden[/bold red]")
            continue
        
        user_data['password'] = password
        break
    
    user = auth_service.register(user_data, 'client')
    
    if user:
        console.print(f"\n[bold green]¡Registro exitoso, {user.name}![/bold green]")
        console.print(f"Su nombre de usuario es: [bold]{user.username}[/bold]")
        console.print("Ahora puede iniciar sesión con sus credenciales.")
    else:
        console.print("\n[bold red]Error: No se pudo completar el registro. Verifique los datos.[/bold red]")
    
    Prompt.ask("\nPresione Enter para continuar...")