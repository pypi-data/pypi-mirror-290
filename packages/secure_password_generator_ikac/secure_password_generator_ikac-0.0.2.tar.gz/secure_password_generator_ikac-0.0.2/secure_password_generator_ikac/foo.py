import random
import string
from typing import Optional, List

def generar_contrasena(
    longitud: Optional[int] = 12, 
    usar_letras: bool = True, 
    usar_numeros: bool = True, 
    usar_simbolos: bool = True
) -> str:
    """Genera una contraseña segura de longitud especificada y con los tipos de caracteres deseados.

    Args:
        longitud (Optional[int]): La longitud de la contraseña a generar. Por defecto es 12.
        usar_letras (bool): Si True, incluye letras en la contraseña.
        usar_numeros (bool): Si True, incluye números en la contraseña.
        usar_simbolos (bool): Si True, incluye símbolos en la contraseña.

    Returns:
        str: Contraseña generada.
    """
    if longitud < 6:
        raise ValueError("La longitud mínima para una contraseña es 6 caracteres.")
    if not (usar_letras or usar_numeros or usar_simbolos):
        raise ValueError("Debe seleccionar al menos un tipo de carácter.")

    # Definimos los grupos de caracteres según los parámetros
    caracteres_mayusculas = string.ascii_uppercase if usar_letras else ""
    caracteres_minusculas = string.ascii_lowercase if usar_letras else ""
    caracteres_numeros = string.digits if usar_numeros else ""
    caracteres_simbolos = string.punctuation if usar_simbolos else ""

    # Concatenamos todos los caracteres posibles
    todos_caracteres = caracteres_mayusculas + caracteres_minusculas + caracteres_numeros + caracteres_simbolos

    # Aseguramos que la contraseña contenga al menos un carácter de cada tipo que se va a usar
    contraseña = []
    if caracteres_mayusculas:
        contraseña.append(random.choice(caracteres_mayusculas))
    if caracteres_minusculas:
        contraseña.append(random.choice(caracteres_minusculas))
    if caracteres_numeros:
        contraseña.append(random.choice(caracteres_numeros))
    if caracteres_simbolos:
        contraseña.append(random.choice(caracteres_simbolos))

    # Rellenamos el resto de la contraseña con una combinación de todos los caracteres posibles
    contraseña += [random.choice(todos_caracteres) for _ in range(longitud - len(contraseña))]

    # Mezclamos la contraseña para asegurar una distribución aleatoria
    random.shuffle(contraseña)

    return ''.join(contraseña)

def generar_lista_contrasenas(
    cantidad: int, 
    longitud: Optional[int] = 12, 
    usar_letras: bool = True, 
    usar_numeros: bool = True, 
    usar_simbolos: bool = True
) -> List[str]:
    """Genera una lista de contraseñas seguras con los tipos de caracteres deseados.

    Args:
        cantidad (int): Número de contraseñas a generar.
        longitud (Optional[int]): Longitud de cada contraseña. Por defecto es 12.
        usar_letras (bool): Si True, incluye letras en la contraseña.
        usar_numeros (bool): Si True, incluye números en la contraseña.
        usar_simbolos (bool): Si True, incluye símbolos en la contraseña.

    Returns:
        List[str]: Lista de contraseñas generadas.
    """
    if cantidad < 1:
        raise ValueError("La cantidad de contraseñas debe ser al menos 1.")
    
    return [
        generar_contrasena(longitud, usar_letras, usar_numeros, usar_simbolos) 
        for _ in range(cantidad)
    ]
