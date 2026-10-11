"""Colores y estilos: solo presentación, sin consultas ni permisos."""
from tkinter import ttk


class Tema:
    def __init__(self, ventana):
        self.ventana = ventana
        self.nombre = "claro"
        self.estilo = ttk.Style(ventana)
        self.estilo.theme_use("clam")
        self.aplicar()

    def alternar(self):
        if self.nombre == "claro":
            self.nombre = "oscuro"
        else:
            self.nombre = "claro"
        self.aplicar()

    def aplicar(self):
        if self.nombre == "claro":
            self.colores = {"fondo": "#F3F5FA", "tarjeta": "#FFFFFF",
                "texto": "#17243B", "suave": "#52627A", "borde": "#D7DFEC",
                "acento": "#315DDF", "hover": "#2449BB", "fila": "#F0F4FA"}
        else:
            self.colores = {"fondo": "#111A2B", "tarjeta": "#1B2940",
                "texto": "#F0F4FC", "suave": "#B3C2D9", "borde": "#354762",
                "acento": "#426DEB", "hover": "#3459CB", "fila": "#22324A"}
        c = self.colores
        s = self.estilo
        self.ventana.configure(background=c["fondo"])
        s.configure("TFrame", background=c["fondo"])
        s.configure("Card.TFrame", background=c["tarjeta"])
        s.configure("TLabel", background=c["fondo"], foreground=c["texto"], font=("Segoe UI", 10))
        s.configure("Muted.TLabel", foreground=c["suave"])
        s.configure("Titulo.TLabel", font=("Segoe UI", 24, "bold"))
        s.configure("Card.TLabel", background=c["tarjeta"])
        s.configure("Muted.Card.TLabel", foreground=c["suave"])
        s.configure("Heading.Card.TLabel", font=("Segoe UI", 13, "bold"))
        s.configure("Number.Card.TLabel", font=("Segoe UI", 25, "bold"), foreground=c["texto"])
        s.configure("Sidebar.TFrame", background="#172B50")
        s.configure("Sidebar.TLabel", background="#172B50", foreground="#FFFFFF")
        s.configure("Brand.Sidebar.TLabel", font=("Segoe UI", 25, "bold"))
        s.configure("Muted.Sidebar.TLabel", foreground="#BECEE7")
        s.configure("TEntry", fieldbackground=c["tarjeta"], foreground=c["texto"],
                    insertcolor=c["texto"], bordercolor=c["borde"], padding=6)
        s.map("TEntry", bordercolor=[("focus", c["acento"])])
        s.configure("TButton", font=("Segoe UI", 10), padding=(8, 8),
                    background=c["tarjeta"], foreground=c["texto"], bordercolor=c["borde"])
        s.map("TButton", background=[("active", c["fila"])])
        s.configure("Primary.TButton", background=c["acento"], foreground="#FFFFFF", borderwidth=0)
        s.map("Primary.TButton", background=[("active", c["hover"])], foreground=[("active", "#FFFFFF")])
        s.configure("Danger.TButton", foreground="#B91C3C")
        if self.nombre == "oscuro":
            s.configure("Danger.TButton", foreground="#FFADB9")
        s.configure("Sidebar.TButton", background="#223D68", foreground="#FFFFFF", borderwidth=0)
        s.map("Sidebar.TButton", background=[("active", "#31517F")], foreground=[("active", "#FFFFFF")])
        s.configure("Treeview", background=c["tarjeta"], fieldbackground=c["tarjeta"],
                    foreground=c["texto"], rowheight=36, font=("Segoe UI", 10), borderwidth=0)
        s.configure("Treeview.Heading", background=c["fila"], foreground=c["suave"],
                    font=("Segoe UI", 10, "bold"), padding=10, relief="flat")
        s.map("Treeview", background=[("selected", c["acento"])], foreground=[("selected", "#FFFFFF")])
        s.map("Treeview.Heading", background=[("active", c["fila"])])
        s.configure("TScrollbar", background=c["borde"], troughcolor=c["tarjeta"], borderwidth=0)
