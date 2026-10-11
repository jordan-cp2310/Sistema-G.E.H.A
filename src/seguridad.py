"""La protección de claves se mantiene separada de la lógica académica."""

import hashlib
import hmac
import secrets


ITERACIONES = 600_000


def proteger_clave(clave):
    if len(clave) < 8 or not clave.strip():
        raise ValueError("La contraseña debe tener al menos 8 caracteres.")
    sal = secrets.token_hex(16)
    # Estas operaciones pertenecen al módulo de apoyo de seguridad.
    clave_en_bytes = clave.encode("utf-8")
    sal_en_bytes = bytes.fromhex(sal)
    resumen = hashlib.pbkdf2_hmac("sha256", clave_en_bytes, sal_en_bytes, ITERACIONES)
    return f"{ITERACIONES}${sal}${resumen.hex()}"


def comprobar_clave(clave, protegida):
    partes = protegida.split("$")
    iteraciones = int(partes[0])
    sal = bytes.fromhex(partes[1])
    resumen = partes[2]
    clave_en_bytes = clave.encode("utf-8")
    candidato = hashlib.pbkdf2_hmac("sha256", clave_en_bytes, sal, iteraciones)
    return hmac.compare_digest(candidato.hex(), resumen)
