from handlers import event_handlers, user_handlers
from menues.organizer_menu import show_organizer_menu
from menues.customer_menu import show_customer_menu
from menues.admin_menu import show_admin_menu
from utils.messages import show_error


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
        match option:
            case "1":
                event_handlers.show_events()
            case "2":
                user = user_handlers.login()
                if user != None:
                    redirect_by_user_role(user)
            case "3":
                user = user_handlers.register_user()
                if user != None:
                    redirect_by_user_role(user) #loguea automáticamente luego del registro. 
            case _:
                show_error("Opción incorrecta, elija una opción existente.")
            
                
def redirect_by_user_role(user):
    match user["role"]:
        case "admin":
            show_admin_menu(user)
        case "organizer":
            show_organizer_menu(user)
        case "customer":
            show_customer_menu(user)
main()