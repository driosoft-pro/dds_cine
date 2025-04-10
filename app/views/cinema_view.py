from rich.console import Console
from rich.panel import Panel
from rich.table import Table

def display_cinema_management(console: Console, cinema_controller):
    console.clear()
    console.print(Panel.fit("🎦 GESTIÓN DE SALAS", style="bold blue"))
    
    # Mostrar estado de salas
    console.print("\n[bold]Estado de Salas:[/bold]")
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Sala")
    table.add_column("Tipo")
    table.add_column("Asientos Disponibles")
    
    for room in cinema_controller.rooms.values():
        available = len([s for s in room.seats.values() if not s.is_occupied])
        table.add_row(room.room_type.value, 
                        "2D" if room.room_type == RoomType.TWO_D else "3D",
                        f"{available}/100")
    
    console.print(table)
    Prompt.ask("\nPresione Enter para continuar...")