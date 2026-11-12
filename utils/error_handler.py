import json
def execute_safely(function):
    """Ejecuta una función y muestra el error si falla el acceso a los datos.

    Parámetros:
        function (callable): función a ejecutar.

    Retorna:
        el resultado de la función, o None si falla el acceso a los datos.
    """
    try:
        return function()

    except (OSError, json.JSONDecodeError) as error:
        print(f"Error al acceder a los datos: {error}")
