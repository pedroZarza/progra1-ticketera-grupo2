from utils.messages import show_error
from handlers import category_handlers
from handlers import venue_handlers

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
        print("5. Eliminar categoría de evento")
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
                category_handlers.create_category()
            case "3":
                venue_handlers.show_venues()
            case "4":
                venue_handlers.edit_venue()
            case "5":
                 category_handlers.delete_category()
            case "6":
               venue_handlers.deactivate_venue()
            case "7":
                venue_handlers.delete_venue()
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
                
                