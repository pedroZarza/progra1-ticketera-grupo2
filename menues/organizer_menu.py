from utils.messages import show_error
from handlers import event_handlers

def show_organizer_menu(user):
    """Muestra el menú del organizador y ejecuta la opción elegida.

    Parámetros:
        user (dict): organizador autenticado.
    """
    while True:
        print("\n==========================================================\n")
        print("EVENTPASS - ORGANIZER PANEL".center(58))
        print(f"Usuario: {user['username']}".center(58))
        print("\n==========================================================")
        print("1. Crear evento")
        print("2. Ver mis eventos publicados")
        print("3. Ver detalle de un evento publicado")
        print("4. Definir precios por sector")
        print("5. Editar información de un evento")
        print("6. Asignar categoría a un evento")
        print("7. Eliminar categoría de un evento")
        print("8. Cancelar evento")
        print("9. Ver órdenes activas de un evento")
        print("10. Ver resumen de ventas y disponibilidad de un evento")
        print("11. Ver historial de eventos publicados")
        print("12. Generar reporte de ventas de un evento")
        print("0. Cerrar sesión")    
        print("----------------------------------------------------------")
        option = input(">>> ")
        
        if option.lower() in ("0", "x", "exit", "q", "-1"):
            break

        match option:
            case "1":
                event_handlers.create_new_event(user)
            case "2":
                event_handlers.view_my_events(user)
            case "3":
                event_handlers.show_organizer_event_detail(user)
            case "4":
                event_handlers.edit_event_prices(user)
            case "5":
                event_handlers.edit_event_info(user)
            case "6":
                event_handlers.assign_event_category(user)
            case "7":
                event_handlers.remove_event_category(user)
            case "8":
                event_handlers.cancel_event(user)
            case "9":
                event_handlers.view_event_orders(user)
            case "10":
                event_handlers.view_event_sales_summary(user)
            case "11":
                event_handlers.view_event_history(user)
            case "12":
                event_handlers.generate_sales_report(user)
            case "0":
                break
            case _:
                show_error("Opción inválida, elija una opción existente.")
                input("\nPresiona ENTER para volver al menú...")