from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model): #Визначає модель Profile, яка має поле user, що вказує на користувача, з яким пов'язаний цей профіль. Відношення здійснено за допомогою OneToOneField, що означає, що кожен користувач має один профіль, і навпаки
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, unique=False, db_index=True, verbose_name="First name")
    last_name = models.CharField(max_length=30, unique=False, db_index=True, verbose_name="Last name")
    subscribe = models.BooleanField(default=False, verbose_name="Subscribe")

    def __str__(self):
        return self.user.username #Метод __str__ повертає ім'я користувача, яке буде відображатися у списках об'єктів Profile.


@receiver(post_save, sender=User)#Це декоратор, який використовується для автоматичного створення профілю користувача при створенні нового користувача або оновленні інформації користувача.
def update_user_profile(sender, instance, created, **kwargs):#Функція update_user_profile викликається після збереження моделі User (користувача)
    if created:#Перевіряється, чи користувач був створений (created) або оновлений. Якщо користувач був створений, то створюється об'єкт Profile для цього користувача.
        Profile.objects.create(user=instance)
    else:#Якщо користувач був оновлений, то оновлюється ім'я та прізвище відповідного профілю.
        instance.profile.first_name = instance.first_name
        instance.profile.last_name = instance.last_name
    instance.profile.save() #Після створення або оновлення профілю, зміни зберігаються за допомогою методу save().
