import hashlib
from pathlib import Path
 
MANIFIESTO = "SHA256SUMS.txt"
CARPETA    = Path("datos")
 
def calcular_sha256(ruta: str) -> str:
    """Calcula el SHA-256 de un archivo leyéndolo en bloques."""
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(65536), b""):
            h.update(bloque)
    return h.hexdigest()
 
def verificar_paquete(manifiesto: str = MANIFIESTO):
    print("  HOSPITAL — Verificador de Integridad de Paquete")
 
    if not Path(manifiesto).exists():
        print(f"  [ERROR] No se encontró el manifiesto: {manifiesto}")
        return
 
    correctos   = []
    incorrectos = []
 
    with open(manifiesto, "r") as f:
        lineas = [l.strip() for l in f if l.strip()]
 
    print(f"\n  Archivos a verificar: {len(lineas)}\n")
 
    for linea in lineas:
        partes = linea.split(None, 1) 
        if len(partes) != 2:
            print(f"  [AVISO] Línea con formato inesperado: {linea}")
            continue
 
        hash_esperado, nombre = partes
        hash_esperado = hash_esperado.strip()
        nombre        = nombre.strip()
 
        ruta = CARPETA / nombre
 
        if not ruta.exists():
            print(f"  [ERROR] Archivo no encontrado: {ruta}")
            incorrectos.append(nombre)
            continue
 
        hash_real = calcular_sha256(ruta)
 
        if hash_real == hash_esperado:
            print(f"   OK       {nombre}")
            correctos.append(nombre)
        else:
            print(f"   ALTERADO {nombre}")
            print(f"    Esperado : {hash_esperado}")
            print(f"    Obtenido : {hash_real}")
            incorrectos.append(nombre)
 
    # Reporte final
    print(" \n REPORTE FINAL")
    print(f"  Correctos  : {len(correctos)}")
    print(f"  Alterados  : {len(incorrectos)}")
 
    if incorrectos:
        print("\n    ADVERTENCIA: Los siguientes archivos fueron modificados")
        print("  o no se encontraron. NO instale este paquete.\n")
        for nombre in incorrectos:
            print(f"    - {nombre}")
    else:
        print("\n   Todos los archivos son íntegros. Paquete seguro.")
 
if __name__ == "__main__":
    verificar_paquete()
 