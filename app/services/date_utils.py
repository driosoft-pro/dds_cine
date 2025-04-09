from datetime import datetime

def calcular_edad(fecha_nacimiento: str) -> int:
    """
    Calcula la edad a partir de una fecha de nacimiento (formato YYYY-MM-DD).
    """
    nacimiento = datetime.strptime(fecha_nacimiento, "%Y-%m-%d")
    hoy = datetime.now()
    edad = hoy.year - nacimiento.year
    if (hoy.month, hoy.day) < (nacimiento.month, nacimiento.day):
        edad -= 1
    return edad

def esta_en_rango_para_reserva(fecha_funcion: str) -> bool:
    """
    Verifica si la fecha de la función está entre 2 y 7 días desde hoy.
    """
    fecha = datetime.strptime(fecha_funcion, "%Y-%m-%d")
    hoy = datetime.now()
    diferencia = (fecha - hoy).days
    return 2 <= diferencia <= 7

def se_puede_cancelar_reserva(fecha_funcion: str) -> bool:
    """
    Verifica si se puede cancelar una reserva (hasta 2 días antes).
    """
    fecha = datetime.strptime(fecha_funcion, "%Y-%m-%d")
    hoy = datetime.now()
    diferencia = (fecha - hoy).days
    return diferencia >= 2

def es_fecha_valida(fecha_str: str) -> bool:
    """
    Verifica si una cadena es una fecha válida en formato YYYY-MM-DD.
    """
    try:
        datetime.strptime(fecha_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False
