#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════╗
║  🏷️  PLATAFORMA DE SUBASTAS ONLINE — Tkinter GUI   ║
╚══════════════════════════════════════════════════════╝

Interfaz gráfica simple con Tkinter.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from app.auth import SistemaAuth
from app.auction import SistemaSubastas

# ─── Paleta de colores ────────────────────────────────────────────────────────
BG       = "#f1f5f9"
BG_DARK  = "#1e293b"
PANEL    = "#ffffff"
SIDEBAR  = "#1e2d5a"
ACCENT   = "#4f46e5"
ACCENT2  = "#818cf8"
SUCCESS  = "#16a34a"
DANGER   = "#dc2626"
WARNING  = "#d97706"
TEXT     = "#1e293b"
TEXT_MUT = "#64748b"
BORDER   = "#e2e8f0"

# ─── Fuentes ──────────────────────────────────────────────────────────────────
FONT_TITLE  = ("Helvetica", 18, "bold")
FONT_SECT   = ("Helvetica", 13, "bold")
FONT_LABEL  = ("Helvetica", 10)
FONT_ENTRY  = ("Helvetica", 10)
FONT_BTN    = ("Helvetica", 10, "bold")
FONT_MONO   = ("Courier", 10)
FONT_SMALL  = ("Helvetica", 9)


# ═══════════════════════════════════════════════════════════════════════════════
class SubastaApp(tk.Tk):
    """Aplicación principal."""

    def __init__(self):
        super().__init__()
        self.title("🏷️ Plataforma de Subastas Online")
        self.geometry("820x620")
        self.minsize(700, 500)
        self.configure(bg=BG)

        # Sistemas de negocio
        self.auth    = SistemaAuth()
        self.sistema = SistemaSubastas(self.auth)
        self.usuario = None                # Usuario actualmente en sesión

        self._build_header()
        self._build_sidebar()
        self._build_content()
        self._build_statusbar()

        self.mostrar_login()

    # ── Layout principal ───────────────────────────────────────────────────────
    def _build_header(self):
        hdr = tk.Frame(self, bg=SIDEBAR, height=54)
        hdr.pack(fill=tk.X, side=tk.TOP)
        hdr.pack_propagate(False)
        tk.Label(hdr, text="🏷️  Plataforma de Subastas Online",
                 font=("Helvetica", 15, "bold"), fg="white", bg=SIDEBAR
                 ).pack(side=tk.LEFT, padx=20, pady=10)
        tk.Label(hdr, text="Pruebas de Caja Negra — Python",
                 font=FONT_SMALL, fg=ACCENT2, bg=SIDEBAR
                 ).pack(side=tk.RIGHT, padx=20)

    def _build_sidebar(self):
        self.sidebar = tk.Frame(self, bg=SIDEBAR, width=180)
        self.sidebar.pack(fill=tk.Y, side=tk.LEFT)
        self.sidebar.pack_propagate(False)

        tk.Label(self.sidebar, text="MENÚ", font=("Helvetica", 9, "bold"),
                 fg=ACCENT2, bg=SIDEBAR).pack(pady=(16, 6), padx=16, anchor="w")

        self.nav_btns = {}
        menu_items = [
            ("🔐", "Iniciar Sesión",       self.mostrar_login),
            ("📝", "Registrarse",           self.mostrar_registro),
            ("💰", "Depositar Saldo",       self.mostrar_depositar),
            ("📦", "Publicar Artículo",     self.mostrar_publicar),
            ("🔍", "Ver Subastas",          self.mostrar_subastas),
            ("⚡", "Realizar Puja",         self.mostrar_pujar),
            ("🔒", "Cerrar Subasta",        self.mostrar_cerrar),
            ("🏆", "Mis Compras",           self.mostrar_ganadas),
            ("⭐", "Calificar Vendedor",    self.mostrar_calificar),
            ("🚪", "Cerrar Sesión",         self._cerrar_sesion),
        ]
        for icon, label, cmd in menu_items:
            btn = tk.Button(
                self.sidebar, text=f"  {icon}  {label}",
                font=FONT_SMALL, fg="white", bg=SIDEBAR,
                activebackground=ACCENT, activeforeground="white",
                bd=0, relief="flat", anchor="w", padx=10, pady=8,
                cursor="hand2", command=cmd
            )
            btn.pack(fill=tk.X, padx=4)
            self.nav_btns[label] = btn

    def _build_content(self):
        self.content = tk.Frame(self, bg=BG)
        self.content.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

    def _build_statusbar(self):
        self.status_var = tk.StringVar(value="  Sin sesión activa")
        bar = tk.Label(self, textvariable=self.status_var,
                       bg=BG_DARK, fg=TEXT_MUT,
                       font=FONT_SMALL, anchor="w", padx=12, pady=5)
        bar.pack(fill=tk.X, side=tk.BOTTOM)

    def _update_status(self):
        if self.usuario:
            self.status_var.set(
                f"  👤 {self.usuario.username}   |   "
                f"💰 Saldo: S/{self.usuario.saldo:.2f}"
            )
        else:
            self.status_var.set("  Sin sesión activa")

    # ── Helpers de UI ──────────────────────────────────────────────────────────
    def _clear(self):
        for w in self.content.winfo_children():
            w.destroy()

    def _panel(self, title=""):
        """Crea un panel con título y retorna el frame de contenido."""
        frame = tk.Frame(self.content, bg=BG)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        if title:
            tk.Label(frame, text=title, font=FONT_SECT,
                     fg=TEXT, bg=BG).pack(anchor="w", pady=(0, 14))
            ttk.Separator(frame, orient="horizontal").pack(fill=tk.X, pady=(0, 14))
        return frame

    def _lbl(self, parent, text):
        tk.Label(parent, text=text, font=FONT_LABEL,
                 fg=TEXT_MUT, bg=BG).pack(anchor="w", pady=(6, 1))

    def _entry(self, parent, show=None):
        e = tk.Entry(parent, font=FONT_ENTRY, fg=TEXT, bg=PANEL,
                     relief="solid", bd=1, show=show or "")
        e.pack(fill=tk.X, ipady=5, pady=(0, 2))
        return e

    def _btn(self, parent, text, cmd, color=ACCENT, width=None):
        b = tk.Button(parent, text=text, font=FONT_BTN,
                      bg=color, fg="white", activebackground=ACCENT2,
                      activeforeground="white", bd=0, relief="flat",
                      padx=16, pady=8, cursor="hand2", command=cmd)
        if width:
            b.config(width=width)
        b.pack(pady=6, anchor="w")
        return b

    def _result_box(self, parent):
        box = scrolledtext.ScrolledText(
            parent, font=FONT_MONO, fg=TEXT, bg="#f8fafc",
            height=8, relief="solid", bd=1, state="disabled"
        )
        box.pack(fill=tk.BOTH, expand=True, pady=6)
        return box

    def _write(self, box, text, tag=None):
        box.config(state="normal")
        box.insert(tk.END, text + "\n")
        box.see(tk.END)
        box.config(state="disabled")

    def _clear_box(self, box):
        box.config(state="normal")
        box.delete("1.0", tk.END)
        box.config(state="disabled")

    def _need_login(self):
        if not self.usuario:
            messagebox.showwarning("Sesión requerida",
                                   "Debes iniciar sesión para acceder a esta función.")
            self.mostrar_login()
            return True
        return False

    def _cerrar_sesion(self):
        if self.usuario:
            nombre = self.usuario.username
            self.usuario = None
            self._update_status()
            messagebox.showinfo("Sesión cerrada", f"¡Hasta pronto, {nombre}!")
        self.mostrar_login()

    # ══════════════════════════════════════════════════════════════════════════
    # PANTALLAS
    # ══════════════════════════════════════════════════════════════════════════

    # ── LOGIN ──────────────────────────────────────────────────────────────────
    def mostrar_login(self):
        self._clear()
        f = self._panel("🔐 Iniciar Sesión")

        self._lbl(f, "Nombre de usuario")
        e_user = self._entry(f)

        self._lbl(f, "Contraseña")
        e_pass = self._entry(f, show="●")

        lbl_res = tk.Label(f, text="", font=FONT_LABEL, bg=BG)
        lbl_res.pack(anchor="w", pady=(4, 0))

        def login():
            r = self.auth.login(e_user.get().strip(), e_pass.get())
            if r["exito"]:
                self.usuario = r["usuario"]
                self._update_status()
                lbl_res.config(text=f"✓ {r['mensaje']}", fg=SUCCESS)
                self.after(800, self.mostrar_subastas)
            else:
                lbl_res.config(text=f"✗ {r['mensaje']}", fg=DANGER)

        self._btn(f, "  Iniciar Sesión  ", login)

        tk.Label(f, text="¿No tienes cuenta?", font=FONT_SMALL,
                 fg=TEXT_MUT, bg=BG).pack(anchor="w", pady=(10, 0))
        tk.Button(f, text="Registrarse aquí →", font=FONT_SMALL,
                  fg=ACCENT, bg=BG, bd=0, cursor="hand2",
                  command=self.mostrar_registro).pack(anchor="w")

        e_user.focus()

    # ── REGISTRO ───────────────────────────────────────────────────────────────
    def mostrar_registro(self):
        self._clear()
        f = self._panel("📝 Registro de Usuario")

        self._lbl(f, "Nombre de usuario (3-20 chars, alfanumérico)")
        e_user = self._entry(f)
        self._lbl(f, "Email")
        e_email = self._entry(f)
        self._lbl(f, "Contraseña (mín 8 chars, 1 mayúscula, 1 número)")
        e_pass = self._entry(f, show="●")
        self._lbl(f, "Edad (18-100)")
        e_edad = self._entry(f)

        lbl_res = tk.Label(f, text="", font=FONT_LABEL, bg=BG, wraplength=420)
        lbl_res.pack(anchor="w", pady=(4, 0))

        def registrar():
            try:
                edad = int(e_edad.get().strip())
            except ValueError:
                edad = e_edad.get().strip()
            r = self.auth.registrar(
                e_user.get().strip(), e_email.get().strip(),
                e_pass.get(), edad
            )
            if r["exito"]:
                lbl_res.config(text=f"✓ {r['mensaje']}", fg=SUCCESS)
                e_user.delete(0, tk.END); e_email.delete(0, tk.END)
                e_pass.delete(0, tk.END); e_edad.delete(0, tk.END)
            else:
                lbl_res.config(text=f"✗ {r['mensaje']}", fg=DANGER)

        self._btn(f, "  Registrarse  ", registrar)

        tk.Button(f, text="← Volver al login", font=FONT_SMALL,
                  fg=ACCENT, bg=BG, bd=0, cursor="hand2",
                  command=self.mostrar_login).pack(anchor="w")

    # ── DEPOSITAR ──────────────────────────────────────────────────────────────
    def mostrar_depositar(self):
        if self._need_login():
            return
        self._clear()
        f = self._panel("💰 Depositar Saldo")

        tk.Label(f, text=f"Saldo actual: S/{self.usuario.saldo:.2f}",
                 font=FONT_LABEL, fg=SUCCESS, bg=BG).pack(anchor="w", pady=(0, 10))

        self._lbl(f, "Monto a depositar S/ (10.00 – 50,000.00)")
        e_monto = self._entry(f)

        lbl_res = tk.Label(f, text="", font=FONT_LABEL, bg=BG, wraplength=420)
        lbl_res.pack(anchor="w", pady=(4, 0))

        def depositar():
            try:
                monto = float(e_monto.get().strip())
            except ValueError:
                monto = e_monto.get().strip()
            r = self.sistema.depositar_saldo(self.usuario, monto)
            if r["exito"]:
                lbl_res.config(text=f"✓ {r['mensaje']}", fg=SUCCESS)
                self._update_status()
                saldo_lbl.config(text=f"Saldo actual: S/{self.usuario.saldo:.2f}")
                e_monto.delete(0, tk.END)
            else:
                lbl_res.config(text=f"✗ {r['mensaje']}", fg=DANGER)

        saldo_lbl = tk.Label(f, text=f"Saldo actual: S/{self.usuario.saldo:.2f}",
                             font=FONT_LABEL, fg=SUCCESS, bg=BG)
        self._btn(f, "  Depositar  ", depositar)

    # ── PUBLICAR ARTÍCULO ──────────────────────────────────────────────────────
    def mostrar_publicar(self):
        if self._need_login():
            return
        self._clear()
        f = self._panel("📦 Publicar Artículo en Subasta")

        self._lbl(f, "Nombre del artículo (3-100 chars)")
        e_nombre = self._entry(f)
        self._lbl(f, "Descripción")
        e_desc = self._entry(f)
        self._lbl(f, "Precio base S/ (1.00 – 1,000,000.00)")
        e_precio = self._entry(f)
        self._lbl(f, "Categoría: electronica | ropa | hogar | arte | vehiculos | coleccionables | deportes | otros")
        e_cat = self._entry(f)

        lbl_res = tk.Label(f, text="", font=FONT_LABEL, bg=BG, wraplength=420)
        lbl_res.pack(anchor="w", pady=(4, 0))

        def publicar():
            try:
                precio = float(e_precio.get().strip())
            except ValueError:
                precio = e_precio.get().strip()
            r = self.sistema.publicar_articulo(
                e_nombre.get().strip(), e_desc.get().strip(),
                precio, self.usuario.username, e_cat.get().strip()
            )
            if r["exito"]:
                sid = r["subasta"].articulo.id
                lbl_res.config(
                    text=f"✓ {r['mensaje']}  (ID de subasta: {sid})", fg=SUCCESS)
                for e in [e_nombre, e_desc, e_precio, e_cat]:
                    e.delete(0, tk.END)
            else:
                lbl_res.config(text=f"✗ {r['mensaje']}", fg=DANGER)

        self._btn(f, "  Publicar Artículo  ", publicar)

    # ── VER SUBASTAS ───────────────────────────────────────────────────────────
    def mostrar_subastas(self):
        self._clear()
        f = self._panel("🔍 Subastas Activas")

        box = self._result_box(f)

        def cargar():
            self._clear_box(box)
            lista = self.sistema.listar_subastas(solo_activas=True)
            if not lista:
                self._write(box, "  No hay subastas activas en este momento.")
            else:
                for s in lista:
                    self._write(box,
                        f"  ID {s.articulo.id} │ {s.articulo.nombre}\n"
                        f"     Precio actual: S/{s.precio_actual():.2f}"
                        f"  │  Pujas: {len(s.pujas)}"
                        f"  │  Vendedor: {s.articulo.vendedor}\n"
                        f"     Categoría: {s.articulo.categoria}\n"
                        f"  {'─'*50}"
                    )

        self._btn(f, "🔄 Actualizar lista", cargar, color="#475569")
        cargar()

    # ── REALIZAR PUJA ──────────────────────────────────────────────────────────
    def mostrar_pujar(self):
        if self._need_login():
            return
        self._clear()
        f = self._panel("⚡ Realizar Puja")

        tk.Label(f, text=f"Tu saldo disponible: S/{self.usuario.saldo:.2f}",
                 font=FONT_LABEL, fg=SUCCESS, bg=BG).pack(anchor="w", pady=(0, 8))

        # Lista de subastas activas arriba
        box = self._result_box(f)
        lista = self.sistema.listar_subastas(solo_activas=True)
        if not lista:
            self._write(box, "  No hay subastas activas.")
        else:
            for s in lista:
                self._write(box,
                    f"  ID {s.articulo.id} │ {s.articulo.nombre}"
                    f"  │ Precio actual: S/{s.precio_actual():.2f}"
                    f"  │ Vendedor: {s.articulo.vendedor}"
                )

        frame_form = tk.Frame(f, bg=BG)
        frame_form.pack(fill=tk.X, pady=(8, 0))

        tk.Label(frame_form, text="ID de subasta:", font=FONT_LABEL,
                 fg=TEXT_MUT, bg=BG).grid(row=0, column=0, sticky="w", padx=(0, 8))
        e_id = tk.Entry(frame_form, font=FONT_ENTRY, width=8, relief="solid", bd=1)
        e_id.grid(row=0, column=1, sticky="w", ipady=4)

        tk.Label(frame_form, text="Monto S/:", font=FONT_LABEL,
                 fg=TEXT_MUT, bg=BG).grid(row=0, column=2, sticky="w", padx=(14, 8))
        e_monto = tk.Entry(frame_form, font=FONT_ENTRY, width=12, relief="solid", bd=1)
        e_monto.grid(row=0, column=3, sticky="w", ipady=4)

        lbl_res = tk.Label(f, text="", font=FONT_LABEL, bg=BG, wraplength=420)
        lbl_res.pack(anchor="w", pady=(4, 0))

        def pujar():
            try:
                art_id = int(e_id.get().strip())
            except ValueError:
                art_id = e_id.get().strip()
            try:
                monto = float(e_monto.get().strip())
            except ValueError:
                monto = e_monto.get().strip()
            r = self.sistema.realizar_puja(art_id, self.usuario.username, monto)
            if r["exito"]:
                lbl_res.config(text=f"✓ {r['mensaje']}", fg=SUCCESS)
                e_id.delete(0, tk.END); e_monto.delete(0, tk.END)
            else:
                lbl_res.config(text=f"✗ {r['mensaje']}", fg=DANGER)

        tk.Button(frame_form, text=" Pujar ", font=FONT_BTN,
                  bg=ACCENT, fg="white", bd=0, relief="flat",
                  padx=12, pady=5, cursor="hand2",
                  command=pujar).grid(row=0, column=4, padx=(14, 0))

    # ── CERRAR SUBASTA ─────────────────────────────────────────────────────────
    def mostrar_cerrar(self):
        if self._need_login():
            return
        self._clear()
        f = self._panel("🔒 Cerrar Subasta")

        tk.Label(f, text="Solo el vendedor puede cerrar su subasta.",
                 font=FONT_SMALL, fg=TEXT_MUT, bg=BG).pack(anchor="w", pady=(0, 10))

        box = self._result_box(f)
        lista = self.sistema.listar_subastas(solo_activas=True)
        for s in lista:
            if s.articulo.vendedor == self.usuario.username:
                self._write(box,
                    f"  ID {s.articulo.id} │ {s.articulo.nombre}"
                    f"  │ Pujas: {len(s.pujas)}"
                    f"  │ Precio actual: S/{s.precio_actual():.2f}"
                )
        if not any(s.articulo.vendedor == self.usuario.username for s in lista):
            self._write(box, "  No tienes subastas activas que cerrar.")

        self._lbl(f, "ID de la subasta a cerrar")
        e_id = self._entry(f)
        e_id.config(width=10)

        lbl_res = tk.Label(f, text="", font=FONT_LABEL, bg=BG, wraplength=420)
        lbl_res.pack(anchor="w", pady=(4, 0))

        def cerrar():
            try:
                art_id = int(e_id.get().strip())
            except ValueError:
                art_id = e_id.get().strip()
            r = self.sistema.cerrar_subasta(art_id, self.usuario.username)
            if r["exito"]:
                msg = r["mensaje"]
                if r.get("ganador"):
                    msg += f"\n🏆 Ganador: {r['ganador']} | Monto: S/{r['monto_final']:.2f}"
                lbl_res.config(text=f"✓ {msg}", fg=SUCCESS)
                self._update_status()
                e_id.delete(0, tk.END)
                # Refrescar lista
                self._clear_box(box)
                lista2 = self.sistema.listar_subastas(solo_activas=True)
                for s in lista2:
                    if s.articulo.vendedor == self.usuario.username:
                        self._write(box,
                            f"  ID {s.articulo.id} │ {s.articulo.nombre}"
                            f"  │ Precio actual: S/{s.precio_actual():.2f}"
                        )
            else:
                lbl_res.config(text=f"✗ {r['mensaje']}", fg=DANGER)

        self._btn(f, "  Cerrar Subasta  ", cerrar, color=DANGER)

    # ── MIS COMPRAS (SUBASTAS GANADAS) ─────────────────────────────────────────
    def mostrar_ganadas(self):
        if self._need_login():
            return
        self._clear()
        f = self._panel("🏆 Mis Subastas Ganadas")

        tk.Label(f, text="Artículos que has comprado al ganar subastas.",
                 font=FONT_SMALL, fg=TEXT_MUT, bg=BG).pack(anchor="w", pady=(0, 10))

        box = self._result_box(f)

        def cargar():
            self._clear_box(box)
            r = self.sistema.ver_subastas_ganadas(self.usuario.username)
            ganadas = r.get("ganadas", [])
            if not ganadas:
                self._write(box, "  Aún no has ganado ninguna subasta.")
            else:
                for i, compra in enumerate(ganadas, 1):
                    self._write(box,
                        f"  #{i}  {compra['nombre']}\n"
                        f"       Categoría : {compra['categoria']}\n"
                        f"       Vendedor  : {compra['vendedor']}\n"
                        f"       Pagado    : S/{compra['monto_pagado']:.2f}"
                        f"  (base S/{compra['precio_base']:.2f})\n"
                        f"  {'─'*50}"
                    )
                self._write(box, f"\n  Total de compras: {len(ganadas)}")

        self._update_status()
        self._btn(f, "🔄 Actualizar", cargar, color="#475569")
        cargar()

    # ── CALIFICAR VENDEDOR ─────────────────────────────────────────────────────
    def mostrar_calificar(self):
        if self._need_login():
            return
        self._clear()
        f = self._panel("⭐ Calificar Vendedor")

        self._lbl(f, "Nombre del vendedor")
        e_vend = self._entry(f)
        self._lbl(f, "Puntuación (1-5)")
        e_punt = self._entry(f)

        lbl_res = tk.Label(f, text="", font=FONT_LABEL, bg=BG, wraplength=420)
        lbl_res.pack(anchor="w", pady=(4, 0))

        def calificar():
            try:
                punt = int(e_punt.get().strip())
            except ValueError:
                punt = e_punt.get().strip()
            r = self.sistema.calificar_vendedor(
                e_vend.get().strip(), self.usuario.username, punt
            )
            if r["exito"]:
                lbl_res.config(text=f"✓ {r['mensaje']}", fg=SUCCESS)
                e_vend.delete(0, tk.END); e_punt.delete(0, tk.END)
            else:
                lbl_res.config(text=f"✗ {r['mensaje']}", fg=DANGER)

        self._btn(f, "  Calificar  ", calificar)


# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = SubastaApp()
    app.mainloop()
