"""
Modelos de datos para la Plataforma de Subastas Online.
"""
from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime


@dataclass
class Usuario:
    username: str
    email: str
    password: str
    edad: int
    saldo: float = 0.0
    activo: bool = True
    # Historial de subastas ganadas (registrado al cerrar una subasta)
    subastas_ganadas: List[dict] = field(default_factory=list)

    def __str__(self):
        return f"Usuario({self.username}, edad={self.edad}, saldo=S/{self.saldo:.2f})"


@dataclass
class Articulo:
    id: int
    nombre: str
    descripcion: str
    precio_base: float
    vendedor: str
    categoria: str
    activo: bool = True

    def __str__(self):
        return f"Artículo[{self.id}] {self.nombre} - Base: S/{self.precio_base:.2f}"


@dataclass
class Puja:
    articulo_id: int
    postor: str
    monto: float
    timestamp: datetime = field(default_factory=datetime.now)

    def __str__(self):
        return f"Puja: {self.postor} → S/{self.monto:.2f}"


@dataclass
class Subasta:
    articulo: Articulo
    pujas: List[Puja] = field(default_factory=list)
    ganador: Optional[str] = None
    cerrada: bool = False

    def precio_actual(self) -> float:
        if not self.pujas:
            return self.articulo.precio_base
        return max(p.monto for p in self.pujas)

    def puja_ganadora(self) -> Optional[Puja]:
        if not self.pujas:
            return None
        return max(self.pujas, key=lambda p: p.monto)

    def __str__(self):
        estado = "Cerrada" if self.cerrada else "Activa"
        return (f"Subasta [{estado}] → {self.articulo.nombre} | "
                f"Precio actual: S/{self.precio_actual():.2f} | "
                f"Pujas: {len(self.pujas)}")
