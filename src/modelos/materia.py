class Materia:
    def __init__(self, codigo, nombre, nivel, horas_teoria, horas_practica):
        self.codigo = codigo.strip().upper()
        self.nombre = nombre
        self.nivel = nivel
        self.horas_teoria = horas_teoria
        self.horas_practica = horas_practica
        self.validar()

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        # La propiedad protege el nombre, incluso al asignarlo directamente.
        if not valor.strip():
            raise ValueError("El nombre es obligatorio.")
        self.__nombre = valor.strip()

    @property
    def horas_semanales(self):
        return self.horas_teoria + self.horas_practica

    def validar(self):
        if not self.codigo or not self.nombre:
            raise ValueError("El código y el nombre son obligatorios.")
        if type(self.nivel) is not int:
            raise ValueError("El nivel debe ser un número entero.")
        if self.nivel < 1:
            raise ValueError("El nivel debe ser mayor que cero.")
        self.revisar_horas(self.horas_teoria, self.horas_practica)

    @staticmethod
    def revisar_horas(teoria, practica):
        # No necesita self: comprueba dos valores antes de guardarlos.
        if type(teoria) is not int or type(practica) is not int:
            raise ValueError("Las horas deben ser números enteros.")
        if teoria < 0 or practica < 0:
            raise ValueError("Las horas no pueden ser negativas.")
        if teoria + practica == 0:
            raise ValueError("La materia debe tener al menos una hora semanal.")

    def cambiar_nombre(self, nombre):
        self.nombre = nombre

    def cambiar_horas(self, teoria, practica):
        # Validar antes de cambiar evita dejar el objeto a medio modificar.
        self.revisar_horas(teoria, practica)
        self.horas_teoria = teoria
        self.horas_practica = practica
