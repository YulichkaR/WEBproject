from goods.models import Good, GoodImage, ImageStatus
from PIL import Image
import os
import time
import socket
import sys

#Обирається перший товар (Good), що має статус ImageStatus.PENDING.
#Якщо такий товар знайдено, йому присвоюється статус ImageStatus.COMPRESSING, і він зберігається.
#Затримка 10 секунд (модельна для імітації роботи зображення).
#Зображення стискається за допомогою функції compress_image.
#Після стискання товару, статус змінюється на ImageStatus.COMPRESSED, і товар знову зберігається.
def compressGood():
    good = Good.objects.select_for_update().filter(status=ImageStatus.PENDING).first()
    if good != None:
        print(f"Starting compressing {good.image.path}")
        good.status = ImageStatus.COMPRESSING
        good.save()
        time.sleep(10)
        compress_image(good.image.path)
        print(f"Finished compressing {good.image.path}")
        good.status = ImageStatus.COMPRESSED
        good.save()

#Ця функція аналогічна compressGood, але працює з моделлю GoodImage. Вона також використовує select_for_update, щоб уникнути конфліктів при паралельних операціях. Вибирається перше додаткове зображення (GoodImage), яке має статус ImageStatus.PENDING, і проводиться аналогічний процес стиснення та оновлення статусу.
def compressGoodImage():
    goodImage = GoodImage.objects.select_for_update().filter(status=ImageStatus.PENDING).first()
    if goodImage != None:
        print(f"Starting compressing {goodImage.image.path}")
        goodImage.status = ImageStatus.COMPRESSING
        goodImage.save()
        time.sleep(10)
        compress_image(goodImage.image.path)
        print(f"Finished compressing {goodImage.image.path}")
        goodImage.status = ImageStatus.COMPRESSED
        goodImage.save()

#Ця функція приймає шлях до зображення і необов'язковий параметр quality (значення за замовчуванням - 85) для налаштування якості стиснення JPEG. Вона використовує бібліотеку Pillow (яка є форком бібліотеки PIL) для відкриття, стиснення та збереження зображення у форматі JPEG. Функція виводить інформацію про стиснення, таку як розмір до та після стиснення та відносний відсоток стиснення.
def compress_image(input_path, quality=85):
    try:
        original_image = Image.open(input_path)
        original_size = os.path.getsize(input_path)
        original_image.save(input_path, quality=quality, format='JPEG')
        compressed_size = os.path.getsize(input_path)
        compression_ratio = (1 - compressed_size / original_size) * 100

        print(f"Image compressed and replaced at {input_path}")
        print(f"Original Size: {original_size}, Compressed Size: {compressed_size}, Compression ratio: {compression_ratio:.2f}%")

        return compression_ratio

    except Exception as e:
        print(f"Error: {e}")
        return None
