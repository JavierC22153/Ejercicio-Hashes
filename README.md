# Ejercicio: Hashes y Firmas Digitales

## Descripción del Proyecto

Este laboratorio simula un escenario real de seguridad en la empresa ficticia **MediSoft S.A.**, distribuidora de software de diagnóstico médico a hospitales en Guatemala, Honduras y El Salvador.

Tras un ataque donde un mirror no oficial inyectó código malicioso en un paquete de actualización, se implementan **dos capas de protección criptográfica**:

- **Integridad de distribución**: verificar que los paquetes descargados son exactamente los que MediSoft publicó, usando SHA-256.
- **Autenticidad del manifiesto**: firmar digitalmente el manifiesto de hashes con RSA para garantizar que no fue alterado por un atacante.

El proyecto cubre: comparación de algoritmos hash, verificación de contraseñas filtradas (HIBP), generación de manifiestos SHA-256, y firma/verificación digital con RSA-PSS.

---

## Estructura del Proyecto

```
Ejercicio-Hashes/
├── datos/                    # Archivos del paquete a verificar (mínimo 5)
│   ├── diagnostico.db
│   ├── lab_config.cfg
│   ├── medisoft_core.bin
│   ├── ssl_certs.pem
│   └── usb_driver.dat
├── explorar_hashes.py        # Problema 1: Comparación de algoritmos
├── generacion_claves.py      # Problema 2: Verificación en HIBP
├── generar_manifiesto.py     # Problema 3: Generador de SHA256SUMS.txt
├── verificar_paquete.py      # Problema 3: Verificador de integridad
├── generar_claves_rsa.py     # Problema 4: Generación de claves y firma
├── verificar_firma.py        # Problema 5: Verificación de firma digital
├── .gitignore
└── README.md
```

---

## Instalación y Uso

### 1. Clonar el repositorio

```bash
git clone https://github.com/JavierC22153/Ejercicio-Hashes.git
cd Ejercicio-Hashes
```

### 2. Instalar dependencias

El proyecto usa la biblioteca estándar de Python y `pycryptodome`:

```bash
pip install pycryptodome
```

### 3. Ejecutar los scripts en orden

```bash
# Problema 1: Comparar algoritmos hash
python explorar_hashes.py

# Problema 2: Verificar contraseñas en HIBP
python generacion_claves.py

# Problema 3: Generar manifiesto de hashes
python generar_manifiesto.py

# Problema 3: Verificar integridad de archivos
python verificar_paquete.py

# Problema 4: Generar claves RSA y firmar el manifiesto
python generar_claves_rsa.py

# Problema 5: Verificar la firma digital
python verificar_firma.py
```

---

## Ejemplos de Ejecución

### `explorar_hashes.py`

```
Input: "MediSoft-v2.1.0"
  Algoritmo    Bits  Hex len  Hash
  ------------------------------------------------------------------------------------------
  MD5           128       32  cac2fe40370e3a68f0a4927c20c75c89
  SHA-1         160       40  3ab92abc44e23465b154e887f90c3a5e0d642c65
  SHA-256       256       64  64942401fe64ac1182bd88326ba7ca57a23ea5d0475653dea996ac15e8e74996
  SHA3-256      256       64  3b0af4c0a9078e2ddc1606313db9206dcb3a4dbf423d78c0cf16929d303e30d2

Input: "medisoft-v2.1.0"
  Algoritmo    Bits  Hex len  Hash
  ------------------------------------------------------------------------------------------
  MD5           128       32  fa386a0d796e388b24cb3302c185a445
  SHA-1         160       40  4fe9fa8c97db362ecce61ee6302a92f0505217cd
  SHA-256       256       64  ec8d163da33b9832c33fbb2d7cba98f5a7087aa6cbdecc04eb32810b1f1f895e
  SHA3-256      256       64  569daf2d0645c0ab6c0a7960cb552f28ac1a222284fa5605ab11cfe0a2dce82c

 ANÁLISIS DE EFECTO AVALANCHA (SHA-256 con XOR)
  Original  : 64942401fe64ac1182bd88326ba7ca57a23ea5d0475653dea996ac15e8e74996
  Lowercase : ec8d163da33b9832c33fbb2d7cba98f5a7087aa6cbdecc04eb32810b1f1f895e
  Bits diferentes : 120 / 256  (46.9%)
```

### `generacion_claves.py`

```
  VERIFICACIÓN DE CONTRASEÑAS EN HAVE I BEEN PWNED (HIBP)

  Contraseña  : admin
  SHA-256     : 8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918
  Prefijo enviado a HIBP → https://api.pwnedpasswords.com/range/D033E
  Filtraciones: 42,085,691 veces encontrada

  Contraseña  : 123456
  SHA-256     : 8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92
  Prefijo enviado a HIBP → https://api.pwnedpasswords.com/range/7C4A8
  Filtraciones: 209,972,844 veces encontrada

  Contraseña  : hospital
  SHA-256     : 8afe3c83decffdf6dc48597a3f1a52be7c6e2b97b4bdf3b15e20a87a1f657f01
  Prefijo enviado a HIBP → https://api.pwnedpasswords.com/range/2B2D0
  Filtraciones: 118,791 veces encontrada

  Contraseña  : medisoft2024
  SHA-256     : 78c12e8e24dfd7836c748c33dff2e9150c028d69488f203485e13f4a6daa777c
  Prefijo enviado a HIBP → https://api.pwnedpasswords.com/range/F80CF
  Filtraciones: 0 veces encontrada

  RESUMEN
  Contraseña           Filtraciones
  ----------------------------------
  admin              42,085,691
  123456            209,972,844
  hospital              118,791
  medisoft2024                0
```

### `generar_manifiesto.py`

```
  Archivos detectados en 'datos': 5

  MEDISOFT S.A. — Generador de Manifiesto SHA-256
  [OK] diagnostico.db
       SHA-256: 877596e67babaefc4591f6ff16b5e604de1e517cd61fae60f55235332b01dfdd
  [OK] lab_config.cfg
       SHA-256: 4d564471585a2d0336bd09e23dc11cfe69c6c813a4901c2658c42763b015e45b
  [OK] medisoft_core.bin
       SHA-256: d6d65f12d5e7bb7774669eb7fa9b600139afb314d5582e3d899d4886b7edd46b
  [OK] ssl_certs.pem
       SHA-256: dd5c906e70b64a51fba75bf738007a9f548a9c5f6504e102a47a3f42bb0a31fe
  [OK] usb_driver.dat
       SHA-256: 674010cd0d17e6b57266894de1c4650b02f87fab0b9632b0b05bcf20de8f1e07

  Manifiesto actualizado -> SHA256SUMS.txt
```

### `verificar_paquete.py`

```
  HOSPITAL — Verificador de Integridad de Paquete

  Archivos a verificar: 5

   OK       diagnostico.db
   OK       lab_config.cfg
   OK       medisoft_core.bin
   OK       ssl_certs.pem
   OK       usb_driver.dat

  REPORTE FINAL
  Correctos  : 5
  Alterados  : 0

   Todos los archivos son íntegros. Paquete seguro.
```

### `generar_claves_rsa.py`

```
  MEDISOFT S.A. — Generación de Claves RSA y Firma Digital
   Clave PRIVADA guardada → medisoft_priv.pem
  Clave PÚBLICA  guardada → medisoft_pub.pem

  Firmando SHA256SUMS.txt con la clave privada (RSA-PSS + SHA-256)...
        SHA-256 del manifiesto: 14260e240cb3cf7c2009906fdd6b0043d79fbffbae7d3e58d70b2d8d9b343d6a
        Firma guardada → SHA256SUMS.sig (256 bytes)
```

### `verificar_firma.py`

```
  HOSPITAL — Verificación de Firma Digital

  Leyendo clave pública  → medisoft_pub.pem
  Leyendo manifiesto     → SHA256SUMS.txt
  Leyendo firma digital  → SHA256SUMS.sig

  Validando firma digital (RSA-PSS + SHA-256)...
  SHA-256 del manifiesto: 14260e240cb3cf7c2009906fdd6b0043d79fbffbae7d3e58d70b2d8d9b343d6a

   FIRMA VÁLIDA
     El manifiesto es auténtico y fue creado por MediSoft.
     Ningún atacante ha modificado SHA256SUMS.txt.
```

---

## Respuestas a las Preguntas de Análisis

### ¿Cuántos bits cambiaron entre los dos hashes SHA-256? ¿Qué propiedad demuestra?

Al cambiar únicamente la capitalización de "MediSoft-v2.1.0" a "medisoft-v2.1.0", el análisis XOR reveló que cambiaron **120 de 256 bits (46.9%)**, a pesar de que el input solo difiere en 8 caracteres. Esto demuestra el **efecto avalancha**: una función hash criptográfica produce una salida completamente diferente ante cualquier cambio mínimo en la entrada, sin importar qué tan pequeño sea.

### ¿Por qué MD5 es considerado inseguro para integridad de archivos?

MD5 produce un hash de únicamente **128 bits**, lo que significa que solo existen 2¹²⁸ posibles valores de salida. Aunque es un número grande, el espacio reducido lo hace vulnerable a **colisiones**: dos archivos distintos pueden producir el mismo hash MD5. Esto ha sido demostrado en la práctica; existen ataques conocidos que generan colisiones MD5 de forma deliberada. 

### ¿Por qué la firma sigue siendo válida al modificar un archivo de `datos/` pero `verificar_paquete.py` sí detecta el cambio?

Porque cada herramienta protege una capa diferente. `verificar_firma.py` únicamente verifica que el archivo `SHA256SUMS.txt` no haya sido alterado desde que MediSoft lo firmó. Si el manifiesto no fue tocado, la firma es válida. Sin embargo, `verificar_paquete.py` compara el hash de cada archivo en `datos/` contra los hashes registrados en ese manifiesto, detectando cualquier modificación en los archivos reales. Esto ilustra por qué ambas verificaciones son necesarias y complementarias: la firma garantiza la **autenticidad** del manifiesto, y el manifiesto garantiza la **integridad** de los archivos.
