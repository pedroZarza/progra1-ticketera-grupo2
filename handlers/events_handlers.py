from services import event_service as service
from utils import layout_helpers

def show_events():
    events = service.read_all_events()
    layout_helpers.events_board(events)
    input("\nPresiona ENTER para volver al menú principal...")
    return
    
    
    
    
    
    

