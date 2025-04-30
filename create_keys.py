"""
create_keys.py

Модуль для генерації RSA ключів (4096 біт) та збереження їх у форматах PEM.
Приватний ключ зберігається в PKCS8, публічний — у SubjectPublicKeyInfo.
"""
import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


def create_keys():
    """
    Ця функція створює нові публічний та приватний ключі RSA
    за допомогою бібліотеки `cryptography` і зберігає їх у папці `keys/`. 
    Файли:
        keys/private.pem — приватний ключ у форматі PKCS8 без паролю.
        keys/public.pem — публічний ключ у форматі SubjectPublicKeyInfo.
    """
    os.makedirs("keys", exist_ok=True)

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
    )

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    with open("keys/private.pem", "wb") as f:
        f.write(private_pem)
    with open("keys/public.pem", "wb") as f:
        f.write(public_pem)

    print("Ключі згенеровано та збережено в папці 'keys/'")

if __name__ == "__main__":
    create_keys()
