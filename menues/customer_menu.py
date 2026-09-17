from utils.messages import show_error
from handlers import event_handlers, venue_handlers, order_handlers

def show_customer_menu(user):
    while True:
        print("\n==========================================================\n")
        print("EVENTPASS".center(58))
        print(f"Bienvenido/a {user['username']}".center(58))
        print("\n==========================================================")
        print("1. Ver cartelera de eventos activos")
        print("2. Ver detalle de un evento")
        print("3. Comprar entradas")
        print("4. Ver mis entradas")
        #print("3. Buscar evento por nombre")
        #print("4. Buscar eventos por categoria")
        # print("7. Cancelar una orden de compra")
        # print("8. Ver eventos recomendados")
        # print("0. Cerrar sesión")
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
                order_handlers.buy_tickets(user)
            case "4":
                order_handlers.show_user_orders(user)
            case "5":
                pass  # event_handler.buy_tickets()
            case "6":
                pass  # event_handler.view_my_orders()
            case "7":
                pass  # event_handler.cancel_order()
            case "8":
                pass  # event_handler.view_recommended_events()
            case "0":
                break
            case _:
                show_error("Opción inválida, elija una opción existente.")