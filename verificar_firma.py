from Crypto.PublicKey import RSA
from Crypto.Signature import pss
from Crypto.Hash import SHA256

CLAVE_PUBLICA = "medisoft_pub.pem"
MANIFIESTO    = "SHA256SUMS.txt"
FIRMA         = "SHA256SUMS.sig"

print("  HOSPITAL — Verificación de Firma Digital")

# Cargar archivos
print(f"\n  Leyendo clave pública  → {CLAVE_PUBLICA}")
with open(CLAVE_PUBLICA, "rb") as f:
    clave_publica = RSA.import_key(f.read())

print(f"  Leyendo manifiesto     → {MANIFIESTO}")
with open(MANIFIESTO, "rb") as f:
    contenido = f.read()

print(f"  Leyendo firma digital  → {FIRMA}")
with open(FIRMA, "rb") as f:
    firma = f.read()

# Validar firma
print("\n  Validando firma digital (RSA-PSS + SHA-256)...")

hash_manifiesto = SHA256.new(contenido)
print(f"  SHA-256 del manifiesto: {hash_manifiesto.hexdigest()}")

try:
    verificador = pss.new(clave_publica)
    verificador.verify(hash_manifiesto, firma)
    print("\n   FIRMA VÁLIDA")
    print("     El manifiesto es auténtico y fue creado por MediSoft.")
    print("     Ningún atacante ha modificado SHA256SUMS.txt.")
except (ValueError, TypeError):
    print("\n   FIRMA INVÁLIDA")
    print("     El manifiesto fue alterado o la firma no corresponde.")
    print("     NO confíe en este paquete.")
