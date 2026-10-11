from abc import ABC, abstractmethod


class Usuario(ABC):
    def __init__(self, codigo, nombre, cuenta, activo=True):
        self.codigo = codigo
        self.nombre = nombre
        self.cuenta = cuenta
        self.activo = bool(activo)

    @abstractmethod
    def permite(self, modulo):
        """Cada tipo de usuario decide qué módulo puede utilizar."""


class Administrador(Usuario):
    # Atributo de clase: es el mismo para todos los administradores.
    rol = "administrador"

    def permite(self, modulo):
        return self.activo and modulo == "usuarios"


class PlanificadorAcademico(Usuario):
    rol = "planificador"

    def permite(self, modulo):
        return self.activo and modulo == "materias"
