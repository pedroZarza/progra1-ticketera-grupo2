from utils.messages import show_error

def show_admin_menu(user):
    while True:
        print("\n==========================================================\n")
        print("EVENTPASS - ADMIN PANEL".center(58))
        print(f"Usuario: {user['username']}".center(58))
        print("\n==========================================================")
        print("1. Dar de alta un venue")
        print("2. Dar de alta nueva categoría de evento")
        print("3. Consultar venues del sistema")
        print("4. Editar un venue")
        print("6. Inactivar venue")
        print("7. Eliminar venue")
        print("8. Consultar estadísticas por venue")
        print("9. Consultar calendario de venues")
        print("0. Cerrar sesión")  
        # print("7. Dar de alta un usuario (organizador o comprador)")
        # print("8. Gestionar usuarios (consultar / inactivar / restablecer contraseña)")
        # print("9. Gestionar eventos (consultar / deshabilitar / eliminar / historial)")
        # print("10. Consultar estadísticas generales de la plataforma")
        print("----------------------------------------------------------")
        option = input(">>> ")
        
        if option.lower() in ("0", "x", "exit", "q", "-1"):
            break  
        
        match option:
            case "1":
                pass  # venue_handler.create_venue()
            case "2":
                pass  # venue_handler.manage_venues()
            case "3":
                pass  # venue_handler.manage_sectors()
            case "4":
                pass  # event_handler.manage_categories()
            case "5":
                pass  # venue_handler.view_calendar()
            case "6":
                pass  # venue_handler.view_statistics()
            case "7":
                pass  # user_handler.create_user()
            case "8":
                pass  # user_handler.manage_users()
            case "9":
                pass  # event_handler.manage_events()
            case "10":
                pass  # event_handler.view_platform_statistics()
            case "0":
                break
            case _:
                show_error("Opción inválida, elija una opción existente.")
                
                