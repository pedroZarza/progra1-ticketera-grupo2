import json
def execute_safely(function):
    try:
        return function()

    except (OSError, json.JSONDecodeError) as error:
        print(f"Error al acceder a los datos: {error}")