from datetime import datetime

from utils.messages import show_info, show_error, show_success, show_warning


def events_board(events):
    print("\n==========================================================")
    print("                    CARTELERA - EVENTPASS")
    print("==========================================================")
    if len(events) == 0:
        show_info("No hay eventos disponibles en este momento.")
        return    
    for event in events:
        datetimeObj = datetime.fromisoformat(event["datetime"])
        date = datetimeObj.strftime("%d-%m-%Y")
        time = datetimeObj.strftime("%H:%M")
        print(f"\n[{event['id']}] {event['name']}")
        print(f"    📅 {date} | 🕒 {time} | 📍 {event['venue']} | 🎭 {", ".join(event["categories"])}\n")
     
    