"""
lsb_utils.py

Модуль для вставки та витягування даних у зображеннях методом LSB (Least Significant Bit).
Використовується для вбудовування цифрового підпису.
"""

import numpy as np
from PIL import Image


def lsb_insert(data, image_path, output_path, marker="SIGNATURE:"):
    """
    Вставляє байтові дані у зображення методом LSB (Least Significant Bit).

    Args:
        data (bytes): Дані для вбудовування (наприклад, цифровий підпис).
        image_path (str): Шлях до вхідного зображення.
        output_path (str): Шлях для збереження зображення з підписом.
        marker (str, optional): Маркер для вказівки кінця підпису. За замовчуванням 'SIGNATURE:'.
    """
    img = Image.open(image_path)
    img_data = np.array(img)

    binary_data = ''.join(format(byte, '08b') for byte in data)
    marker_binary = ''.join(format(ord(char), '08b') for char in marker)
    binary_data += marker_binary

    data_index = 0
    for row in range(img_data.shape[0]):
        for col in range(img_data.shape[1]):
            for channel in range(3):  # RGB
                if data_index < len(binary_data):
                    original = img_data[row, col, channel]
                    img_data[row, col, channel] = (original & 0xFE) | int(binary_data[data_index])
                    data_index += 1

    new_img = Image.fromarray(img_data)
    new_img.save(output_path)
    print(f"Підписане зображення збережено як {output_path}")


def lsb_extract(image_path, marker="SIGNATURE:"):
    """
    Витягує вбудовані дані з зображення, використовуючи метод LSB і заданий маркер завершення.

    Args:
        image_path (str): Шлях до зображення з вбудованим підписом.
        marker (str, optional): Маркер, що вказує кінець підпису. За замовчуванням 'SIGNATURE:'.

    Returns:
        bytes or None: Витягнутий підпис, якщо маркер знайдено; інакше None.
    """
    img = Image.open(image_path)
    img_data = np.array(img)

    binary_data = ''
    for row in range(img_data.shape[0]):
        for col in range(img_data.shape[1]):
            for channel in range(3):
                binary_data += str(img_data[row, col, channel] & 1)

    marker_binary = ''.join(format(ord(char), '08b') for char in marker)

    byte_array = []
    current_bits = ""
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i + 8]
        if len(byte) < 8:
            break
        byte_val = int(byte, 2)
        byte_array.append(byte_val)
        current_bits += byte

        if current_bits.endswith(marker_binary):
            signature = bytes(byte_array[:-len(marker_binary) // 8])
            return signature

    print("Маркер підпису не знайдено.")
    return None
