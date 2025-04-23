from handlers.handle_movie_management import handle_movie_management
from handlers.handle_movie_listing import handle_movie_listing
from handlers.handle_user_management import handle_user_management
from handlers.handle_ticket_purchase import handle_ticket_purchase
from handlers.handle_reservation import handle_reservation
from handlers.handle_user_tickets import handle_user_tickets
from handlers.handle_food_management import handle_food_management
from handlers.handle_food_menu import handle_food_menu
from handlers.handle_reports import handle_reports
from handlers.handle_availability import handle_availability


def handle_main_menu(app):
    """Despacha a cada sub-handler según la opción elegida."""
    while True:
        app.menu_view.show_title()
        app.menu_view.show_main_menu(app.is_admin)
        opts = ("1","2","3","4","5","6","0") if not app.is_admin else ("1","2","3","4","5","0")
        choice = app.menu_view.get_user_choice(opts)

        if choice == "0":
            app.auth_service.logout()
            break
        mapping = {
            '1': handle_movie_management if app.is_admin else handle_movie_listing,
            '2': handle_user_management  if app.is_admin else handle_ticket_purchase,
            '3': handle_food_management  if app.is_admin else handle_reservation,
            '4': handle_reports          if app.is_admin else handle_user_tickets,
            '5': handle_availability     if app.is_admin else handle_food_menu,
            '6': handle_availability
        }
        fn = mapping.get(choice)
        if fn:
            fn(app)