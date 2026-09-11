
def show_customer_menu(user):
    while True:
        print("\n==========================================================\n")
        print("EVENTPASS".center(58))
        print(f"Bienvenido/a {user['username']}".center(58))
        print("\n==========================================================")
        print("1. Ver cartelera de eventos")
        print("3. Ver detalle de un evento")
        print("3. Buscar evento por nombre")
        print("4. Buscar eventos por categoria")
        print("5. Comprar entradas (elegir sector o butaca)")
        print("6. Ver mis órdenes de compra")
        # print("7. Cancelar una orden de compra")
        # print("8. Ver eventos recomendados")
        # print("0. Cerrar sesión")
        print("----------------------------------------------------------")
        option = input(">>> ")
        
        if option == "0" or option.lower() == "x" or option == "exit" or option == "q" or option == "-1":
            break
        
        match option:
            case "1":
                pass  # event_handler.view_events()
            case "2":
                pass  # event_handler.search_events()
            case "3":
                pass  # event_handler.view_event_detail()
            case "4":
                pass  # event_handler.view_featured_events()
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
                print("Opción inválida, elija una opción existente.")