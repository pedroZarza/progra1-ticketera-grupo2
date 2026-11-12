from utils.messages import show_error
from handlers import category_handlers, venue_handlers, user_handlers

def show_admin_menu(user):
    """Muestra el menú del administrador y ejecuta la opción elegida.

    Parámetros:
        user (dict): usuario autenticado.
    """
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
        print("10. Inactivar venue")
        print("11. Activar venue")
        print("12. Eliminar venue")
        print("13. Dar de alta un usuario (organizador o comprador)")           
        print("14. Inactivar un usuario")
        print("15. Activar un usuario")
        print("16. Restablecer contraseña de un usuario")
        print("0. Cerrar sesión")  
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
                venue_handlers.deactivate_venue()
            case "11":
                venue_handlers.activate_venue()
            case "12":
                venue_handlers.delete_venue()
            case "13":
                user_handlers.register_user()
            case "14":
                user_handlers.deactivate_user()
            case "15":
                user_handlers.activate_user()
            case "16":
                user_handlers.reset_password()
            case "0":
                break
            case _:
                show_error("Opción inválida, elija una opción existente.")
                input("\nPresiona ENTER para volver al menú...")
                