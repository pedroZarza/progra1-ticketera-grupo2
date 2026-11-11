from utils.messages import show_error
from handlers import event_handlers

def show_organizer_menu(user):
    while True:
        print("\n==========================================================\n")
        print("EVENTPASS - ORGANIZER PANEL".center(58))
        print(f"Usuario: {user['username']}".center(58))
        print("\n==========================================================")
        print("1. Crear evento")
        print("2. Ver mis eventos publicados")
        print("3. Buscar evento por nombre")
        print("4. Buscar evento por categoria")
        print("5. Definir precios por sector")
        print("6. Modificar evento")
        print("7. Asignar categoría a un evento")
        print("8. Ver estado de ventas y disponibilidad de un evento")
        print("0. Cerrar sesión")    
        # print("6. Cancelar evento")
        # print("7. Posponer evento")
        # print("8. Habilitar / deshabilitar venta de tickets")
        # print("10. Ver detalle de órdenes de compra de un evento")
        # print("11. Ver mis estadísticas")
        # print("12. Generar reporte de ventas por período")
        print("----------------------------------------------------------")
        option = input(">>> ")
        
        if option.lower() in ("0", "x", "exit", "q", "-1"):
            break

        match option:
            case "1":
                event_handlers.create_event(user)
            case "2":
                pass
            case "3":
                pass
            case "4":
                pass
            case "5":
               pass                         
            case "6":
               pass
            case "7":
                pass
            case "8":
              pass
            case "9":
                pass  # event_handler.view_sales_status()
            case "10":
                pass  # event_handler.view_order_details()
            case "11":
                pass  # event_handler.view_my_statistics()
            case "12":
                pass  # event_handler.generate_sales_report()
            case "0":
                break
            case _:
                show_error("Opción inválida, elija una opción existente.")