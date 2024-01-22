def convertir_a_porcentaje(porcentaje):
    """
    Coge un porcentaje de una respuesta de un modelo bedrock y la convierte a un formato adecuado

    Args:
        porcentaje (str): Porcentaje a examinar obtenido de una respuesta de invoke_model de bedrock runtime

    Returns:
        porcentaje_num (float): Porcentaje numérico cuyo valor se comprende entre 0 y 1.
    """

    # Check deprecado: Sí que puede recibir integers o float la función
    # # Verificar si el input es un string
    # if type(porcentaje) != str:
    #     raise TypeError("El porcentaje introducido no es un string")

    # Verificar si el valor es None o está vacío. En caso afirmativo, devolver un cero.
    if porcentaje is None or str(porcentaje).strip() == "":
        return float(0)
    
    # Valores válidos para la función
    type_list = [str, int, float]

    # Si no es alguno de estos valores, interrumpe la función
    if type(porcentaje) not in type_list:
        raise TypeError(f"El porcentaje introducido no es ni int, ni float, ni str: Es de tipo {type(porcentaje)}")

    if isinstance(porcentaje, str):
        # Eliminar el símbolo de porcentaje si existe
        if porcentaje.endswith('%'):
            porcentaje = porcentaje[:-1]

    # Convertir a número
    try:
        porcentaje_num = float(porcentaje)
    except ValueError:
        raise ValueError("El valor proporcionado no es un número válido")

    # Normalizar a porcentaje
    if porcentaje_num > 1:
        porcentaje_num /= 100

    # Asegurar que el número está en el rango 0 - 100
    if porcentaje_num > 1 or porcentaje_num < 0:
        raise ValueError("El porcentaje está fuera del rango válido")

    # Convertir a formato de porcentaje
    # return f"{porcentaje_num:.2f}%"
    # Cambio revertido. Razón: porcentaje_del_resultado en GATI_CLASIFICACION FICHAS es un float. Adicionalmente,
    # si convertimos el porcentaje en un texto con %, no se podrán filtrar las respuestas según porcentaje de fiabilidad
    # en MySQL o Power BI.
    return porcentaje_num