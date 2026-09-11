
def show_organizer_menu(user):
    while True:
        print("\n==========================================================\n")
        print("EVENTPASS - ORGANIZER PANEL".center(58))
        print(f"Usuario: {user['username']}".center(58))
        print("\n==========================================================")
        print("1. Crear evento")
        print("2. Ver mis eventos (buscar por nombre / filtrar por categoría)")
        print("3. Definir precios por sector")
        print("4. Modificar evento")
        print("5. Asignar categorías al evento")
        print("6. Cancelar evento")
        print("7. Posponer evento")
        print("8. Habilitar / deshabilitar venta de tickets")
        print("9. Ver estado de ventas y disponibilidad")
        print("10. Ver detalle de órdenes de compra de un evento")
        print("11. Ver mis estadísticas")
        print("12. Generar reporte de ventas por período")
        print("0. Cerrar sesión")
        print("----------------------------------------------------------")
        option = input(">>> ")
        
        
        if option == "0" or option.lower() == "x" or option == "exit" or option == "q" or option == "-1":
            break

        match option:
            case "1":
                pass  # event_handler.create_event()
            case "2":
                pass  # event_handler.view_my_events()
            case "3":
                pass  # event_handler.set_prices_by_sector()
            case "4":
                pass  # event_handler.edit_event()
            case "5":
                pass  # event_handler.assign_categories()
            case "6":
                pass  # event_handler.cancel_event()
            case "7":
                pass  # event_handler.postpone_event()
            case "8":
                pass  # event_handler.toggle_ticket_sales()
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
                print("Opción inválida, elija una opción existente.")
                
                