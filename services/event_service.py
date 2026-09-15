from data.events_data import events 
from datetime import datetime

def read_all_events():
    events.sort(key=lambda event: event["datetime"])
    return events