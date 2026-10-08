# G.E.H.A. — Estructura inicial del equipo

Proyecto académico de Gestión de Horarios Académicos con Python, Tkinter y SQLite.
Esta entrega contiene únicamente la estructura de carpetas para comenzar el trabajo
del equipo. Todavía no incluye una aplicación ejecutable.

## Estructura

```text
Sistema-G.E.H.A/
├── README.md
├── .gitignore
├── diagramas/
├── docs/
├── src/
│   ├── datos/
│   ├── interfaz/
│   └── modelos/
└── tests/
```

- `modelos/`: clases del dominio y sus reglas.
- `datos/`: consultas y almacenamiento en SQLite.
- `interfaz/`: ventanas y formularios con Tkinter/ttk.
- `docs/`: alcance, decisiones y explicación de los aportes.
- `diagramas/`: modelos UML acordados por el equipo.
- `tests/`: comprobaciones de las funciones implementadas.

Los archivos `.gitkeep` permiten guardar carpetas que aún no tienen contenido.
No son código de Python. `data/` y `__pycache__/` son carpetas locales generadas
durante el uso del programa y se excluyen de Git.

## Trabajo de cada integrante

1. Clonar este repositorio e ingresar con su propia cuenta de GitHub.
2. Configurar su nombre y correo de autor en Git.
3. Crear una rama para su aporte, por ejemplo `aporte-materias`.
4. Implementar, adaptar y comprobar la parte acordada.
5. Registrar cambios con mensajes que describan el trabajo realizado.
6. Subir su rama y abrir un pull request hacia `main` para revisión del equipo.

El prototipo preparado previamente con ayuda de Codex se conserva como referencia
en [G.E.H.A., rama del avance](https://github.com/jordan-cp2310/G.E.H.A/tree/avance-01-base-y-materias).
Cuando se reutilice una parte, se documentará su incorporación, adaptación y
comprobación. El acceso a ese repositorio de referencia requiere autorización.

El primer objetivo funcional es acceso con dos roles y un catálogo de materias
persistente. La distribución de responsabilidades se acordará entre los cinco
integrantes antes de incorporar los módulos.
