from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from profiles.models import Profile
from goods.models import Good


class Cart(models.Model): #це модель, яка представляє кошик. Вона містить наступні поля:
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE) #Зв'язок з моделлю Profile через ForeignKey, який вказує на користувача, якому належить цей кошик.
    total = models.FloatField(default=0.0)#total: Поле, що представляє загальну суму кошика.
    is_active = models.BooleanField(default=True, verbose_name="Is active") #Поле типу boolean, яке вказує, чи активний цей кошик.

    def __str__(self):
        return "Cart - " + self.profile.user.username #повертає рядок, який представляє цей об'єкт


class CartItem(models.Model): # це модель, яка представляє товари в кошику. Вона містить наступні поля:
    good = models.ForeignKey(Good, on_delete=models.CASCADE)#Зв'язок з моделлю Good через ForeignKey, який вказує на товар.
    quantity = models.PositiveIntegerField(default=1)#: Кількість товару в кошику.
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE) #Зв'язок з моделлю Cart через ForeignKey, який вказує на кошик, до якого належить цей товар.
    material = models.CharField(max_length=10, default='rubber', verbose_name="Material") # Рядкове поле, яке вказує на матеріал товару.

    def __str__(self):
        return self.cart.profile.user.username + " - " + self.good.name #повертає рядок, який представляє цей об'єкт.


@receiver(pre_save, sender=CartItem) 
#@receiver(pre_save, sender=CartItem) - ця анотація встановлює сигнал pre_save для моделі CartItem. Сигнал викликається перед збереженням запису CartItem в базу даних.
def update_cart_total(sender, instance, **kwargs):
#Функція update_cart_total обробляє сигнал pre_save і виконує наступні дії:
# Перевіряє, чи це оновлення існуючого запису або створення нового.
# Отримує інформацію про попередню вартість товару та нову вартість товару.
# Оновлює загальну суму кошика шляхом вирахування попередньої вартості товару та додавання нової вартості товару.
# Зберігає зміни у кошику.
    if not instance._state.adding:
        db_instace = CartItem.objects.filter(cart=instance.cart, good=instance.good)[0]
        if db_instace.good.price_acc is None or db_instace.good.price >= db_instace.good.price:
            prev_cost = db_instace.quantity * db_instace.good.price
        else:
            prev_cost = db_instace.quantity * db_instace.good.price_acc
    else:
        prev_cost = 0.0

    if instance.good.price_acc is None or instance.good.price >= instance.good.price:
        cost = instance.quantity * instance.good.price
    else:
        cost = instance.quantity * instance.good.price_acc
    instance.cart.total -= prev_cost
    instance.cart.total += cost
    instance.cart.save()
