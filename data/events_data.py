events = [
    {
        "id": 1,
        "name": "Noches de Rock",
        "datetime": "2026-10-15T21:00",
        "venue": "Movistar Arena",
        "venueId": 1,
        "categories": ["Música en vivo", "Rock"],
        "description": "Festival de rock con bandas nacionales invitadas.",
        "organizerId": 4,
        "status": "active",
        "sectors": {
            "Campo": {
                "price": 15000,
                "capacity": 200,
                "sold": 85
            },
            "Platea": {
                "price": 25000,
                       "seats": [
                    ["free", "free", "occupied", "free", "free", "free", "free", "free"],
                    ["free", "occupied", "free", "free", "free", "free", "free", "free"],
                    ["free", "free", "free", "free", "free", "free", "free", "free"],
                    ["free", "free", "free", "free", "free", "free", "free", "free"],
                    ["free", "free", "free", "free", "free", "free", "free", "free"]
                    ]
            }
        }
    },
    {
        "id": 2,
        "name": "Festival Indie BA",
        "datetime": "2026-09-28T19:30",
        "venue": "Estadio Obras",
        "venueId": 2,
        "categories": ["Música en vivo", "Indie"],
        "description": "Festival con artistas emergentes de la escena indie nacional.",
        "organizerId": 5,
        "status": "active",
        "sectors": {
            "Campo": {
                "price": 12000,
                "capacity": 300,
                "sold": 240
            },
            "Platea": {
                "price": 18000,
                "seats": [
                    ["occupied", "free", "free"],
                    ["occupied", "occupied", "free"]
                ]
            }
        }
    },
    {
        "id": 3,
        "name": "Stand Up Night",
        "datetime": "2026-11-08T20:00",
        "venue": "Teatro Gran Rex",
        "venueId": 3,
        "categories": ["Comedia", "Stand Up"],
        "description": "Noche de stand up con comediantes invitados.",
        "organizerId": 5,
        "status": "active",
        "sectors": {
            "Campo": {
                "price": 10000,
                "capacity": 100,
                "sold": 100
            },
            "Platea": {
                "price": 16000,
                "seats": [
                    ["occupied", "occupied", "occupied"],
                    ["occupied", "occupied", "occupied"]
                ]
            }
        }
    },
    {
        "id": 4,
        "name": "Tech Conference 2026",
        "datetime": "2026-10-03T10:00",
        "venue": "Centro de Convenciones",
        "venueId": 4,
        "categories": ["Tecnología", "Conferencia"],
        "description": "Conferencia sobre desarrollo de software y nuevas tecnologías.",
        "organizerId": 4,
        "status": "active",
        "sectors": {
            "General": {
                "price": 8000,
                "capacity": 500,
                "sold": 320
            },
            "VIP": {
                "price": 20000,
                "capacity": 50,
                "sold": 45
            }
        }
    }
]