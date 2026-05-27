"""
Lógica de autenticación (registro e inicio de sesión).
"""
from app.models import Usuario
from app.validations import (
    validar_username, validar_email,
    validar_password, validar_edad
)


class SistemaAuth:
    def __init__(self):
        self._usuarios: dict[str, Usuario] = {}

    # ── Registro ─────────────────────────────────────────────────────────────
    def registrar(self, username: str, email: str,
                password: str, edad) -> dict:
        """
        Registra un nuevo usuario.
        Retorna {"exito": bool, "mensaje": str, "usuario": Usuario | None}
        """
        errores = []

        r_user = validar_username(username)
        if not r_user["valido"]:
            errores.append(r_user["mensaje"])

        r_email = validar_email(email)
        if not r_email["valido"]:
            errores.append(r_email["mensaje"])

        r_pass = validar_password(password)
        if not r_pass["valido"]:
            errores.append(r_pass["mensaje"])

        r_edad = validar_edad(edad)
        if not r_edad["valido"]:
            errores.append(r_edad["mensaje"])

        if errores:
            return {"exito": False, "mensaje": " | ".join(errores), "usuario": None}

        if username in self._usuarios:
            return {"exito": False, "mensaje": "El nombre de usuario ya está en uso.", "usuario": None}

        usuario = Usuario(username=username, email=email,
                            password=password, edad=edad)
        self._usuarios[username] = usuario
        return {"exito": True, "mensaje": "Usuario registrado exitosamente.", "usuario": usuario}

    # ── Login ─────────────────────────────────────────────────────────────────
    def login(self, username: str, password: str) -> dict:
        """
        Inicia sesión.
        Retorna {"exito": bool, "mensaje": str, "usuario": Usuario | None}
        """
        if not username or not password:
            return {"exito": False, "mensaje": "Usuario y contraseña son obligatorios.", "usuario": None}
        usuario = self._usuarios.get(username)
        if usuario is None:
            return {"exito": False, "mensaje": "Usuario no encontrado.", "usuario": None}
        if usuario.password != password:
            return {"exito": False, "mensaje": "Contraseña incorrecta.", "usuario": None}
        return {"exito": True, "mensaje": "Inicio de sesión exitoso.", "usuario": usuario}

    def obtener_usuario(self, username: str) -> Usuario | None:
        return self._usuarios.get(username)
