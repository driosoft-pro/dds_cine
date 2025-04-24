from datetime import datetime

def handle_reports(app):
    """Maneja la generación de reportes (admin)."""
    rv = app.report_view
    rc = app.report_controller
    mv = app.menu_view

    while True:
        choice = rv.show_report_menu()
        if choice == "0":
            return

        # Pedimos rango de fechas
        start = rv.ask_date("Fecha inicial")
        end   = rv.ask_date("Fecha final")

        if choice == "1":
            total = rc.total_sales(start, end)
            rv.show_total_sales(total, start, end)

        elif choice == "2":
            data = rc.sales_by_movie(start, end)
            rv.show_sales_by_movie(data)

        elif choice == "3":
            data = rc.sales_by_user(start, end)
            rv.show_sales_by_user(data)

        mv.press_enter_to_continue()