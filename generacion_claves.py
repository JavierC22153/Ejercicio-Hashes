import hashlib
import urllib.request

CONTRASENAS = ["admin", "123456", "hospital", "medisoft2024"]

def calcular_hashes(contrasena: str) -> tuple[str, str]:
    encoded = contrasena.encode("utf-8")
    sha256 = hashlib.sha256(encoded).hexdigest()
    sha1   = hashlib.sha1(encoded).hexdigest().upper()
    return sha256, sha1

def consultar_hibp(sha1_hex: str) -> int:
    prefijo  = sha1_hex[:5]
    sufijo   = sha1_hex[5:]
    url      = f"https://api.pwnedpasswords.com/range/{prefijo}"

    req = urllib.request.Request(url, headers={"User-Agent": "MediSoft-Lab-Script"})
    with urllib.request.urlopen(req) as response:
        contenido = response.read().decode("utf-8")

    for linea in contenido.splitlines():
        hash_sufijo, cantidad = linea.split(":")
        if hash_sufijo.upper() == sufijo.upper():
            return int(cantidad)
    return 0

print("  VERIFICACIÓN DE CONTRASEÑAS EN HAVE I BEEN PWNED (HIBP)")

resultados = []

for contrasena in CONTRASENAS:
    sha256, sha1 = calcular_hashes(contrasena)
    print(f"\n  Contraseña  : {contrasena}")
    print(f"  SHA-256     : {sha256}")
    print(f"  Prefijo enviado a HIBP → https://api.pwnedpasswords.com/range/{sha1[:5]}")

    try:
        veces = consultar_hibp(sha1)
        print(f"  Filtraciones: {veces:,} veces encontrada")
        resultados.append((contrasena, sha256, veces))
    except Exception as e:
        print(f"  Error al consultar HIBP: {e}")
        resultados.append((contrasena, sha256, -1))

# Tabla resumen
print("\n  RESUMEN")
print(f"  {'Contraseña':<18} {'Filtraciones':>14}")
print("  " + "-" * 34)
for contrasena, _, veces in resultados:
    veces_str = f"{veces:,}" if veces >= 0 else "N/A"
    print(f"  {contrasena:<18} {veces_str:>14}")