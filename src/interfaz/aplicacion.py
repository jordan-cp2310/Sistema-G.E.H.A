import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

from src.modelos.materia import Materia
from src.interfaz.tema import Tema
from src.interfaz.componentes import TarjetaResumen


class Aplicacion(tk.Tk):
    def __init__(self, sistema):
        super().__init__()
        self.sistema = sistema
        self.title("G.E.H.A. v1.1 · Gestión de Horarios Académicos")
        self.geometry("1200x800")
        self.minsize(1040, 740)
        self.tema = Tema(self)
        self.base_visual = ttk.Frame(self)
        self.base_visual.pack(fill="both", expand=True)
        self.mostrar_acceso()

    def preparar_pantalla(self, titulo, detalle):
        for widget in self.base_visual.winfo_children():
            widget.destroy()
        self.tarjetas = []
        self.tabla = None
        lateral = ttk.Frame(self.base_visual, style="Sidebar.TFrame", padding=22, width=220)
        lateral.pack(side="left", fill="y")
        lateral.pack_propagate(False)
        ttk.Label(lateral, text="G.E.H.A.", style="Brand.Sidebar.TLabel").pack(anchor="w", pady=(14, 4))
        ttk.Label(lateral, text="Gestión de Horarios\nAcadémicos", style="Muted.Sidebar.TLabel").pack(anchor="w")
        ttk.Separator(lateral).pack(fill="x", pady=24)
        usuario = self.sistema.usuario
        if usuario is None:
            rol = "ACCESO AL SISTEMA"
            nombre = "Bienvenido"
            seccion = "Inicio de sesión"
        else:
            nombre = usuario.nombre
            if usuario.permite("usuarios"):
                rol = "ADMINISTRADOR"
                seccion = "Cuentas de planificadores"
            else:
                rol = "PLANIFICADOR"
                seccion = "Catálogo de materias"
        ttk.Label(lateral, text=rol, style="Muted.Sidebar.TLabel", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        ttk.Label(lateral, text=nombre, style="Sidebar.TLabel", wraplength=175).pack(anchor="w", pady=(8, 24))
        ttk.Label(lateral, text=seccion, style="Sidebar.TLabel", wraplength=175).pack(anchor="w")
        pie = ttk.Frame(lateral, style="Sidebar.TFrame")
        pie.pack(side="bottom", fill="x")
        ttk.Label(pie, text="GEHA v1.1", style="Sidebar.TLabel").pack(anchor="w")
        ttk.Label(pie, text="Acceso y materias", style="Muted.Sidebar.TLabel").pack(anchor="w", pady=(4, 16))
        self.boton_tema = ttk.Button(pie, command=self.cambiar_tema, style="Sidebar.TButton")
        self.boton_tema.pack(fill="x")
        if usuario is not None:
            ttk.Button(pie, text="Cerrar sesión", command=self.al_cerrar_sesion,
                       style="Sidebar.TButton").pack(fill="x", pady=(10, 0))
        self.texto_tema()
        self.contenido = ttk.Frame(self.base_visual, padding=24)
        self.contenido.pack(side="left", fill="both", expand=True)
        ttk.Label(self.contenido, text="PANEL DE GESTIÓN", style="Muted.TLabel", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        ttk.Label(self.contenido, text=titulo, style="Titulo.TLabel").pack(anchor="w", pady=(4, 6))
        ttk.Label(self.contenido, text=detalle, style="Muted.TLabel", wraplength=750).pack(anchor="w", pady=(0, 20))

    def texto_tema(self):
        if self.tema.nombre == "claro":
            self.boton_tema.configure(text="Activar tema oscuro")
        else:
            self.boton_tema.configure(text="Activar tema claro")

    def cambiar_tema(self):
        # Solo cambiar estilos: conservar entradas, selección y sesión.
        self.tema.alternar()
        self.texto_tema()
        self.colorear_filas()

    def colorear_filas(self):
        if self.tabla is None:
            return
        self.tabla.tag_configure("alterna", background=self.tema.colores["fila"])
        fila = 0
        for codigo in self.tabla.get_children():
            if fila % 2 == 0:
                self.tabla.item(codigo, tags=("alterna",))
            else:
                self.tabla.item(codigo, tags=())
            fila = fila + 1

    def crear_resumen(self, datos):
        fila = ttk.Frame(self.contenido)
        fila.pack(fill="x", pady=(0, 20))
        columna = 0
        for titulo, detalle in datos:
            tarjeta = TarjetaResumen(fila, titulo, detalle)
            tarjeta.grid(row=0, column=columna, sticky="ew", padx=(0, 10))
            fila.columnconfigure(columna, weight=1, uniform="resumen")
            self.tarjetas.append(tarjeta)
            columna = columna + 1

    def crear_area_trabajo(self, titulo_formulario, titulo_tabla):
        zona = ttk.Frame(self.contenido)
        zona.pack(fill="both", expand=True)
        zona.columnconfigure(1, weight=1)
        zona.rowconfigure(0, weight=1)
        self.panel_formulario = ttk.Frame(zona, style="Card.TFrame", padding=18, width=285)
        self.panel_formulario.grid(row=0, column=0, sticky="ns", padx=(0, 16))
        self.panel_formulario.grid_propagate(False)
        self.panel_formulario.columnconfigure(0, weight=1)
        ttk.Label(self.panel_formulario, text=titulo_formulario, style="Heading.Card.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 16))
        self.panel_tabla = ttk.Frame(zona, style="Card.TFrame", padding=18)
        self.panel_tabla.grid(row=0, column=1, sticky="nsew")
        ttk.Label(self.panel_tabla, text=titulo_tabla, style="Heading.Card.TLabel").pack(anchor="w", pady=(0, 12))

    def formulario(self, campos):
        marco = ttk.Frame(self.panel_formulario, style="Card.TFrame")
        marco.grid(row=1, column=0, sticky="ew")
        marco.columnconfigure(0, weight=1)
        marco.columnconfigure(1, weight=1)
        self.entradas = {}
        fila = 0
        for campo in campos:
            columna = 0
            ancho = 2
            if campo == "Horas de teoría":
                ancho = 1
            if campo == "Horas de práctica":
                columna = 1
                ancho = 1
            ttk.Label(marco, text=campo, style="Muted.Card.TLabel").grid(
                row=fila, column=columna, columnspan=ancho, sticky="w", pady=(0, 4))
            entrada = ttk.Entry(marco, font=("Segoe UI", 10), width=12)
            if "Contraseña" in campo:
                entrada.config(show="*")
            entrada.grid(row=fila + 1, column=columna, columnspan=ancho,
                         sticky="ew", padx=(0, 4), pady=(0, 8))
            self.entradas[campo] = entrada
            if fila == 0:
                entrada.focus_set()
            if campo != "Horas de teoría":
                fila = fila + 2

    def ejecutar(self, accion):
        # Un solo lugar para mostrar los errores esperados de los formularios.
        try:
            accion()
        except (ValueError, PermissionError) as error:
            messagebox.showwarning("Revisa los datos", str(error), parent=self)
        except sqlite3.Error:
            messagebox.showerror("Base de datos", "No se pudo guardar o consultar. Comprueba que la base esté disponible e inténtalo otra vez.", parent=self)

    def botones(self, acciones):
        marco = ttk.Frame(self.panel_formulario, style="Card.TFrame")
        marco.grid(row=2, column=0, sticky="ew", pady=(4, 0))
        fila = 0
        columna = 0
        marco.columnconfigure(0, weight=1)
        marco.columnconfigure(1, weight=1)
        for texto, accion in acciones:
            estilo = "TButton"
            if texto in ("Guardar", "Crear planificador", "Iniciar sesión", "Crear administrador"):
                estilo = "Primary.TButton"
            if texto in ("Eliminar", "Desactivar seleccionado"):
                estilo = "Danger.TButton"
            boton = ttk.Button(marco, text=texto, command=accion, style=estilo)
            if len(acciones) > 2:
                boton.grid(row=fila, column=columna, sticky="ew", padx=(0, 4), pady=(0, 8))
                columna = columna + 1
                if columna == 2:
                    columna = 0
                    fila = fila + 1
            else:
                boton.grid(row=fila, column=0, columnspan=2, sticky="ew", pady=(0, 8))
                fila = fila + 1

    def al_acceder(self):
        self.ejecutar(self.acceder)

    def al_crear_planificador(self):
        self.ejecutar(self.crear_planificador)

    def al_desactivar(self):
        self.ejecutar(self.desactivar)

    def al_guardar(self):
        self.ejecutar(self.guardar_materia)

    def al_eliminar(self):
        self.ejecutar(self.eliminar_materia)

    def al_actualizar(self):
        self.ejecutar(self.actualizar_materias)

    def al_cerrar_sesion(self):
        self.ejecutar(self.mostrar_acceso)

    def mostrar_acceso(self):
        self.sistema.cerrar_sesion()
        self.inicial = self.sistema.necesita_configuracion()
        if self.inicial:
            detalle = "Primera apertura: crea el administrador de esta computadora."
            campos = ("Nombre", "Cuenta", "Contraseña", "Contraseña (repetir)")
            texto_boton = "Crear administrador"
        else:
            detalle = "Ingresa con tu cuenta autorizada."
            campos = ("Cuenta", "Contraseña")
            texto_boton = "Iniciar sesión"
        self.preparar_pantalla("G.E.H.A.", detalle)
        tarjeta = ttk.Frame(self.contenido, style="Card.TFrame", padding=28)
        tarjeta.pack(anchor="center", pady=(18, 0))
        self.panel_formulario = tarjeta
        tarjeta.columnconfigure(0, minsize=350)
        ttk.Label(tarjeta, text="Tu espacio de trabajo académico", style="Heading.Card.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 20))
        self.formulario(campos)
        self.botones([(texto_boton, self.al_acceder)])
        ttk.Label(self.contenido, text="Versión 1.1 · Acceso y catálogo de materias\nLa planificación de horarios se desarrollará en próximas etapas.").pack(anchor="w", pady=18)

    def acceder(self):
        cuenta = self.entradas["Cuenta"].get()
        clave = self.entradas["Contraseña"].get()
        if self.inicial:
            nombre = self.entradas["Nombre"].get()
            repetida = self.entradas["Contraseña (repetir)"].get()
            if clave != repetida:
                raise ValueError("Las contraseñas no coinciden.")
            self.sistema.configurar_administrador(nombre, cuenta, clave)
            self.mostrar_acceso()
            messagebox.showinfo("Configuración lista", "Administrador creado. Ya puedes iniciar sesión.", parent=self)
        else:
            usuario = self.sistema.iniciar_sesion(cuenta, clave)
            if usuario.permite("usuarios"):
                self.mostrar_usuarios()
            else:
                self.mostrar_materias()

    def crear_tabla(self, columnas):
        self.estado = ttk.Label(self.panel_tabla, style="Muted.Card.TLabel", wraplength=370)
        self.estado.pack(side="bottom", anchor="w", pady=(12, 0))
        marco = ttk.Frame(self.panel_tabla, style="Card.TFrame")
        marco.pack(fill="both", expand=True)
        self.tabla = ttk.Treeview(marco, columns=columnas, show="headings", selectmode="browse")
        for columna in columnas:
            self.tabla.heading(columna, text=columna)
            self.tabla.column(columna, width=90, minwidth=55)
        barra = ttk.Scrollbar(marco, orient="vertical", command=self.tabla.yview)
        horizontal = ttk.Scrollbar(marco, orient="horizontal", command=self.tabla.xview)
        self.tabla.configure(yscrollcommand=barra.set, xscrollcommand=horizontal.set)
        marco.rowconfigure(0, weight=1)
        marco.columnconfigure(0, weight=1)
        self.tabla.grid(row=0, column=0, sticky="nsew")
        barra.grid(row=0, column=1, sticky="ns")
        horizontal.grid(row=1, column=0, sticky="ew")

    def mostrar_usuarios(self):
        self.preparar_pantalla("Cuentas de planificadores", f"Administrador: {self.sistema.usuario.nombre} · Contraseñas de al menos 8 caracteres.")
        self.crear_resumen([("Planificadores", "Cuentas registradas"), ("Activos", "Con acceso al sistema"), ("Inactivos", "Acceso deshabilitado")])
        self.crear_area_trabajo("Nuevo planificador", "Cuentas registradas")
        self.formulario(("Nombre", "Cuenta", "Contraseña"))
        self.botones([("Crear planificador", self.al_crear_planificador), ("Desactivar seleccionado", self.al_desactivar)])
        self.crear_tabla(("Nombre", "Cuenta", "Estado"))
        self.actualizar_usuarios()

    def actualizar_usuarios(self):
        filas = self.sistema.listar_planificadores()
        self.vaciar_tabla()
        for fila in filas:
            if fila["activo"]:
                estado = "Activo"
            else:
                estado = "Inactivo"
            self.tabla.insert("", "end", iid=str(fila["codigo"]), values=(fila["nombre"], fila["cuenta"], estado))
        activos = 0
        for fila in filas:
            if fila["activo"]:
                activos = activos + 1
        self.tarjetas[0].actualizar(len(filas))
        self.tarjetas[1].actualizar(activos)
        self.tarjetas[2].actualizar(len(filas) - activos)
        self.colorear_filas()
        self.estado.config(text=f"{len(filas)} cuenta(s) de planificador")

    def crear_planificador(self):
        nombre = self.entradas["Nombre"].get()
        cuenta = self.entradas["Cuenta"].get()
        clave = self.entradas["Contraseña"].get()
        self.sistema.crear_planificador(nombre, cuenta, clave)
        for entrada in self.entradas.values():
            entrada.delete(0, "end")
        self.actualizar_usuarios()
        self.estado.config(text="Cuenta creada correctamente.")

    def seleccionado(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            raise ValueError("Primero selecciona un registro de la tabla.")
        return seleccion[0]

    def desactivar(self):
        codigo = self.seleccionado()
        cuenta = self.tabla.item(codigo, "values")[1]
        if messagebox.askyesno("Desactivar cuenta", f"¿Desactivar la cuenta {cuenta}? Ya no podrá acceder.", parent=self):
            self.sistema.desactivar_planificador(int(codigo))
            self.actualizar_usuarios()

    def mostrar_materias(self):
        self.preparar_pantalla("Catálogo de materias", f"Planificador: {self.sistema.usuario.nombre} · Selecciona una fila para editarla.")
        self.crear_resumen([("Materias", "En el catálogo"), ("Horas semanales", "Suma del catálogo"), ("Niveles", "Niveles registrados")])
        self.crear_area_trabajo("Datos de la materia", "Materias registradas")
        self.formulario(("Código", "Nombre", "Nivel", "Horas de teoría", "Horas de práctica"))
        self.botones([("Nueva / limpiar", self.limpiar_materia), ("Guardar", self.al_guardar), ("Eliminar", self.al_eliminar), ("Actualizar lista", self.al_actualizar)])
        self.crear_tabla(("Código", "Nombre", "Nivel", "Teoría", "Práctica", "Total semanal"))
        self.tabla.column("Nombre", width=210)
        self.tabla.bind("<<TreeviewSelect>>", self.cargar_materia)
        self.codigo_anterior = None
        self.actualizar_materias()

    def actualizar_materias(self):
        materias = self.sistema.listar_materias()
        self.vaciar_tabla()
        for materia in materias:
            valores = (materia.codigo, materia.nombre, materia.nivel, materia.horas_teoria, materia.horas_practica, materia.horas_semanales)
            self.tabla.insert("", "end", iid=materia.codigo, values=valores)
        horas = 0
        niveles = []
        for materia in materias:
            horas = horas + materia.horas_semanales
            if materia.nivel not in niveles:
                niveles.append(materia.nivel)
        self.tarjetas[0].actualizar(len(materias))
        self.tarjetas[1].actualizar(horas)
        self.tarjetas[2].actualizar(len(niveles))
        self.colorear_filas()
        self.limpiar_materia()
        self.estado.config(text=f"{len(materias)} materia(s) · Horas semanales enteras; total mayor que cero.")

    def limpiar_materia(self):
        self.codigo_anterior = None
        for codigo in self.tabla.selection():
            self.tabla.selection_remove(codigo)
        for entrada in self.entradas.values():
            entrada.delete(0, "end")
        self.entradas["Código"].focus_set()

    def cargar_materia(self, evento=None):
        if not self.tabla.selection():
            return
        self.codigo_anterior = self.seleccionado()
        valores = self.tabla.item(self.codigo_anterior, "values")
        self.escribir_campo("Código", valores[0])
        self.escribir_campo("Nombre", valores[1])
        self.escribir_campo("Nivel", valores[2])
        self.escribir_campo("Horas de teoría", valores[3])
        self.escribir_campo("Horas de práctica", valores[4])

    def escribir_campo(self, nombre, valor):
        entrada = self.entradas[nombre]
        entrada.delete(0, "end")
        entrada.insert(0, valor)

    def vaciar_tabla(self):
        for codigo in self.tabla.get_children():
            self.tabla.delete(codigo)

    def guardar_materia(self):
        codigo = self.entradas["Código"].get()
        nombre = self.entradas["Nombre"].get()
        try:
            nivel = int(self.entradas["Nivel"].get())
            teoria = int(self.entradas["Horas de teoría"].get())
            practica = int(self.entradas["Horas de práctica"].get())
        except ValueError:
            raise ValueError("Completa el nivel y las horas con números enteros.")
        materia = Materia(codigo, nombre, nivel, teoria, practica)
        self.sistema.guardar_materia(materia, self.codigo_anterior)
        self.actualizar_materias()
        self.estado.config(text=f"Materia {materia.codigo} guardada correctamente.")

    def eliminar_materia(self):
        codigo = self.seleccionado()
        if messagebox.askyesno("Eliminar materia", f"¿Eliminar la materia {codigo}?", parent=self):
            self.sistema.eliminar_materia(codigo)
            self.actualizar_materias()
