# 🏷️ Plataforma de Subastas Online — Guerra de Testers

Sistema diseñado para el curso de **Pruebas de Software** — actividad *Guerra de Testers*.

Implementa **Pruebas de Caja Negra** completas:
- 🗂️ Partición de Equivalencia (PE) — 60 casos
- 📏 Análisis de Valores Límite (AVL) — 63 casos
- ✅ **Total: 123 tests · 100% pasando**

---

## 📁 Estructura del proyecto

```
testvs/
├── app/
│   ├── __init__.py
│   ├── models.py         # Modelos: Usuario, Articulo, Puja, Subasta
│   ├── validations.py    # Núcleo de validaciones (Black Box Testing)
│   ├── auction.py        # Lógica de subastas + cobro al ganador
│   └── auth.py           # Autenticación de usuarios
├── tests/
│   ├── __init__.py
│   ├── test_pe.py        # Pruebas de Partición de Equivalencia (60 casos)
│   └── test_avl.py       # Pruebas de Análisis de Valores Límite (63 casos)
├── gui.py                # Interfaz gráfica Tkinter (único punto de entrada)
├── requirements.txt
└── README.md
```

---

## ⚙️ Requisitos previos

- Python 3.10 o superior
- `tkinter` incluido con Python (en Ubuntu/WSL puede necesitar instalación)
- `pytest` para las pruebas

---

## 🚀 Instalación y ejecución (Windows WSL / Ubuntu)

### 1. Clonar o descargar el proyecto

```bash
cd ~
# Si usas git:
git clone <URL_DEL_REPO> testvs
cd testvs

# O si ya tienes la carpeta:
cd testvs
```

### 2. Instalar tkinter (solo si no está instalado)

```bash
sudo apt update
sudo apt install python3-tk -y
```

### 3. Crear y activar entorno virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5. Ejecutar la aplicación (interfaz gráfica)

```bash
python3 gui.py
```

> **Nota WSL:** Si aparece el error `cannot connect to X server`, necesitas un servidor X instalado en Windows.  
> Opciones: [VcXsrv](https://sourceforge.net/projects/vcxsrv/), [Xming](https://sourceforge.net/projects/xming/), o usar **WSLg** (Windows 11 lo incluye por defecto).  
> Con WSLg no necesitas configuración adicional.

---

## 🧪 Ejecutar las pruebas

```bash
# Activar el entorno virtual primero:
source .venv/bin/activate

# Todas las pruebas (PE + AVL):
python3 -m pytest tests/ -v

# Solo Partición de Equivalencia:
python3 -m pytest tests/test_pe.py -v

# Solo Análisis de Valores Límite:
python3 -m pytest tests/test_avl.py -v

# Resumen corto:
python3 -m pytest tests/ -v --tb=short

# Con reporte de cobertura:
python3 -m pytest tests/ --cov=app --cov-report=term-missing
```

**Resultado esperado:**
```
123 passed in 0.08s
```

---

## 🎮 Funcionalidades del sistema

| Función | Descripción |
|---------|-------------|
| Registro | Crea cuenta con validación de username, email, password y edad |
| Login | Inicia sesión con credenciales válidas |
| Depositar | Agrega saldo a la cuenta (S/10 – S/50,000) |
| Publicar artículo | Crea una subasta con precio base y categoría |
| Ver subastas | Lista todas las subastas activas |
| Realizar puja | Puja verificando saldo suficiente e incremento mínimo |
| Cerrar subasta | Cobra al ganador y acredita al vendedor automáticamente |
| Mis compras 🏆 | Historial de subastas ganadas con montos pagados |
| Calificar | Calificación 1–5 al vendedor |

---

## 📋 Reglas de negocio (validaciones clave)

| Campo | Regla |
|-------|-------|
| Username | 3 ≤ len ≤ 20, solo `[a-zA-Z0-9_]` |
| Password | 8 ≤ len ≤ 64, ≥1 mayúscula, ≥1 dígito |
| Edad | 18 ≤ edad ≤ 100 (entero) |
| Precio base | S/1.00 ≤ precio ≤ S/1,000,000.00 |
| Monto puja | monto ≥ precio_actual + S/1.00 |
| Saldo puja | saldo_usuario ≥ monto_puja |
| Depósito | S/10.00 ≤ monto ≤ S/50,000.00 |
| Puntuación | 1 ≤ puntuacion ≤ 5 (entero) |

---

## 🏗️ Tecnologías

- **Python 3.10+**
- **Tkinter** — interfaz gráfica
- **pytest** — framework de pruebas
- **pytest-cov** — cobertura de código

