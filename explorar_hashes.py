import hashlib

def calcular_hashes(texto: str) -> dict:
    encoded = texto.encode("utf-8")
    return {
        "MD5":      hashlib.md5(encoded),
        "SHA-1":    hashlib.sha1(encoded),
        "SHA-256":  hashlib.sha256(encoded),
        "SHA3-256": hashlib.sha3_256(encoded),
    }

def imprimir_tabla(texto: str, hashes: dict):
    print(f"\n  Input: \"{texto}\"")
    print(f"  {'Algoritmo':<10} {'Bits':>6} {'Hex len':>8}  Hash")
    print("  " + "-" * 90)
    for nombre, h in hashes.items():
        digest = h.hexdigest()
        bits = h.digest_size * 8
        print(f"  {nombre:<10} {bits:>6} {len(digest):>8}  {digest}")

def contar_bits_diferentes(hash1_hex: str, hash2_hex: str) -> int:
    xor = int(hash1_hex, 16) ^ int(hash2_hex, 16)
    return bin(xor).count("1")

#Inputs
input_original  = "MediSoft-v2.1.0"
input_lowercase = "medisoft-v2.1.0"

hashes_orig = calcular_hashes(input_original)
hashes_low  = calcular_hashes(input_lowercase)

# Tabla comparativa
imprimir_tabla(input_original, hashes_orig)
imprimir_tabla(input_lowercase, hashes_low)

# ── Análisis de efecto avalancha con XOR (SHA-256)─
sha256_orig = hashes_orig["SHA-256"].hexdigest()
sha256_low  = hashes_low["SHA-256"].hexdigest()

bits_diferentes = contar_bits_diferentes(sha256_orig, sha256_low)
total_bits      = 256

print(" \n ANÁLISIS DE EFECTO AVALANCHA (SHA-256 con XOR)")
print(f"\n  Original  : {sha256_orig}")
print(f"  Lowercase : {sha256_low}")
print(f"\n  Bits diferentes : {bits_diferentes} / {total_bits}  ({bits_diferentes/total_bits*100:.1f}%)")

