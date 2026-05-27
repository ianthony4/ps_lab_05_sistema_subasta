"""
Módulo de VALIDACIONES

Todas las funciones retornan un diccionario:
    {"valido": True/False, "mensaje": "..."}

Reglas de negocio:
─────────────────────────────────────────────────────────────
USUARIO
  - Username  : 3-20 chars, solo alfanumérico + guion bajo
  - Email     : debe contener @ y dominio
  - Password  : 8-64 chars, al menos 1 número, 1 mayúscula
  - Edad      : 18 <= edad <= 100  (AVL clave)

SUBASTA / PUJA
  - Precio base artículo : 1.00 <= precio <= 1_000_000.00
  - Incremento mínimo puja: el nuevo monto debe superar el
    precio actual en al menos S/ 1.00
  - Monto puja           : 1.00 <= monto <= 1_000_000.00

SALDO / DEPÓSITO
  - Monto depósito       : 10.00 <= monto <= 50_000.00

CALIFICACIÓN POST-SUBASTA
  - Puntuación           : 1 <= puntuacion <= 5  (entero)

NOMBRE ARTÍCULO
  - Longitud             : 3 <= len <= 100 chars
─────────────────────────────────────────────────────────────
"""

import re

# ─── Constantes (fácil de referenciar en los tests) ─────────────────────────
EDAD_MIN = 18
EDAD_MAX = 100

PASSWORD_MIN = 8
PASSWORD_MAX = 64

USERNAME_MIN = 3
USERNAME_MAX = 20

PRECIO_MIN = 1.00
PRECIO_MAX = 1_000_000.00

DEPOSITO_MIN = 10.00
DEPOSITO_MAX = 50_000.00

INCREMENTO_MIN = 1.00       # La puja debe superar el precio actual en al menos S/1

PUNTUACION_MIN = 1
PUNTUACION_MAX = 5

NOMBRE_ARTICULO_MIN = 3
NOMBRE_ARTICULO_MAX = 100

# SALDO vs PUJA (nueva regla — consistencia de dinero)
#   saldo_usuario >= monto_puja  para poder pujar


# ─── Helpers internos ────────────────────────────────────────────────────────
def _ok(mensaje: str = "OK") -> dict:
    return {"valido": True, "mensaje": mensaje}


def _err(mensaje: str) -> dict:
    return {"valido": False, "mensaje": mensaje}


# ════════════════════════════════════════════════════════════════════════════
# VALIDACIONES DE USUARIO
# ════════════════════════════════════════════════════════════════════════════

def validar_username(username) -> dict:
    """
    Reglas:
      - No puede ser None ni vacío.
      - Longitud: 3–20 caracteres.
      - Solo letras, números y guion bajo (_).
    """
    if username is None:
        return _err("El nombre de usuario es obligatorio.")
    if not isinstance(username, str):
        return _err("El nombre de usuario debe ser texto.")
    username = username.strip()
    if len(username) == 0:
        return _err("El nombre de usuario no puede estar vacío.")
    if len(username) < USERNAME_MIN:
        return _err(f"El nombre de usuario debe tener al menos {USERNAME_MIN} caracteres.")
    if len(username) > USERNAME_MAX:
        return _err(f"El nombre de usuario no puede exceder {USERNAME_MAX} caracteres.")
    if not re.match(r"^[a-zA-Z0-9_]+$", username):
        return _err("El nombre de usuario solo puede contener letras, números y guion bajo.")
    return _ok("Nombre de usuario válido.")


def validar_email(email) -> dict:
    """
    Reglas:
      - No puede ser None ni vacío.
      - Debe tener exactamente un @.
      - Debe tener dominio (algo.algo) después del @.
    """
    if email is None:
        return _err("El email es obligatorio.")
    if not isinstance(email, str):
        return _err("El email debe ser texto.")
    email = email.strip()
    if len(email) == 0:
        return _err("El email no puede estar vacío.")
    patron = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    if not re.match(patron, email):
        return _err("El email no tiene un formato válido.")
    return _ok("Email válido.")


def validar_password(password) -> dict:
    """
    Reglas:
      - No puede ser None ni vacío.
      - Longitud: 8–64 caracteres.
      - Al menos 1 letra mayúscula.
      - Al menos 1 dígito numérico.
    """
    if password is None:
        return _err("La contraseña es obligatoria.")
    if not isinstance(password, str):
        return _err("La contraseña debe ser texto.")
    if len(password) < PASSWORD_MIN:
        return _err(f"La contraseña debe tener al menos {PASSWORD_MIN} caracteres.")
    if len(password) > PASSWORD_MAX:
        return _err(f"La contraseña no puede exceder {PASSWORD_MAX} caracteres.")
    if not any(c.isupper() for c in password):
        return _err("La contraseña debe contener al menos una letra mayúscula.")
    if not any(c.isdigit() for c in password):
        return _err("La contraseña debe contener al menos un número.")
    return _ok("Contraseña válida.")


def validar_edad(edad) -> dict:
    """
    Reglas (AVL clave):
      - Debe ser entero.
      - 18 <= edad <= 100.
    """
    if edad is None:
        return _err("La edad es obligatoria.")
    if not isinstance(edad, int) or isinstance(edad, bool):
        return _err("La edad debe ser un número entero.")
    if edad < EDAD_MIN:
        return _err(f"La edad mínima para participar es {EDAD_MIN} años.")
    if edad > EDAD_MAX:
        return _err(f"La edad máxima registrada es {EDAD_MAX} años.")
    return _ok("Edad válida.")


# ════════════════════════════════════════════════════════════════════════════
# VALIDACIONES DE ARTÍCULO
# ════════════════════════════════════════════════════════════════════════════

def validar_nombre_articulo(nombre) -> dict:
    """
    Reglas:
      - No puede ser None ni vacío.
      - Longitud: 3–100 caracteres.
    """
    if nombre is None:
        return _err("El nombre del artículo es obligatorio.")
    if not isinstance(nombre, str):
        return _err("El nombre del artículo debe ser texto.")
    nombre = nombre.strip()
    if len(nombre) < NOMBRE_ARTICULO_MIN:
        return _err(f"El nombre del artículo debe tener al menos {NOMBRE_ARTICULO_MIN} caracteres.")
    if len(nombre) > NOMBRE_ARTICULO_MAX:
        return _err(f"El nombre del artículo no puede exceder {NOMBRE_ARTICULO_MAX} caracteres.")
    return _ok("Nombre de artículo válido.")


def validar_precio_base(precio) -> dict:
    """
    Reglas (AVL):
      - Debe ser numérico (int o float).
      - 1.00 <= precio <= 1_000_000.00.
    """
    if precio is None:
        return _err("El precio base es obligatorio.")
    if isinstance(precio, bool):
        return _err("El precio debe ser un valor numérico.")
    if not isinstance(precio, (int, float)):
        return _err("El precio debe ser un valor numérico.")
    if precio < PRECIO_MIN:
        return _err(f"El precio base mínimo es S/{PRECIO_MIN:.2f}.")
    if precio > PRECIO_MAX:
        return _err(f"El precio base máximo es S/{PRECIO_MAX:,.2f}.")
    return _ok("Precio base válido.")


def validar_categoria(categoria) -> dict:
    """
    Reglas:
      - Debe pertenecer a la lista de categorías permitidas.
    """
    CATEGORIAS_VALIDAS = {
        "electronica", "ropa", "coleccionables",
        "hogar", "deportes", "arte", "vehiculos", "otros"
    }
    if categoria is None:
        return _err("La categoría es obligatoria.")
    if not isinstance(categoria, str):
        return _err("La categoría debe ser texto.")
    if categoria.lower().strip() not in CATEGORIAS_VALIDAS:
        return _err(
            f"Categoría inválida. Opciones: {', '.join(sorted(CATEGORIAS_VALIDAS))}."
        )
    return _ok("Categoría válida.")


# ════════════════════════════════════════════════════════════════════════════
# VALIDACIONES DE PUJA
# ════════════════════════════════════════════════════════════════════════════

def validar_monto_puja(monto, precio_actual: float) -> dict:
    """
    Reglas (AVL + lógica de negocio):
      - Debe ser numérico.
      - 1.00 <= monto <= 1_000_000.00.
      - monto > precio_actual + INCREMENTO_MIN.
    """
    if monto is None:
        return _err("El monto de la puja es obligatorio.")
    if isinstance(monto, bool):
        return _err("El monto debe ser un valor numérico.")
    if not isinstance(monto, (int, float)):
        return _err("El monto de la puja debe ser un valor numérico.")
    if monto < PRECIO_MIN:
        return _err(f"El monto mínimo de puja es S/{PRECIO_MIN:.2f}.")
    if monto > PRECIO_MAX:
        return _err(f"El monto máximo de puja es S/{PRECIO_MAX:,.2f}.")
    minimo_requerido = round(precio_actual + INCREMENTO_MIN, 2)
    if monto < minimo_requerido:
        return _err(
            f"La puja debe superar el precio actual (S/{precio_actual:.2f}) "
            f"en al menos S/{INCREMENTO_MIN:.2f}. Mínimo: S/{minimo_requerido:.2f}."
        )
    return _ok("Monto de puja válido.")


# ════════════════════════════════════════════════════════════════════════════
# VALIDACIONES DE DEPÓSITO
# ════════════════════════════════════════════════════════════════════════════

def validar_deposito(monto) -> dict:
    """
    Reglas (AVL):
      - Debe ser numérico.
      - 10.00 <= monto <= 50_000.00.
    """
    if monto is None:
        return _err("El monto de depósito es obligatorio.")
    if isinstance(monto, bool):
        return _err("El monto debe ser un valor numérico.")
    if not isinstance(monto, (int, float)):
        return _err("El monto de depósito debe ser un valor numérico.")
    if monto < DEPOSITO_MIN:
        return _err(f"El depósito mínimo es S/{DEPOSITO_MIN:.2f}.")
    if monto > DEPOSITO_MAX:
        return _err(f"El depósito máximo es S/{DEPOSITO_MAX:,.2f}.")
    return _ok("Monto de depósito válido.")


# ════════════════════════════════════════════════════════════════════════════
# VALIDACIONES DE CALIFICACIÓN
# ════════════════════════════════════════════════════════════════════════════

def validar_puntuacion(puntuacion) -> dict:
    """
    Reglas (AVL):
      - Debe ser entero.
      - 1 <= puntuacion <= 5.
    """
    if puntuacion is None:
        return _err("La puntuación es obligatoria.")
    if isinstance(puntuacion, bool):
        return _err("La puntuación debe ser un número entero.")
    if not isinstance(puntuacion, int):
        return _err("La puntuación debe ser un número entero.")
    if puntuacion < PUNTUACION_MIN:
        return _err(f"La puntuación mínima es {PUNTUACION_MIN}.")
    if puntuacion > PUNTUACION_MAX:
        return _err(f"La puntuación máxima es {PUNTUACION_MAX}.")
    return _ok("Puntuación válida.")


# ════════════════════════════════════════════════════════════════════════════
# VALIDACIÓN DE SALDO SUFICIENTE
# ════════════════════════════════════════════════════════════════════════════

def validar_saldo_suficiente(saldo, monto_puja) -> dict:
    """
    Regla de negocio: el saldo disponible del usuario debe ser
    mayor o igual al monto de la puja que desea realizar.

      saldo_usuario >= monto_puja

    Parámetros:
      saldo      : saldo actual del usuario (float/int)
      monto_puja : monto que el usuario quiere pujar (float/int)
    """
    if isinstance(saldo, bool) or not isinstance(saldo, (int, float)):
        return _err("El saldo debe ser un valor numérico.")
    if isinstance(monto_puja, bool) or not isinstance(monto_puja, (int, float)):
        return _err("El monto de puja debe ser un valor numérico.")
    if saldo < monto_puja:
        return _err(
            f"Saldo insuficiente. Disponible: S/{saldo:.2f} | "
            f"Requerido: S/{monto_puja:.2f}."
        )
    return _ok("Saldo suficiente para realizar la puja.")

