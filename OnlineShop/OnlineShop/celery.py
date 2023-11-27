from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

#Цей рядок встановлює змінну середовища DJANGO_SETTINGS_MODULE на OnlineShop.settings, що вказує, де знаходиться файл налаштувань Django для вашого проекту.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OnlineShop.settings')
# Тут створюється екземпляр Celery з ім'ям 'OnlineShop'. Це ім'я буде використовуватися для визначення файлів конфігурації та задач.
app = Celery('OnlineShop')

#Цей рядок конфігурує екземпляр Celery, використовуючи налаштування Django. Це включає в себе параметри, такі як BROKER_URL для налаштування брокера повідомлень, який використовується Celery.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Цей рядок вказує Celery автоматично визначати завдання (tasks) у вашому проекті. Це означає, що Celery шукатиме файли tasks.py у ваших Django-додатках і визначатиме завдання, що вони мають виконувати.
app.autodiscover_tasks()
