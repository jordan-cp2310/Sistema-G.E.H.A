import sqlite3
from pathlib import Path

from src.modelos.materia import Materia
from src.modelos.usuario import Administrador, PlanificadorAcademico


class BaseDatos:
    def __init__(self, ruta):
        Path(ruta).parent.mkdir(parents=True, exist_ok=True)
        self.conexion = sqlite3.connect(ruta)
        self.conexion.row_factory = sqlite3.Row
        self.conexion.execute("PRAGMA foreign_keys = ON")
        self.conexion.executescript("""
            CREATE TABLE IF NOT EXISTS usuarios (
                codigo INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                cuenta TEXT NOT NULL UNIQUE COLLATE NOCASE,
                clave_protegida TEXT NOT NULL,
                rol TEXT NOT NULL CHECK (rol IN ('administrador', 'planificador')),
                activo INTEGER NOT NULL DEFAULT 1 CHECK (activo IN (0, 1))
            );
            CREATE TABLE IF NOT EXISTS materias (
                codigo TEXT PRIMARY KEY COLLATE NOCASE,
                nombre TEXT NOT NULL,
                nivel INTEGER NOT NULL CHECK (nivel > 0),
                horas_teoria INTEGER NOT NULL CHECK (horas_teoria >= 0),
                horas_practica INTEGER NOT NULL CHECK (horas_practica >= 0),
                CHECK (horas_teoria + horas_practica > 0)
            );
        """)

    def cerrar(self):
        self.conexion.close()

    def hay_usuarios(self):
        return self.conexion.execute("SELECT 1 FROM usuarios LIMIT 1").fetchone() is not None

    def crear_usuario(self, nombre, cuenta, clave, rol, inicial=False):
        try:
            # Reservar la escritura antes de comprobar la primera cuenta.
            self.conexion.execute("BEGIN IMMEDIATE")
            if inicial and self.hay_usuarios():
                raise ValueError("La configuración inicial ya fue completada.")
            self.conexion.execute(
                "INSERT INTO usuarios (nombre, cuenta, clave_protegida, rol) VALUES (?, ?, ?, ?)",
                (nombre, cuenta, clave, rol),
            )
            self.conexion.commit()
        except (sqlite3.Error, ValueError):
            self.conexion.rollback()
            raise

    def _guardar_cambio(self, consulta, parametros):
        # commit confirma; rollback cancela el cambio si SQLite informa un error.
        try:
            resultado = self.conexion.execute(consulta, parametros)
            self.conexion.commit()
            return resultado.rowcount
        except sqlite3.Error:
            self.conexion.rollback()
            raise

    def buscar_cuenta(self, cuenta):
        return self.conexion.execute("SELECT * FROM usuarios WHERE cuenta = ?", (cuenta,)).fetchone()

    def obtener_usuario(self, codigo):
        fila = self.conexion.execute("SELECT * FROM usuarios WHERE codigo = ?", (codigo,)).fetchone()
        if fila is None:
            return None
        if fila["rol"] == "administrador":
            return Administrador(fila["codigo"], fila["nombre"], fila["cuenta"], fila["activo"])
        return PlanificadorAcademico(fila["codigo"], fila["nombre"], fila["cuenta"], fila["activo"])

    def listar_planificadores(self):
        return self.conexion.execute(
            "SELECT codigo, nombre, cuenta, activo FROM usuarios WHERE rol = 'planificador' ORDER BY nombre"
        ).fetchall()

    def desactivar_planificador(self, codigo):
        cambios = self._guardar_cambio(
            "UPDATE usuarios SET activo = 0 WHERE codigo = ? AND rol = 'planificador'", (codigo,)
        )
        if cambios == 0:
            raise ValueError("Selecciona una cuenta de planificador.")

    def listar_materias(self):
        filas = self.conexion.execute("SELECT * FROM materias ORDER BY codigo").fetchall()
        materias = []
        for fila in filas:
            materia = Materia(fila["codigo"], fila["nombre"], fila["nivel"],
                              fila["horas_teoria"], fila["horas_practica"])
            materias.append(materia)
        return materias

    def guardar_materia(self, materia, codigo_anterior=None):
        materia.validar()
        valores = (materia.codigo, materia.nombre, materia.nivel, materia.horas_teoria, materia.horas_practica)
        if codigo_anterior is None:
            self._guardar_cambio("INSERT INTO materias VALUES (?, ?, ?, ?, ?)", valores)
        else:
            cambios = self._guardar_cambio(
                "UPDATE materias SET codigo=?, nombre=?, nivel=?, horas_teoria=?, horas_practica=? WHERE codigo=?",
                valores + (codigo_anterior,),
            )
            if cambios == 0:
                raise ValueError("La materia seleccionada ya no existe. Actualiza la lista.")

    def eliminar_materia(self, codigo):
        cambios = self._guardar_cambio("DELETE FROM materias WHERE codigo = ?", (codigo,))
        if cambios == 0:
            raise ValueError("La materia seleccionada ya no existe.")
