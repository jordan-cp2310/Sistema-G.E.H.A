"""Una tarjeta reutilizable para los dos dashboards."""
from tkinter import ttk


class TarjetaResumen(ttk.Frame):
    def __init__(self, padre, titulo, detalle):
        super().__init__(padre, style="Card.TFrame", padding=16)
        ttk.Label(self, text=titulo, style="Muted.Card.TLabel").pack(anchor="w")
        self.valor = ttk.Label(self, text="0", style="Number.Card.TLabel")
        self.valor.pack(anchor="w", pady=(4, 2))
        ttk.Label(self, text=detalle, style="Muted.Card.TLabel").pack(anchor="w")

    def actualizar(self, valor):
        self.valor.configure(text=str(valor))
