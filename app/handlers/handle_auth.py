from rich.panel import Panel
from rich.table import Table
from rich import box
from rich.prompt import Prompt

def handle_auth(app):
    """Maneja el proceso de autenticación."""
    app.menu_view.show_welcome()
    app.console.print(Panel.fit("[bold]Inicio de Sesión[/]", border_style="blue"))

    # Opciones de auth
    table = Table(box=box.ROUNDED, border_style="blue")
    table.add_column("ID", style="cyan")
    table.add_column("Opción", style="magenta")
    table.add_row("1", "Iniciar sesión")
    table.add_row("2", "Registrarse")
    table.add_row("0", "Salir")
    app.console.print(table)

    # Lógica de selección
    while True:
        choice = Prompt.ask("Seleccione [0/1/2]").strip()
        if choice in ["0","1","2"]:
            break
        app.console.print("[red]Opción inválida[/]")

    if choice == "1":
        username, password = app.login_view.show_login()
        if username in (None, "volver") or password in (None, "volver"):
            app.menu_view.show_message("Acción cancelada.")
            return
        user = app.auth_service.login(username, password)
        if user:
            msg = f"Bienvenido, {'Administrador ' if user['is_admin'] else ''}{user['name']}!"
            app.console.print(f"[green]{msg}[/]")
            app.current_user = user
            app.is_admin = user['is_admin']
        else:
            app.login_view.show_login_error()
            app.menu_view.press_enter_to_continue()

    elif choice == "2":
        data = app.login_view.show_register()
        if not data or any(v=='volver' for v in data.values()):
            app.menu_view.show_message("Registro cancelado.")
            return
        valid, msg = app.validation_service.validate_email(data['email'])
        if not valid:
            app.menu_view.show_message(msg, is_error=True)
            return
        valid, msg, date = app.validation_service.validate_date(data['birth_date'])
        if not valid:
            app.menu_view.show_message(msg, is_error=True)
            return
        if data['password'] != data['confirm_password']:
            app.menu_view.show_message("Contraseñas no coinciden", is_error=True)
            return
        try:
            app.auth_service.register_user(
                username=data['username'], identification=data['identification'],
                name=data['name'], email=data['email'], birth_date=date,
                password=data['password']
            )
            app.login_view.show_register_success()
        except ValueError as e:
            app.menu_view.show_message(str(e), is_error=True)
        app.menu_view.press_enter_to_continue()

    else:
        app.console.print("[yellow]Saliendo...[/]")
        sys.exit(0)