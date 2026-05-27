"""
════════════════════════════════════════════════════════════════════════════════
TEST PE — PARTICIÓN DE EQUIVALENCIA
Plataforma de Subastas Online

Cada función de validación tiene clases válidas e inválidas.
Las tablas en los comentarios resumen las clases antes de los casos.
════════════════════════════════════════════════════════════════════════════════
"""
import pytest
from app.validations import (
    validar_username, validar_email, validar_password, validar_edad,
    validar_nombre_articulo, validar_precio_base, validar_categoria,
    validar_monto_puja, validar_deposito, validar_puntuacion,
    validar_saldo_suficiente
)
from app.auth import SistemaAuth
from app.auction import SistemaSubastas


# ════════════════════════════════════════════════════════════════════════════
# PE-01  VALIDAR USERNAME
# ════════════════════════════════════════════════════════════════════════════
# ┌──────────────────────┬──────────────────────┬───────────────┐
# │ Clase                │ Valor de prueba       │ Resultado     │
# ├──────────────────────┼──────────────────────┼───────────────┤
# │ Válida (normal)      │ "juan_perez"          │ Válido        │
# │ Inválida – corto     │ "ab"                  │ Error         │
# │ Inválida – largo     │ "a" * 21              │ Error         │
# │ Inválida – especial  │ "juan@perez"          │ Error         │
# │ Inválida – vacío     │ ""                    │ Error         │
# │ Inválida – None      │ None                  │ Error         │
# └──────────────────────┴──────────────────────┴───────────────┘

class TestPE_Username:
    def test_username_valido_normal(self):
        """CE-V1: username alfanumérico normal → válido"""
        resultado = validar_username("juan_perez")
        assert resultado["valido"] is True

    def test_username_valido_solo_numeros_letras(self):
        """CE-V2: username solo letras → válido"""
        resultado = validar_username("Maria123")
        assert resultado["valido"] is True

    def test_username_invalido_muy_corto(self):
        """CE-I1: username < 3 chars → inválido"""
        resultado = validar_username("ab")
        assert resultado["valido"] is False

    def test_username_invalido_muy_largo(self):
        """CE-I2: username > 20 chars → inválido"""
        resultado = validar_username("a" * 21)
        assert resultado["valido"] is False

    def test_username_invalido_caracteres_especiales(self):
        """CE-I3: username con @ → inválido"""
        resultado = validar_username("juan@perez")
        assert resultado["valido"] is False

    def test_username_invalido_vacio(self):
        """CE-I4: username vacío → inválido"""
        resultado = validar_username("")
        assert resultado["valido"] is False

    def test_username_invalido_none(self):
        """CE-I5: username None → inválido"""
        resultado = validar_username(None)
        assert resultado["valido"] is False


# ════════════════════════════════════════════════════════════════════════════
# PE-02  VALIDAR EMAIL
# ════════════════════════════════════════════════════════════════════════════
# ┌──────────────────────┬──────────────────────────────┬───────────────┐
# │ Clase                │ Valor de prueba               │ Resultado     │
# ├──────────────────────┼──────────────────────────────┼───────────────┤
# │ Válida               │ "user@example.com"            │ Válido        │
# │ Inválida – sin @     │ "userexample.com"             │ Error         │
# │ Inválida – sin dom.  │ "user@"                       │ Error         │
# │ Inválida – vacío     │ ""                            │ Error         │
# │ Inválida – None      │ None                          │ Error         │
# └──────────────────────┴──────────────────────────────┴───────────────┘

class TestPE_Email:
    def test_email_valido(self):
        """CE-V1: email con formato correcto → válido"""
        assert validar_email("user@example.com")["valido"] is True

    def test_email_invalido_sin_arroba(self):
        """CE-I1: email sin @ → inválido"""
        assert validar_email("userexample.com")["valido"] is False

    def test_email_invalido_sin_dominio(self):
        """CE-I2: email sin dominio → inválido"""
        assert validar_email("user@")["valido"] is False

    def test_email_invalido_vacio(self):
        """CE-I3: email vacío → inválido"""
        assert validar_email("")["valido"] is False

    def test_email_invalido_none(self):
        """CE-I4: email None → inválido"""
        assert validar_email(None)["valido"] is False


# ════════════════════════════════════════════════════════════════════════════
# PE-03  VALIDAR PASSWORD
# ════════════════════════════════════════════════════════════════════════════
# ┌───────────────────────────┬─────────────────┬───────────────┐
# │ Clase                     │ Valor de prueba  │ Resultado     │
# ├───────────────────────────┼─────────────────┼───────────────┤
# │ Válida                    │ "Segura123"      │ Válido        │
# │ Inválida – muy corta      │ "Abc1234"        │ Error (7 ch.) │
# │ Inválida – sin mayúscula  │ "segura123"      │ Error         │
# │ Inválida – sin número     │ "Segurapass"     │ Error         │
# │ Inválida – None           │ None             │ Error         │
# └───────────────────────────┴─────────────────┴───────────────┘

class TestPE_Password:
    def test_password_valida(self):
        """CE-V1: password cumple todos los requisitos → válida"""
        assert validar_password("Segura123")["valido"] is True

    def test_password_invalida_muy_corta(self):
        """CE-I1: password < 8 chars → inválida"""
        assert validar_password("Abc123")["valido"] is False

    def test_password_invalida_sin_mayuscula(self):
        """CE-I2: password sin mayúscula → inválida"""
        assert validar_password("segura123")["valido"] is False

    def test_password_invalida_sin_numero(self):
        """CE-I3: password sin número → inválida"""
        assert validar_password("Segurapass")["valido"] is False

    def test_password_invalida_none(self):
        """CE-I4: password None → inválida"""
        assert validar_password(None)["valido"] is False


# ════════════════════════════════════════════════════════════════════════════
# PE-04  VALIDAR EDAD
# ════════════════════════════════════════════════════════════════════════════
# ┌──────────────────────┬──────────────────┬───────────────┐
# │ Clase                │ Valor de prueba  │ Resultado     │
# ├──────────────────────┼──────────────────┼───────────────┤
# │ Válida (interior)    │ 30               │ Válido        │
# │ Inválida – menor     │ 17               │ Error         │
# │ Inválida – mayor     │ 101              │ Error         │
# │ Inválida – negativa  │ -1               │ Error         │
# │ Inválida – tipo str  │ "treinta"        │ Error         │
# │ Inválida – float     │ 25.5             │ Error         │
# │ Inválida – None      │ None             │ Error         │
# └──────────────────────┴──────────────────┴───────────────┘

class TestPE_Edad:
    def test_edad_valida_interior(self):
        """CE-V1: edad en rango interior → válida"""
        assert validar_edad(30)["valido"] is True

    def test_edad_invalida_menor(self):
        """CE-I1: edad por debajo del mínimo → inválida"""
        assert validar_edad(17)["valido"] is False

    def test_edad_invalida_mayor(self):
        """CE-I2: edad por encima del máximo → inválida"""
        assert validar_edad(101)["valido"] is False

    def test_edad_invalida_negativa(self):
        """CE-I3: edad negativa → inválida"""
        assert validar_edad(-1)["valido"] is False

    def test_edad_invalida_tipo_str(self):
        """CE-I4: edad como string → inválida"""
        assert validar_edad("treinta")["valido"] is False

    def test_edad_invalida_float(self):
        """CE-I5: edad como float → inválida"""
        assert validar_edad(25.5)["valido"] is False

    def test_edad_invalida_none(self):
        """CE-I6: edad None → inválida"""
        assert validar_edad(None)["valido"] is False


# ════════════════════════════════════════════════════════════════════════════
# PE-05  VALIDAR PRECIO BASE
# ════════════════════════════════════════════════════════════════════════════
# ┌────────────────────────┬──────────────────┬───────────────┐
# │ Clase                  │ Valor de prueba  │ Resultado     │
# ├────────────────────────┼──────────────────┼───────────────┤
# │ Válida (interior)      │ 500.00           │ Válido        │
# │ Inválida – menor       │ 0.50             │ Error         │
# │ Inválida – mayor       │ 1_500_000.00     │ Error         │
# │ Inválida – tipo str    │ "cien"           │ Error         │
# │ Inválida – negativo    │ -10.00           │ Error         │
# └────────────────────────┴──────────────────┴───────────────┘

class TestPE_PrecioBase:
    def test_precio_valido_interior(self):
        """CE-V1: precio normal → válido"""
        assert validar_precio_base(500.00)["valido"] is True

    def test_precio_invalido_menor(self):
        """CE-I1: precio menor al mínimo → inválido"""
        assert validar_precio_base(0.50)["valido"] is False

    def test_precio_invalido_mayor(self):
        """CE-I2: precio mayor al máximo → inválido"""
        assert validar_precio_base(1_500_000.00)["valido"] is False

    def test_precio_invalido_tipo_str(self):
        """CE-I3: precio como string → inválido"""
        assert validar_precio_base("cien")["valido"] is False

    def test_precio_invalido_negativo(self):
        """CE-I4: precio negativo → inválido"""
        assert validar_precio_base(-10.00)["valido"] is False


# ════════════════════════════════════════════════════════════════════════════
# PE-06  VALIDAR CATEGORÍA
# ════════════════════════════════════════════════════════════════════════════
# ┌──────────────────────┬──────────────────────┬───────────────┐
# │ Clase                │ Valor de prueba       │ Resultado     │
# ├──────────────────────┼──────────────────────┼───────────────┤
# │ Válida               │ "electronica"         │ Válido        │
# │ Inválida – inexist.  │ "mascotas"            │ Error         │
# │ Inválida – None      │ None                  │ Error         │
# │ Inválida – vacía     │ ""                    │ Error         │
# └──────────────────────┴──────────────────────┴───────────────┘

class TestPE_Categoria:
    def test_categoria_valida(self):
        """CE-V1: categoría permitida → válida"""
        assert validar_categoria("electronica")["valido"] is True

    def test_categoria_valida_case_insensitive(self):
        """CE-V2: categoría en mayúsculas → válida"""
        assert validar_categoria("ROPA")["valido"] is True

    def test_categoria_invalida_inexistente(self):
        """CE-I1: categoría no permitida → inválida"""
        assert validar_categoria("mascotas")["valido"] is False

    def test_categoria_invalida_none(self):
        """CE-I2: categoría None → inválida"""
        assert validar_categoria(None)["valido"] is False

    def test_categoria_invalida_vacia(self):
        """CE-I3: categoría vacía → inválida"""
        assert validar_categoria("")["valido"] is False


# ════════════════════════════════════════════════════════════════════════════
# PE-07  VALIDAR MONTO PUJA
# ════════════════════════════════════════════════════════════════════════════
# ┌──────────────────────────┬──────────────────┬───────────────┐
# │ Clase                    │ Valor de prueba  │ Resultado     │
# ├──────────────────────────┼──────────────────┼───────────────┤
# │ Válida                   │ 200.00 (base=100)│ Válido        │
# │ Inválida – insuf. incr.  │ 100.50 (base=100)│ Error         │
# │ Inválida – supera máx.   │ 2_000_000        │ Error         │
# │ Inválida – negativa      │ -50              │ Error         │
# │ Inválida – tipo str      │ "doscientos"     │ Error         │
# └──────────────────────────┴──────────────────┴───────────────┘

class TestPE_MontoPuja:
    def test_monto_puja_valido(self):
        """CE-V1: monto supera precio actual en más de S/1 → válido"""
        assert validar_monto_puja(200.00, 100.00)["valido"] is True

    def test_monto_puja_invalido_incremento_insuficiente(self):
        """CE-I1: monto no supera el incremento mínimo → inválido"""
        assert validar_monto_puja(100.50, 100.00)["valido"] is False

    def test_monto_puja_invalido_supera_maximo(self):
        """CE-I2: monto mayor al máximo permitido → inválido"""
        assert validar_monto_puja(2_000_000, 100.00)["valido"] is False

    def test_monto_puja_invalido_negativo(self):
        """CE-I3: monto negativo → inválido"""
        assert validar_monto_puja(-50, 100.00)["valido"] is False

    def test_monto_puja_invalido_tipo_str(self):
        """CE-I4: monto como string → inválido"""
        assert validar_monto_puja("doscientos", 100.00)["valido"] is False


# ════════════════════════════════════════════════════════════════════════════
# PE-08  VALIDAR DEPÓSITO
# ════════════════════════════════════════════════════════════════════════════
# ┌──────────────────────┬──────────────────┬───────────────┐
# │ Clase                │ Valor de prueba  │ Resultado     │
# ├──────────────────────┼──────────────────┼───────────────┤
# │ Válida (interior)    │ 1000.00          │ Válido        │
# │ Inválida – menor     │ 5.00             │ Error         │
# │ Inválida – mayor     │ 60_000.00        │ Error         │
# │ Inválida – tipo str  │ "mil"            │ Error         │
# └──────────────────────┴──────────────────┴───────────────┘

class TestPE_Deposito:
    def test_deposito_valido(self):
        """CE-V1: monto de depósito dentro del rango → válido"""
        assert validar_deposito(1000.00)["valido"] is True

    def test_deposito_invalido_menor(self):
        """CE-I1: monto menor al mínimo → inválido"""
        assert validar_deposito(5.00)["valido"] is False

    def test_deposito_invalido_mayor(self):
        """CE-I2: monto mayor al máximo → inválido"""
        assert validar_deposito(60_000.00)["valido"] is False

    def test_deposito_invalido_tipo_str(self):
        """CE-I3: monto como string → inválido"""
        assert validar_deposito("mil")["valido"] is False


# ════════════════════════════════════════════════════════════════════════════
# PE-09  VALIDAR PUNTUACIÓN
# ════════════════════════════════════════════════════════════════════════════
# ┌──────────────────────┬──────────────────┬───────────────┐
# │ Clase                │ Valor de prueba  │ Resultado     │
# ├──────────────────────┼──────────────────┼───────────────┤
# │ Válida (interior)    │ 3               │ Válido        │
# │ Inválida – menor     │ 0               │ Error         │
# │ Inválida – mayor     │ 6               │ Error         │
# │ Inválida – float     │ 3.5             │ Error         │
# │ Inválida – None      │ None            │ Error         │
# └──────────────────────┴──────────────────┴───────────────┘

class TestPE_Puntuacion:
    def test_puntuacion_valida_interior(self):
        """CE-V1: puntuación en rango interior → válida"""
        assert validar_puntuacion(3)["valido"] is True

    def test_puntuacion_invalida_menor(self):
        """CE-I1: puntuación por debajo del mínimo → inválida"""
        assert validar_puntuacion(0)["valido"] is False

    def test_puntuacion_invalida_mayor(self):
        """CE-I2: puntuación por encima del máximo → inválida"""
        assert validar_puntuacion(6)["valido"] is False

    def test_puntuacion_invalida_float(self):
        """CE-I3: puntuación como float → inválida"""
        assert validar_puntuacion(3.5)["valido"] is False

    def test_puntuacion_invalida_none(self):
        """CE-I4: puntuación None → inválida"""
        assert validar_puntuacion(None)["valido"] is False


# ════════════════════════════════════════════════════════════════════════════
# PE-10  VALIDAR SALDO SUFICIENTE (nueva validación)
# ════════════════════════════════════════════════════════════════════════════
# ┌──────────────────────────────┬──────────────────────┬───────────────┐
# │ Clase                        │ Valores (saldo/puja)  │ Resultado     │
# ├──────────────────────────────┼──────────────────────┼───────────────┤
# │ Válida – saldo > monto       │ 200.00 / 100.00       │ Válido        │
# │ Válida – saldo = monto       │ 100.00 / 100.00       │ Válido        │
# │ Inválida – saldo < monto     │ 50.00  / 100.00       │ Error         │
# │ Inválida – saldo cero        │ 0.00   / 100.00       │ Error         │
# │ Inválida – saldo negativo    │ -10.00 / 100.00       │ Error         │
# │ Inválida – saldo tipo str    │ "cien" / 100.00       │ Error         │
# │ Inválida – monto tipo str    │ 100.00 / "cien"       │ Error         │
# └──────────────────────────────┴──────────────────────┴───────────────┘

class TestPE_SaldoSuficiente:
    def test_saldo_mayor_al_monto(self):
        """CE-V1: saldo > monto_puja → válido"""
        assert validar_saldo_suficiente(200.00, 100.00)["valido"] is True

    def test_saldo_igual_al_monto(self):
        """CE-V2: saldo == monto_puja (exacto) → válido (límite)"""
        assert validar_saldo_suficiente(100.00, 100.00)["valido"] is True

    def test_saldo_menor_al_monto(self):
        """CE-I1: saldo < monto_puja → inválido"""
        assert validar_saldo_suficiente(50.00, 100.00)["valido"] is False

    def test_saldo_cero(self):
        """CE-I2: saldo = 0 → inválido para cualquier puja"""
        assert validar_saldo_suficiente(0.00, 100.00)["valido"] is False

    def test_saldo_negativo(self):
        """CE-I3: saldo negativo → inválido"""
        assert validar_saldo_suficiente(-10.00, 100.00)["valido"] is False

    def test_saldo_tipo_str(self):
        """CE-I4: saldo como string → inválido"""
        assert validar_saldo_suficiente("cien", 100.00)["valido"] is False

    def test_monto_puja_tipo_str(self):
        """CE-I5: monto_puja como string → inválido"""
        assert validar_saldo_suficiente(100.00, "cien")["valido"] is False


# ════════════════════════════════════════════════════════════════════════════
# PE-11  VER SUBASTAS GANADAS — prueba de integración
# ════════════════════════════════════════════════════════════════════════════
# Prueba el flujo completo: pujar → cerrar subasta → verificar registro
# de la compra y el descuento de saldo.
# ┌──────────────────────────────┬────────────────────────┬───────────────┐
# │ Escenario                    │ Acción                  │ Resultado     │
# ├──────────────────────────────┼────────────────────────┼───────────────┤
# │ Usuario sin compras          │ ver_subastas_ganadas    │ Lista vacía   │
# │ Usuario inexistente          │ ver_subastas_ganadas    │ exito=False   │
# │ Ganador: dinero descontado   │ cerrar + ver saldo      │ saldo - monto │
# │ Vendedor: dinero acreditado  │ cerrar + ver saldo      │ saldo + monto │
# │ Registro en historial        │ ver_subastas_ganadas    │ 1 elemento    │
# └──────────────────────────────┴────────────────────────┴───────────────┘

class TestPE_VerSubastasGanadas:
    """Pruebas de integración para la función ver_subastas_ganadas."""

    def setup_method(self):
        """Crea un sistema limpio antes de cada test."""
        self.auth = SistemaAuth()
        self.sistema = SistemaSubastas(self.auth)
        # Registrar vendedor
        self.auth.registrar("vendedor1", "v@test.com", "Vendedor1", 30)
        usr_v = self.auth.obtener_usuario("vendedor1")
        usr_v.saldo = 0.0
        # Registrar comprador
        self.auth.registrar("comprador1", "c@test.com", "Comprador1", 25)
        usr_c = self.auth.obtener_usuario("comprador1")
        usr_c.saldo = 500.0

    def test_usuario_sin_compras_devuelve_lista_vacia(self):
        """CE-V1: usuario existente sin subastas ganadas → lista vacía"""
        result = self.sistema.ver_subastas_ganadas("comprador1")
        assert result["exito"] is True
        assert result["ganadas"] == []

    def test_usuario_inexistente_devuelve_exito_false(self):
        """CE-I1: username que no existe → exito=False"""
        result = self.sistema.ver_subastas_ganadas("fantasma")
        assert result["exito"] is False
        assert result["ganadas"] == []

    def test_ganar_subasta_descuenta_saldo_comprador(self):
        """CE-V2: al cerrar la subasta, el saldo del ganador se reduce."""
        self.sistema.publicar_articulo(
            "Laptop", "Descripción", 100.0, "vendedor1", "electronica"
        )
        self.sistema.realizar_puja(1, "comprador1", 200.0)
        self.sistema.cerrar_subasta(1, "vendedor1")
        comprador = self.auth.obtener_usuario("comprador1")
        assert comprador.saldo == 300.0   # 500 - 200

    def test_ganar_subasta_acredita_saldo_vendedor(self):
        """CE-V3: al cerrar la subasta, el saldo del vendedor aumenta."""
        self.sistema.publicar_articulo(
            "Silla", "Ergonómica", 50.0, "vendedor1", "hogar"
        )
        self.sistema.realizar_puja(1, "comprador1", 150.0)
        self.sistema.cerrar_subasta(1, "vendedor1")
        vendedor = self.auth.obtener_usuario("vendedor1")
        assert vendedor.saldo == 150.0

    def test_ganar_subasta_registra_en_historial(self):
        """CE-V4: tras cerrar, el artículo aparece en ver_subastas_ganadas."""
        self.sistema.publicar_articulo(
            "Reloj", "Clásico", 80.0, "vendedor1", "coleccionables"
        )
        self.sistema.realizar_puja(1, "comprador1", 120.0)
        self.sistema.cerrar_subasta(1, "vendedor1")
        result = self.sistema.ver_subastas_ganadas("comprador1")
        assert result["exito"] is True
        assert len(result["ganadas"]) == 1
        assert result["ganadas"][0]["nombre"] == "Reloj"
        assert result["ganadas"][0]["monto_pagado"] == 120.0
