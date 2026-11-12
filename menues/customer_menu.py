from utils.messages import show_error
from handlers import event_handlers, order_handlers

def show_customer_menu(user):
    """Muestra el menú del comprador y ejecuta la opción elegida.

    Parámetros:
        user (dict): comprador autenticado.
    """
    while True:
        print("\n==========================================================\n")
        print("EVENTPASS".center(58))
        print(f"Bienvenido/a {user['username']}".center(58))
        print("\n==========================================================")
        print("1. Ver cartelera de eventos activos")
        print("2. Ver detalle de un evento")
        print("3. Buscar eventos")
        print("4. Filtrar eventos por categorías")
        print("5. Comprar entradas")
        print("6. Ver mis entradas")
        print("7. Cancelar una orden de compra")
        print("0. Cerrar sesión")
        print("----------------------------------------------------------")
        option = input(">>> ")

        if option.lower() in ("0", "x", "exit", "q", "-1"):
            break
        match option:
            case "1":
                event_handlers.show_events()
            case "2":
                event_handlers.show_event_detail()
            case "3":
                event_handlers.search_events()
            case "4":
                event_handlers.filter_events_by_category()
            case "5":
                order_handlers.buy_tickets(user)
            case "6":
                order_handlers.show_user_orders(user)
            case "7":
                order_handlers.cancel_order(user)
            case _:
                show_error("Opción inválida, elija una opción existente.")
                input("\nPresiona ENTER para volver al menú...")
