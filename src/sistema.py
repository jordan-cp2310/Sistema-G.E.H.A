import sqlite3

from src.seguridad import comprobar_clave, proteger_clave


class Sistema:
    """Conecta los casos de uso con los datos, sin depender de Tkinter."""

    def __init__(self, base):
        self.base = base
        self.usuario = None

    def necesita_configuracion(self):
        return not self.base.hay_usuarios()

    def configurar_administrador(self, nombre, cuenta, clave):
        if not self.necesita_configuracion():
            raise ValueError("La configuración inicial ya fue completada.")
        self._crear_usuario(nombre, cuenta, clave, "administrador", inicial=True)

    def _crear_usuario(self, nombre, cuenta, clave, rol, inicial=False):
        if not nombre.strip() or not cuenta.strip():
            raise ValueError("El nombre y la cuenta son obligatorios.")
        protegida = proteger_clave(clave)
        try:
            self.base.crear_usuario(nombre.strip(), cuenta.strip().lower(), protegida, rol, inicial)
        except sqlite3.IntegrityError:
            raise ValueError("Ya existe una cuenta con ese nombre de acceso.")

    def iniciar_sesion(self, cuenta, clave):
        self.cerrar_sesion()
        fila = self.base.buscar_cuenta(cuenta.strip())
        if fila is None:
            raise ValueError("Cuenta o contraseña incorrecta, o cuenta desactivada.")
        if not fila["activo"]:
            raise ValueError("Cuenta o contraseña incorrecta, o cuenta desactivada.")
        if not comprobar_clave(clave, fila["clave_protegida"]):
            raise ValueError("Cuenta o contraseña incorrecta, o cuenta desactivada.")
        self.usuario = self.base.obtener_usuario(fila["codigo"])
        return self.usuario

    def cerrar_sesion(self):
        self.usuario = None

    def _exigir_permiso(self, modulo):
        # Se consulta otra vez por si un administrador desactivó la cuenta.
        if self.usuario is not None:
            self.usuario = self.base.obtener_usuario(self.usuario.codigo)
        if self.usuario is None or not self.usuario.permite(modulo):
            raise PermissionError("Tu cuenta no tiene permiso para realizar esta acción.")

    def crear_planificador(self, nombre, cuenta, clave):
        self._exigir_permiso("usuarios")
        self._crear_usuario(nombre, cuenta, clave, "planificador")

    def listar_planificadores(self):
        self._exigir_permiso("usuarios")
        return self.base.listar_planificadores()

    def desactivar_planificador(self, codigo):
        self._exigir_permiso("usuarios")
        self.base.desactivar_planificador(codigo)

    def listar_materias(self):
        self._exigir_permiso("materias")
        return self.base.listar_materias()

    def guardar_materia(self, materia, codigo_anterior=None):
        self._exigir_permiso("materias")
        try:
            self.base.guardar_materia(materia, codigo_anterior)
        except sqlite3.IntegrityError:
            raise ValueError("Ya existe una materia con ese código.")

    def eliminar_materia(self, codigo):
        self._exigir_permiso("materias")
        try:
            self.base.eliminar_materia(codigo)
        except sqlite3.IntegrityError:
            raise ValueError("La materia tiene referencias y no puede eliminarse.")
