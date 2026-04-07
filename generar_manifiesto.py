import hashlib
import sys
from pathlib import Path

MANIFIESTO = "SHA256SUMS.txt"
CARPETA    = Path("datos")

def calcular_sha256(ruta) -> str:
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(65536), b""):
            h.update(bloque)
    return h.hexdigest()

def generar_manifiesto(rutas):
    print("  MEDISOFT S.A. — Generador de Manifiesto SHA-256")

    with open(MANIFIESTO, "a") as f:
        for ruta in rutas:
            path = Path(ruta)
            if not path.exists():
                print(f"  [ERROR] No encontrado: {ruta}")
                continue

            hash_sha256 = calcular_sha256(path)
            linea = f"{hash_sha256}  {path.name}\n"
            f.write(linea)
            print(f"  [OK] {path.name}")
            print(f"       SHA-256: {hash_sha256}")

    print(f"\n  Manifiesto actualizado -> {MANIFIESTO}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Archivos pasados como argumentos
        archivos = sys.argv[1:]
    else:
        # Auto-detectar archivos dentro de la carpeta "datos"
        if not CARPETA.exists():
            print(f"  [ERROR] No se encontró la carpeta '{CARPETA}'.")
            sys.exit(1)

        archivos = [f for f in CARPETA.iterdir() if f.is_file()]

        if not archivos:
            print(f"  No se encontraron archivos en '{CARPETA}'.")
            sys.exit(1)

        print(f"  Archivos detectados en '{CARPETA}': {len(archivos)}\n")

    generar_manifiesto(archivos)