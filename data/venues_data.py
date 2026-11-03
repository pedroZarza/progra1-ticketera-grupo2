venues = [
    {
        "id": 1,
        "name": "Movistar Arena",
        "address": "Av. Figueroa Alcorta 7597",
        "active": True,
        "time_slots": ["19:00", "21:30"],
        "sectors": {
            "Campo": {"type": "general", "capacity": 200},
            "Platea": {"type": "numbered", "rows": 5, "columns": 8},
        },
    },
    {
        "id": 2,
        "name": "Estadio Obras",
        "address": "Sin especificar",
        "active": True,
        "time_slots": ["19:30"],
        "sectors": {
            "Campo": {"type": "general", "capacity": 300},
            "Platea": {"type": "numbered", "rows": 2, "columns": 3},
        },
    },
    {
        "id": 3,
        "name": "Teatro Gran Rex",
        "address": "Sin especificar",
        "active": True,
        "time_slots": ["20:00"],
        "sectors": {
            "Campo": {"type": "general", "capacity": 100},
            "Platea": {"type": "numbered", "rows": 2, "columns": 3},
        },
    },
    {
        "id": 4,
        "name": "Centro de Convenciones",
        "address": "Sin especificar",
        "active": True,
        "time_slots": ["10:00"],
        "sectors": {
            "General": {"type": "general", "capacity": 500},
            "VIP": {"type": "general", "capacity": 50},
        },
    }
]