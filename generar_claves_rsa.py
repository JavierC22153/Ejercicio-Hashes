from Crypto.PublicKey import RSA
from Crypto.Signature import pss
from Crypto.Hash import SHA256

# Archivos de salida
CLAVE_PRIVADA = "medisoft_priv.pem"
CLAVE_PUBLICA = "medisoft_pub.pem"
MANIFIESTO    = "SHA256SUMS.txt"
FIRMA         = "SHA256SUMS.sig"

# Generación del par de claves RSA 2048 bits
print("  MEDISOFT S.A. — Generación de Claves RSA y Firma Digital")
clave = RSA.generate(2048)

# Exportar clave privada
clave_privada_pem = clave.export_key(format="PEM")
with open(CLAVE_PRIVADA, "wb") as f:
    f.write(clave_privada_pem)

print(f"   Clave PRIVADA guardada → {CLAVE_PRIVADA}")

# Exportar clave pública
clave_publica_pem = clave.publickey().export_key(format="PEM")
with open(CLAVE_PUBLICA, "wb") as f:
    f.write(clave_publica_pem)

print(f"  Clave PÚBLICA  guardada → {CLAVE_PUBLICA}")

# 4. Firmar el manifiesto SHA256SUMS.txt
print(f"\n  Firmando {MANIFIESTO} con la clave privada (RSA-PSS + SHA-256)...")

with open(MANIFIESTO, "rb") as f:
    contenido = f.read()

# Calcular hash SHA-256 del manifiesto
hash_manifiesto = SHA256.new(contenido)
print(f"        SHA-256 del manifiesto: {hash_manifiesto.hexdigest()}")

# Firmar con RSA-PSS
firmante = pss.new(clave)
firma    = firmante.sign(hash_manifiesto)

with open(FIRMA, "wb") as f:
    f.write(firma)

print(f"        Firma guardada → {FIRMA} ({len(firma)} bytes)")