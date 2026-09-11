from handlers import user_handlers
from menues.organizer_menu import show_organizer_menu
from menues.customer_menu import show_customer_menu
from menues.admin_menu import show_admin_menu


def main():  
    while True:
        print("\n==========================================================")
        print("                        EVENTPASS")
        print("              Gestión de Eventos y Tickets")
        print("==========================================================")
        print("1. Ver cartelera de eventos")
        print("2. Iniciar sesión")
        print("\n\n¿Todavía no tienes cuenta?\n")
        print("3. Registrarse para comprar tickets o publicar tus eventos")
        print("\n\n0. Salir")
        print("----------------------------------------------------------")
        option = input(">>> ")
        
        
        if option.lower() in ("0", "x", "exit", "q", "-1"):
            break
        # if option == "0" or option.lower() == "x" or option == "exit" or option == "q" or option == "-1":
        #     break

        match option:
            case "1":
                pass
            case "2":
                user = user_handlers.login()
                if user != None:
                    redirect_by_user_role(user)
            case "3":
                user_handlers.register_user()
            case _:
                print("Opción incorrecta, elija una opción existente.")
                # input("\nPresiona ENTER para continuar...")
            
                
def redirect_by_user_role(user):
    match user["role"]:
        case "admin":
            show_admin_menu(user)
        case "organizer":
            show_organizer_menu(user)
        case "customer":
            show_customer_menu(user)
main()