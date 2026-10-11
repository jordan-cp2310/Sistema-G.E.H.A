from pathlib import Path

from src.datos.base_datos import BaseDatos
from src.sistema import Sistema
from src.interfaz.aplicacion import Aplicacion


if __name__ == "__main__":
    ruta = Path(__file__).resolve().parent / "data" / "geha.db"
    base = BaseDatos(ruta)
    try:
        sistema = Sistema(base)
        ventana = Aplicacion(sistema)
        ventana.mainloop()
    finally:
        base.cerrar()
