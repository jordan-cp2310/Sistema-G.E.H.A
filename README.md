# G.E.H.A. — Estructura inicial del equipo

Proyecto académico de Gestión de Horarios Académicos con Python, Tkinter y SQLite.
rencia requiere autorización.

# G.E.H.A. — Gestión de Horarios Académicos

Proyecto académico de Programación Orientada a Objetos, tercer semestre de
Ingeniería en Software de la ULEAM. El repositorio conserva el nombre del sistema es **G.E.H.A.**

## Avance 01: acceso y catálogo de materias

Este primer avance establece la estructura del programa y un recorrido funcional
con datos guardados. Corresponde al alcance inicial solicitado no es una medición exacta del proyecto ni una consigna atribuida
al profesor. **Todavía no crea horarios.**

### Funciones terminadas

- Configuración del administrador en la primera apertura, sin cuentas predefinidas.
- Inicio y cierre de sesión; rechazo de claves incorrectas y cuentas inactivas.
- Administrador: crear y desactivar cuentas de planificadores.
- Planificador: registrar, consultar, modificar y eliminar materias con confirmación.
- Validación de campos, códigos únicos, niveles y horas.
- Persistencia SQLite y contraseñas protegidas con sal y PBKDF2-HMAC-SHA256.
- Verificación de permisos en cada acción del sistema, además de la interfaz.

## Cómo ejecutar

Requisitos: **Python 3.10 o superior con Tkinter**. Se comprobó con Python 3.14 y
Tkinter 8.6 en Windows. No hay paquetes externos que instalar.

Abre la carpeta del repositorio en Visual Studio Code y ejecuta en su terminal:

```powershell
python main.py
```

Si Windows reconoce Python como `py`, utiliza `py main.py`.
La base se crea en `data/geha.db`, siempre junto al proyecto aunque se inicie
desde otra carpeta. No se reemplaza durante el arranque y no se sube a GitHub.
El código descargado en otra PC comienza con su propia base vacía.

### Primera apertura

1. Escribe el nombre y la cuenta del administrador y una contraseña de al menos
   ocho caracteres. Repite la contraseña y pulsa **Crear administrador**.
2. Inicia sesión con esa cuenta.
3. Crea una cuenta de planificador con datos ficticios para la demostración.
4. Cierra sesión y entra con el planificador para acceder a las materias.

La configuración inicial deja de estar disponible cuando existe una cuenta.
El administrador gestiona accesos; la edición académica corresponde al planificador.
No hay registro público, recuperación de contraseña ni cuentas de estudiantes
o profesores en esta etapa. Guarda tus claves de demostración en un lugar seguro.

## Estructura y responsabilidades

```text
AcademiSync/
├── main.py                     # Punto de entrada
├── src/
│   ├── modelos/
│   │   ├── materia.py          # Datos y reglas de una materia
│   │   └── usuario.py          # Usuario y sus dos tipos concretos
│   ├── datos/
│   │   └── base_datos.py       # Consultas y transacciones SQLite
│   ├── interfaz/
│   │   └── aplicacion.py       # Ventanas, formularios y tabla
│   ├── sistema.py             # Sesión, permisos y casos de uso
│   └── seguridad.py           # Protección y comprobación de claves
├── docs/                      # Alcance, decisiones y guía de exposición
├── diagrams/                  # Diagramas originales conservados
├── diagramas/                 # Carpeta inicial del equipo conservada
├── tests/                     # Pruebas con bases temporales
└── data/                      # Datos locales; excluidos de Git
```

Los archivos `__init__.py` identifican los paquetes de Python. La explicación
de las clases y de cómo crecerá esta estructura está en
[la guía de POO](docs/guia_poo.md).

## Demostración para el profesor

1. Abre la aplicación y realiza el acceso inicial descrito arriba.
2. Como planificador registra `POO-03`, `Programación Orientada a Objetos`,
   nivel `3`, teoría `2`, práctica `2`. La tabla mostrará un total de `4` horas.
3. Pulsa **Nueva / limpiar** e intenta repetir `POO-03`: debe rechazarlo.
4. Selecciona la fila, cambia las horas de teoría a `3` y guarda: total `5`.
5. Cierra la ventana y ejecuta otra vez `python main.py`. Inicia sesión y
   comprueba que la materia sigue guardada.
6. Selecciona la materia, pulsa **Eliminar** y confirma.
7. Entra como administrador, desactiva el planificador y comprueba que esa
   cuenta ya no puede iniciar sesión.

En una nueva exposición puedes crear otro planificador: la reactivación no se
incluye en este avance. Los códigos de materia se guardan en mayúsculas; al editar
puedes cambiarlos siempre que no coincidan con otro registro.

## Comprobaciones

```powershell
python -m unittest discover -s tests -v
```

Ocho pruebas automatizadas cubren el dominio, autenticación, permisos, registro,
edición, duplicados, persistencia, eliminación y el recorrido de widgets Tkinter.
No cambian la base real. La prueba de interfaz necesita un entorno que permita
crear ventanas y simula la respuesta de los diálogos; no sustituye una inspección
visual humana. Para probar solo la lógica sin escritorio:

```powershell
python -m unittest discover -s tests -p test_avance.py -v
```

## Próximas etapas

1. Incorporar `Carrera` y su colección de materias, después `Paralelo` y `Profesor`.
2. Registrar aulas, laboratorios, periodos y disponibilidad.
3. Implementar `BloqueHorario`, `Clase` y `Horario`, con revisión de cruces.
4. Añadir sugerencias, tutorías, revisiones, registro de aprobación institucional,
   exportación y respaldos.

La planificación será asistida: el planificador decide y el sistema comprueba.
No se implementan clases vacías ni botones que aparenten esas funciones futuras.
