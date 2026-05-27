"""
════════════════════════════════════════════════════════════════════════════════
TEST AVL — ANÁLISIS DE VALORES LÍMITE
Plataforma de Subastas Online

Para cada campo con rango [MIN, MAX] se prueban:
  • MIN - 1  → INVÁLIDO
  • MIN      → VÁLIDO   (límite inferior)
  • MIN + 1  → VÁLIDO
  • Valor interior representativo
  • MAX - 1  → VÁLIDO
  • MAX      → VÁLIDO   (límite superior)
  • MAX + 1  → INVÁLIDO
════════════════════════════════════════════════════════════════════════════════
"""
import pytest
from app.validations import (
    validar_edad, validar_password, validar_username,
    validar_precio_base, validar_deposito, validar_puntuacion,
    validar_monto_puja, validar_nombre_articulo,
    validar_saldo_suficiente,
    EDAD_MIN, EDAD_MAX,
    PASSWORD_MIN, PASSWORD_MAX,
    USERNAME_MIN, USERNAME_MAX,
    PRECIO_MIN, PRECIO_MAX,
    DEPOSITO_MIN, DEPOSITO_MAX,
    PUNTUACION_MIN, PUNTUACION_MAX,
    NOMBRE_ARTICULO_MIN, NOMBRE_ARTICULO_MAX,
    INCREMENTO_MIN
)


# ════════════════════════════════════════════════════════════════════════════
# AVL-01  EDAD  [18 – 100]
# ════════════════════════════════════════════════════════════════════════════
# ┌────────────────┬──────────┬───────────────┐
# │ Entrada        │ Valor    │ Resultado      │
# ├────────────────┼──────────┼───────────────┤
# │ MIN - 1        │ 17       │ Error          │
# │ MIN (límite ↓) │ 18       │ Correcto       │
# │ MIN + 1        │ 19       │ Correcto       │
# │ Interior       │ 50       │ Correcto       │
# │ MAX - 1        │ 99       │ Correcto       │
# │ MAX (límite ↑) │ 100      │ Correcto       │
# │ MAX + 1        │ 101      │ Error          │
# └────────────────┴──────────┴───────────────┘

class TestAVL_Edad:
    def test_edad_min_menos_1(self):
        """AVL: edad = 17 (MIN-1) → INVÁLIDO"""
        assert validar_edad(EDAD_MIN - 1)["valido"] is False

    def test_edad_min(self):
        """AVL: edad = 18 (MIN) → VÁLIDO"""
        assert validar_edad(EDAD_MIN)["valido"] is True

    def test_edad_min_mas_1(self):
        """AVL: edad = 19 (MIN+1) → VÁLIDO"""
        assert validar_edad(EDAD_MIN + 1)["valido"] is True

    def test_edad_interior(self):
        """AVL: edad = 50 (interior) → VÁLIDO"""
        assert validar_edad(50)["valido"] is True

    def test_edad_max_menos_1(self):
        """AVL: edad = 99 (MAX-1) → VÁLIDO"""
        assert validar_edad(EDAD_MAX - 1)["valido"] is True

    def test_edad_max(self):
        """AVL: edad = 100 (MAX) → VÁLIDO"""
        assert validar_edad(EDAD_MAX)["valido"] is True

    def test_edad_max_mas_1(self):
        """AVL: edad = 101 (MAX+1) → INVÁLIDO"""
        assert validar_edad(EDAD_MAX + 1)["valido"] is False


# ════════════════════════════════════════════════════════════════════════════
# AVL-02  PASSWORD LONGITUD  [8 – 64]
# ════════════════════════════════════════════════════════════════════════════
# ┌────────────────┬──────────┬───────────────┐
# │ Entrada        │ Longitud │ Resultado      │
# ├────────────────┼──────────┼───────────────┤
# │ MIN - 1        │ 7        │ Error          │
# │ MIN (límite ↓) │ 8        │ Correcto       │
# │ MIN + 1        │ 9        │ Correcto       │
# │ Interior       │ 20       │ Correcto       │
# │ MAX - 1        │ 63       │ Correcto       │
# │ MAX (límite ↑) │ 64       │ Correcto       │
# │ MAX + 1        │ 65       │ Error          │
# └────────────────┴──────────┴───────────────┘

def _pwd(longitud: int) -> str:
    """Genera una password válida (1 mayúscula + 1 número + relleno) de `longitud` chars."""
    base = "A1" + "a" * (longitud - 2)
    return base[:longitud]


class TestAVL_PasswordLongitud:
    def test_password_longitud_min_menos_1(self):
        """AVL: password de 7 chars (MIN-1) → INVÁLIDA"""
        assert validar_password(_pwd(PASSWORD_MIN - 1))["valido"] is False

    def test_password_longitud_min(self):
        """AVL: password de 8 chars (MIN) → VÁLIDA"""
        assert validar_password(_pwd(PASSWORD_MIN))["valido"] is True

    def test_password_longitud_min_mas_1(self):
        """AVL: password de 9 chars (MIN+1) → VÁLIDA"""
        assert validar_password(_pwd(PASSWORD_MIN + 1))["valido"] is True

    def test_password_longitud_interior(self):
        """AVL: password de 20 chars (interior) → VÁLIDA"""
        assert validar_password(_pwd(20))["valido"] is True

    def test_password_longitud_max_menos_1(self):
        """AVL: password de 63 chars (MAX-1) → VÁLIDA"""
        assert validar_password(_pwd(PASSWORD_MAX - 1))["valido"] is True

    def test_password_longitud_max(self):
        """AVL: password de 64 chars (MAX) → VÁLIDA"""
        assert validar_password(_pwd(PASSWORD_MAX))["valido"] is True

    def test_password_longitud_max_mas_1(self):
        """AVL: password de 65 chars (MAX+1) → INVÁLIDA"""
        assert validar_password(_pwd(PASSWORD_MAX + 1))["valido"] is False


# ════════════════════════════════════════════════════════════════════════════
# AVL-03  PRECIO BASE  [1.00 – 1,000,000.00]
# ════════════════════════════════════════════════════════════════════════════
# ┌────────────────┬────────────────┬───────────────┐
# │ Entrada        │ Valor (S/)     │ Resultado      │
# ├────────────────┼────────────────┼───────────────┤
# │ MIN - epsilon  │ 0.99           │ Error          │
# │ MIN (límite ↓) │ 1.00           │ Correcto       │
# │ MIN + epsilon  │ 1.01           │ Correcto       │
# │ Interior       │ 500.00         │ Correcto       │
# │ MAX - epsilon  │ 999_999.99     │ Correcto       │
# │ MAX (límite ↑) │ 1_000_000.00   │ Correcto       │
# │ MAX + epsilon  │ 1_000_000.01   │ Error          │
# └────────────────┴────────────────┴───────────────┘

class TestAVL_PrecioBase:
    def test_precio_min_menos_epsilon(self):
        """AVL: precio = 0.99 (MIN-ε) → INVÁLIDO"""
        assert validar_precio_base(0.99)["valido"] is False

    def test_precio_min(self):
        """AVL: precio = 1.00 (MIN) → VÁLIDO"""
        assert validar_precio_base(PRECIO_MIN)["valido"] is True

    def test_precio_min_mas_epsilon(self):
        """AVL: precio = 1.01 (MIN+ε) → VÁLIDO"""
        assert validar_precio_base(1.01)["valido"] is True

    def test_precio_interior(self):
        """AVL: precio = 500.00 (interior) → VÁLIDO"""
        assert validar_precio_base(500.00)["valido"] is True

    def test_precio_max_menos_epsilon(self):
        """AVL: precio = 999_999.99 (MAX-ε) → VÁLIDO"""
        assert validar_precio_base(999_999.99)["valido"] is True

    def test_precio_max(self):
        """AVL: precio = 1_000_000.00 (MAX) → VÁLIDO"""
        assert validar_precio_base(PRECIO_MAX)["valido"] is True

    def test_precio_max_mas_epsilon(self):
        """AVL: precio = 1_000_000.01 (MAX+ε) → INVÁLIDO"""
        assert validar_precio_base(1_000_000.01)["valido"] is False


# ════════════════════════════════════════════════════════════════════════════
# AVL-04  DEPÓSITO  [10.00 – 50,000.00]
# ════════════════════════════════════════════════════════════════════════════
# ┌────────────────┬────────────────┬───────────────┐
# │ Entrada        │ Valor (S/)     │ Resultado      │
# ├────────────────┼────────────────┼───────────────┤
# │ MIN - epsilon  │ 9.99           │ Error          │
# │ MIN (límite ↓) │ 10.00          │ Correcto       │
# │ MIN + epsilon  │ 10.01          │ Correcto       │
# │ Interior       │ 1_000.00       │ Correcto       │
# │ MAX - epsilon  │ 49_999.99      │ Correcto       │
# │ MAX (límite ↑) │ 50_000.00      │ Correcto       │
# │ MAX + epsilon  │ 50_000.01      │ Error          │
# └────────────────┴────────────────┴───────────────┘

class TestAVL_Deposito:
    def test_deposito_min_menos_epsilon(self):
        """AVL: depósito = 9.99 (MIN-ε) → INVÁLIDO"""
        assert validar_deposito(9.99)["valido"] is False

    def test_deposito_min(self):
        """AVL: depósito = 10.00 (MIN) → VÁLIDO"""
        assert validar_deposito(DEPOSITO_MIN)["valido"] is True

    def test_deposito_min_mas_epsilon(self):
        """AVL: depósito = 10.01 (MIN+ε) → VÁLIDO"""
        assert validar_deposito(10.01)["valido"] is True

    def test_deposito_interior(self):
        """AVL: depósito = 1000.00 (interior) → VÁLIDO"""
        assert validar_deposito(1_000.00)["valido"] is True

    def test_deposito_max_menos_epsilon(self):
        """AVL: depósito = 49_999.99 (MAX-ε) → VÁLIDO"""
        assert validar_deposito(49_999.99)["valido"] is True

    def test_deposito_max(self):
        """AVL: depósito = 50_000.00 (MAX) → VÁLIDO"""
        assert validar_deposito(DEPOSITO_MAX)["valido"] is True

    def test_deposito_max_mas_epsilon(self):
        """AVL: depósito = 50_000.01 (MAX+ε) → INVÁLIDO"""
        assert validar_deposito(50_000.01)["valido"] is False


# ════════════════════════════════════════════════════════════════════════════
# AVL-05  PUNTUACIÓN  [1 – 5]
# ════════════════════════════════════════════════════════════════════════════
# ┌────────────────┬──────────┬───────────────┐
# │ Entrada        │ Valor    │ Resultado      │
# ├────────────────┼──────────┼───────────────┤
# │ MIN - 1        │ 0        │ Error          │
# │ MIN (límite ↓) │ 1        │ Correcto       │
# │ MIN + 1        │ 2        │ Correcto       │
# │ Interior       │ 3        │ Correcto       │
# │ MAX - 1        │ 4        │ Correcto       │
# │ MAX (límite ↑) │ 5        │ Correcto       │
# │ MAX + 1        │ 6        │ Error          │
# └────────────────┴──────────┴───────────────┘

class TestAVL_Puntuacion:
    def test_puntuacion_min_menos_1(self):
        """AVL: puntuación = 0 (MIN-1) → INVÁLIDA"""
        assert validar_puntuacion(PUNTUACION_MIN - 1)["valido"] is False

    def test_puntuacion_min(self):
        """AVL: puntuación = 1 (MIN) → VÁLIDA"""
        assert validar_puntuacion(PUNTUACION_MIN)["valido"] is True

    def test_puntuacion_min_mas_1(self):
        """AVL: puntuación = 2 (MIN+1) → VÁLIDA"""
        assert validar_puntuacion(PUNTUACION_MIN + 1)["valido"] is True

    def test_puntuacion_interior(self):
        """AVL: puntuación = 3 (interior) → VÁLIDA"""
        assert validar_puntuacion(3)["valido"] is True

    def test_puntuacion_max_menos_1(self):
        """AVL: puntuación = 4 (MAX-1) → VÁLIDA"""
        assert validar_puntuacion(PUNTUACION_MAX - 1)["valido"] is True

    def test_puntuacion_max(self):
        """AVL: puntuación = 5 (MAX) → VÁLIDA"""
        assert validar_puntuacion(PUNTUACION_MAX)["valido"] is True

    def test_puntuacion_max_mas_1(self):
        """AVL: puntuación = 6 (MAX+1) → INVÁLIDA"""
        assert validar_puntuacion(PUNTUACION_MAX + 1)["valido"] is False


# ════════════════════════════════════════════════════════════════════════════
# AVL-06  USERNAME LONGITUD  [3 – 20]
# ════════════════════════════════════════════════════════════════════════════
# ┌────────────────┬──────────┬───────────────┐
# │ Entrada        │ Longitud │ Resultado      │
# ├────────────────┼──────────┼───────────────┤
# │ MIN - 1        │ 2        │ Error          │
# │ MIN (límite ↓) │ 3        │ Correcto       │
# │ MIN + 1        │ 4        │ Correcto       │
# │ Interior       │ 10       │ Correcto       │
# │ MAX - 1        │ 19       │ Correcto       │
# │ MAX (límite ↑) │ 20       │ Correcto       │
# │ MAX + 1        │ 21       │ Error          │
# └────────────────┴──────────┴───────────────┘

class TestAVL_UsernameLongitud:
    def test_username_longitud_min_menos_1(self):
        """AVL: username 2 chars (MIN-1) → INVÁLIDO"""
        assert validar_username("ab")["valido"] is False

    def test_username_longitud_min(self):
        """AVL: username 3 chars (MIN) → VÁLIDO"""
        assert validar_username("abc")["valido"] is True

    def test_username_longitud_min_mas_1(self):
        """AVL: username 4 chars (MIN+1) → VÁLIDO"""
        assert validar_username("abcd")["valido"] is True

    def test_username_longitud_interior(self):
        """AVL: username 10 chars (interior) → VÁLIDO"""
        assert validar_username("abcde12345")["valido"] is True

    def test_username_longitud_max_menos_1(self):
        """AVL: username 19 chars (MAX-1) → VÁLIDO"""
        assert validar_username("a" * 19)["valido"] is True

    def test_username_longitud_max(self):
        """AVL: username 20 chars (MAX) → VÁLIDO"""
        assert validar_username("a" * 20)["valido"] is True

    def test_username_longitud_max_mas_1(self):
        """AVL: username 21 chars (MAX+1) → INVÁLIDO"""
        assert validar_username("a" * 21)["valido"] is False


# ════════════════════════════════════════════════════════════════════════════
# AVL-07  MONTO PUJA — INCREMENTO MÍNIMO  (precio_actual = 100.00)
# ════════════════════════════════════════════════════════════════════════════
# ┌─────────────────────────┬────────────────┬───────────────┐
# │ Entrada                 │ Monto (S/)     │ Resultado      │
# ├─────────────────────────┼────────────────┼───────────────┤
# │ Precio actual exacto    │ 100.00         │ Error          │
# │ < incremento mínimo     │ 100.99         │ Error          │
# │ Justo en límite (MIN+1) │ 101.00         │ Correcto       │
# │ Un poco más             │ 101.01         │ Correcto       │
# │ Interior                │ 200.00         │ Correcto       │
# └─────────────────────────┴────────────────┴───────────────┘

class TestAVL_MontoPuja:
    PRECIO_ACTUAL = 100.00

    def test_puja_igual_al_precio_actual(self):
        """AVL: puja = precio_actual (sin incremento) → INVÁLIDA"""
        assert validar_monto_puja(100.00, self.PRECIO_ACTUAL)["valido"] is False

    def test_puja_menor_al_incremento_minimo(self):
        """AVL: puja = precio_actual + 0.99 (< INCREMENTO_MIN) → INVÁLIDA"""
        assert validar_monto_puja(100.99, self.PRECIO_ACTUAL)["valido"] is False

    def test_puja_justo_en_limite_inferior(self):
        """AVL: puja = precio_actual + INCREMENTO_MIN (101.00) → VÁLIDA"""
        assert validar_monto_puja(101.00, self.PRECIO_ACTUAL)["valido"] is True

    def test_puja_un_poco_mas_del_limite(self):
        """AVL: puja = 101.01 (límite + ε) → VÁLIDA"""
        assert validar_monto_puja(101.01, self.PRECIO_ACTUAL)["valido"] is True

    def test_puja_interior(self):
        """AVL: puja = 200.00 (interior) → VÁLIDA"""
        assert validar_monto_puja(200.00, self.PRECIO_ACTUAL)["valido"] is True

    def test_puja_en_maximo(self):
        """AVL: puja = 1_000_000.00 (MAX absoluto) → VÁLIDA"""
        assert validar_monto_puja(PRECIO_MAX, self.PRECIO_ACTUAL)["valido"] is True

    def test_puja_sobre_maximo(self):
        """AVL: puja = 1_000_000.01 (MAX+ε) → INVÁLIDA"""
        assert validar_monto_puja(PRECIO_MAX + 0.01, self.PRECIO_ACTUAL)["valido"] is False


# ════════════════════════════════════════════════════════════════════════════
# AVL-08  NOMBRE ARTÍCULO  [3 – 100]
# ════════════════════════════════════════════════════════════════════════════

class TestAVL_NombreArticulo:
    def test_nombre_min_menos_1(self):
        """AVL: nombre 2 chars (MIN-1) → INVÁLIDO"""
        assert validar_nombre_articulo("ab")["valido"] is False

    def test_nombre_min(self):
        """AVL: nombre 3 chars (MIN) → VÁLIDO"""
        assert validar_nombre_articulo("abc")["valido"] is True

    def test_nombre_min_mas_1(self):
        """AVL: nombre 4 chars (MIN+1) → VÁLIDO"""
        assert validar_nombre_articulo("abcd")["valido"] is True

    def test_nombre_interior(self):
        """AVL: nombre 50 chars (interior) → VÁLIDO"""
        assert validar_nombre_articulo("a" * 50)["valido"] is True

    def test_nombre_max_menos_1(self):
        """AVL: nombre 99 chars (MAX-1) → VÁLIDO"""
        assert validar_nombre_articulo("a" * 99)["valido"] is True

    def test_nombre_max(self):
        """AVL: nombre 100 chars (MAX) → VÁLIDO"""
        assert validar_nombre_articulo("a" * 100)["valido"] is True

    def test_nombre_max_mas_1(self):
        """AVL: nombre 101 chars (MAX+1) → INVÁLIDO"""
        assert validar_nombre_articulo("a" * 101)["valido"] is False


# ════════════════════════════════════════════════════════════════════════════
# AVL-09  SALDO SUFICIENTE  [saldo_usuario ≥ monto_puja]
# ════════════════════════════════════════════════════════════════════════════
# La regla es: saldo ≥ monto_puja.
# El punto crítico (límite inferior) es cuando saldo = monto_puja.
# Se fija monto_puja = 100.00 y se varía el saldo.
# ┌────────────────┤──────────────┤───────────────┐
# │ Entrada       │ Saldo (S/)   │ Resultado     │
# ├────────────────┼──────────────┼───────────────┤
# │ Límite - ε   │ 99.99        │ Error         │
# │ Límite (↓)  │ 100.00       │ Correcto      │
# │ Límite + ε   │ 100.01       │ Correcto      │
# │ Interior      │ 500.00       │ Correcto      │
# │ Saldo cero    │ 0.00         │ Error         │
# │ Saldo negat.  │ -0.01        │ Error         │
# │ Tipo incorr.  │ "cien"       │ Error         │
# └────────────────┴──────────────┴───────────────┘

class TestAVL_SaldoSuficiente:
    MONTO_PUJA = 100.00   # referencia fija

    def test_saldo_limite_menos_epsilon(self):
        """AVL: saldo = 99.99 (límite - ε) → INVÁLIDO"""
        assert validar_saldo_suficiente(99.99, self.MONTO_PUJA)["valido"] is False

    def test_saldo_igual_al_limite(self):
        """AVL: saldo = 100.00 (límite exacto) → VÁLIDO"""
        assert validar_saldo_suficiente(100.00, self.MONTO_PUJA)["valido"] is True

    def test_saldo_limite_mas_epsilon(self):
        """AVL: saldo = 100.01 (límite + ε) → VÁLIDO"""
        assert validar_saldo_suficiente(100.01, self.MONTO_PUJA)["valido"] is True

    def test_saldo_interior(self):
        """AVL: saldo = 500.00 (valor interior) → VÁLIDO"""
        assert validar_saldo_suficiente(500.00, self.MONTO_PUJA)["valido"] is True

    def test_saldo_cero(self):
        """AVL: saldo = 0.00 → INVÁLIDO (no puede pujar)"""
        assert validar_saldo_suficiente(0.00, self.MONTO_PUJA)["valido"] is False

    def test_saldo_negativo_epsilon(self):
        """AVL: saldo = -0.01 (negativo mínimo) → INVÁLIDO"""
        assert validar_saldo_suficiente(-0.01, self.MONTO_PUJA)["valido"] is False

    def test_saldo_tipo_incorrecto(self):
        """AVL: saldo = str → INVÁLIDO (tipo de dato incorrecto)"""
        assert validar_saldo_suficiente("cien", self.MONTO_PUJA)["valido"] is False
