from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

class PaymentView:
    """Vista para gestión de pagos."""
    
    def __init__(self):
        self.console = Console()
    
    def show_payment_summary(self, payment: dict):
        """Muestra un resumen del pago realizado."""
        # Formatear la fecha si es necesario
        payment_date = payment.get('payment_date', 'Fecha no disponible')
        if isinstance(payment_date, str) and 'T' in payment_date:
            payment_date = payment_date.replace('T', ' ')
        
        panel = Panel.fit(
            f"[bold]Comprobante de Pago[/]\n\n"
            f"ID de Transacción: [cyan]{payment['payment_id']}[/]\n"
            f"Fecha: [white]{payment_date}[/]\n"  # Usar la fecha formateada
            f"Método: [blue]{payment['payment_method']}[/]\n"
            f"Monto: [green]${payment['amount']:,.0f}[/]\n"
            f"Estado: [green]Confirmado[/]",
            border_style="green"
        )
        self.console.print(panel)
    
    def show_change(self, amount: float, change: float):
        """Muestra el cambio a devolver en pagos en efectivo."""
        if change > 0:
            panel = Panel.fit(
                f"[bold]Cambio a devolver[/]\n\n"
                f"Monto recibido: [green]${amount:,.0f}[/]\n"
                f"Total a pagar: [yellow]${(amount - change):,.0f}[/]\n"
                f"Cambio: [green]${change:,.0f}[/]",
                border_style="yellow"
            )
            self.console.print(panel)
    
    def show_payments(self, payments: list):
        """Muestra una lista de pagos."""
        if not payments:
            self.console.print("[yellow]No se encontraron registros de pago.[/]")
            return
        
        table = Table(title="[bold]Historial de Pagos[/]", box=box.ROUNDED)
        table.add_column("ID", style="cyan")
        table.add_column("Fecha", style="white")
        table.add_column("Método", style="blue")
        table.add_column("Monto", style="green")
        table.add_column("Estado", style="red")
        
        for payment in payments:
            status = "Activo" if payment['status'] == 'activo' else "Cancelado"
            table.add_row(
                str(payment['payment_id']),
                payment['payment_date'],
                payment['payment_method'],
                f"${payment['amount']:,.0f}",
                status
            )
        
        self.console.print(table)