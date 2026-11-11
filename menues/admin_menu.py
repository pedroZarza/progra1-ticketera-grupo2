from utils.messages import show_error
from handlers import category_handlers, venue_handlers, user_handlers

def show_admin_menu(user):
    while True:
        print("\n==========================================================\n")
        print("EVENTPASS - ADMIN PANEL".center(58))
        print(f"Usuario: {user['username']}".center(58))
        print("\n==========================================================")
        print("1. Dar de alta un venue")
        print("2. Consultar venues disponibles")
        print("3. Consultar detalle de un venue")
        print("4. Agregar nueva categoría")
        print("5. Eliminar categoría existente")
        print("6. Consultar categorías")
        print("7. Editar información de un venue")
        print("8. Agregar/eliminar time slots de un venue")
        print("9. Editar configuración de sectores de un venue")
        print("8. Inactivar venue")
        print("9. Eliminar venue")
        #print("8. Consultar estadísticas por venue")
        print("11. Dar de alta un usuario (organizador o comprador)")
        #print("9. Consultar calendario de venues")
        print("0. Cerrar sesión")  
        # print("8. Gestionar usuarios (consultar / inactivar / restablecer contraseña)")
        # print("9. Gestionar eventos (consultar / deshabilitar / eliminar / historial)")
        # print("10. Consultar estadísticas generales de la plataforma")
        print("----------------------------------------------------------")
        option = input(">>> ")
        
        if option.lower() in ("0", "x", "exit", "q", "-1"):
            break  
        
        match option:
            case "1":
               venue_handlers.create_venue()
            case "2":
               venue_handlers.show_venues()
            case "3":
                venue_handlers.show_venue_detail()
            case "4":
                category_handlers.create_category()
            case "5":
                category_handlers.delete_category()
            case "6":
                category_handlers.show_categories()
            case "7":
                venue_handlers.edit_venue_info()
            case "8":
                venue_handlers.edit_venue_time_slots()
            case "9":
                venue_handlers.edit_venue_sectors()
            case "10":
                pass  # event_handler.manage_events()
            case "11":
                user_handlers.register_user()
            case "0":
                break
            case _:
                show_error("Opción inválida, elija una opción existente.")
                
                