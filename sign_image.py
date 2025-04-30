"""
sign_image.py

Модуль для створення цифрового підпису зображення за допомогою RSA
та вбудовування цього підпису в зображення за допомогою LSB-методу.
"""

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from lsb_utils import lsb_insert

def sign_image(image_path, private_key_path, output_path):
    """
    Підписує зображення за допомогою приватного RSA-ключа та вбудовує підпис у зображення (LSB).

    Args:
        image_path (str): Шлях до зображення для підпису.
        private_key_path (str): Шлях до приватного ключа RSA.
        output_path (str): Шлях до збереження зображення з вбудованим підписом.
    """
    with open(private_key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(key_file.read(), password=None)

    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    signature = private_key.sign(
        image_data,
        padding.PKCS1v15(),
        hashes.SHA256()
    )

    lsb_insert(signature, image_path, output_path)
    print(f"Підпис вставлено у файл: {output_path}")


if __name__ == "__main__":
    INPUT_IMAGE = "./input_image/test_image.png"
    PRIVATE_KEY = "./keys/private.pem"
    OUTPUT_IMAGE = "./output_image/signed_image_lsb.png"

    sign_image(INPUT_IMAGE, PRIVATE_KEY, OUTPUT_IMAGE)
