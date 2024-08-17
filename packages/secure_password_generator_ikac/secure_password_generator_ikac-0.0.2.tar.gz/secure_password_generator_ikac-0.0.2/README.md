# Generador de Contraseñas Seguras

## Descripción

`secure_password_generator_ikac` es un paquete de Python diseñado para generar contraseñas seguras y aleatorias. Utiliza combinaciones de caracteres para crear contraseñas robustas que cumplen con los estándares de seguridad.

## Instalación

Puedes instalar el paquete desde PyPI usando `pip`:

```bash
pip install secure_password_generator_ikac
```

## Uso

### Generar una contraseña segura
Puedes generar una contraseña segura de 12 caracteres (por defecto) con la siguiente función:

```python
from secure_password_generator_ikac.foo import generar_contrasena

contraseña = generar_contrasena(12)
print(contraseña)
```

### Generar una lista de contraseñas seguras
Si necesitas varias contraseñas, puedes generar una lista de contraseñas seguras:

```python
from secure_password_generator_ikac.foo import generar_lista_contrasenas

lista_contrasenas = generar_lista_contrasenas(5, 12)
print(lista_contrasenas)
```

### Ejemplo de Uso Interactivo

Si deseas una interfaz de línea de comandos para generar contraseñas, puedes usar el siguiente script:

```python
from secure_password_generator_ikac.foo import generar_contrasena, generar_lista_contrasenas

def solicitar_opcion(mensaje: str) -> bool:
    """Solicita al usuario una respuesta sí/no y la devuelve como un valor booleano."""
    while True:
        respuesta = input(mensaje + " (y/n): ").strip().lower()
        if respuesta == 'y':
            return True
        elif respuesta == 'n':
            return False
        else:
            print("Por favor, responde con 'y' o 'n'.")

def solicitar_numero(mensaje: str, minimo: int) -> int:
    """Solicita al usuario un número entero mayor o igual al valor mínimo especificado."""
    while True:
        try:
            numero = int(input(mensaje + f" (mínimo {minimo}): "))
            if numero >= minimo:
                return numero
            else:
                print(f"El número debe ser al menos {minimo}.")
        except ValueError:
            print("Por favor, ingresa un número válido.")

if __name__ == "__main__":
    print("Generador de Contraseñas Seguras")

    # Preguntar al usuario qué opciones desea para la contraseña
    usar_letras = solicitar_opcion("¿Deseas incluir letras (mayúsculas y minúsculas)?")
    usar_numeros = solicitar_opcion("¿Deseas incluir números?")
    usar_simbolos = solicitar_opcion("¿Deseas incluir símbolos?")
    longitud = solicitar_numero("¿Cuál debería ser la longitud de la contraseña?", minimo=6)
    cantidad = solicitar_numero("¿Cuántas contraseñas deseas generar?", minimo=1)

    # Generar y mostrar la(s) contraseña(s)
    lista_contrasenas = generar_lista_contrasenas(
        cantidad=cantidad,
        longitud=longitud,
        usar_letras=usar_letras,
        usar_numeros=usar_numeros,
        usar_simbolos=usar_simbolos
    )

    print("Lista de Contraseñas Generadas:")
    for i, contrasena in enumerate(lista_contrasenas, start=1):
        print(f"{i}: {contrasena}")
```


## Características
1. Genera contraseñas seguras y aleatorias.
2. Permite personalizar la longitud de las contraseñas.
3. Genera múltiples contraseñas en un solo llamado.

## Ejecución de Pruebas
Este proyecto utiliza unittest para las pruebas. Puedes ejecutar todas las pruebas con:

```bash
python -m unittest discover -s tests
```

## Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para obtener más detalles.
