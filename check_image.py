"""
check_image.py

Модуль для перевірки цифрового підпису RSA, вбудованого у зображення методом LSB.
Підпис порівнюється з оригінальним вмістом зображення.
"""
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature
from lsb_utils import lsb_extract

def check_image(original_image_path, signed_image_path, public_key_path):
    """
    Перевіряє вбудований RSA-підпис у зображенні, використовуючи оригінальне зображення.
    
    Args:
        original_image_path (str): Шлях до оригінального (непідписаного) зображення.
        signed_image_path (str): Шлях до зображення з вбудованим підписом.
        public_key_path (str): Шлях до файлу з публічним RSA-ключем.
    """
    with open(public_key_path, "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())

    with open(original_image_path, "rb") as f:
        original_data = f.read()

    signature = lsb_extract(signed_image_path)

    if signature is None:
        print("Не вдалося витягти підпис.")
        return

    try:
        public_key.verify(
            signature,
            original_data,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        print("Підпис вірний.")
    except InvalidSignature:
        print("Невірний підпис.")

if __name__ == "__main__":
    ORIGINAL_IMAGE = "./input_image/test_image.png"
    PUBLIC_KEY = "./keys/public.pem"
    SIGNED_IMAGE = "./output_image/signed_image_lsb.png"

    check_image(ORIGINAL_IMAGE, SIGNED_IMAGE, PUBLIC_KEY)
