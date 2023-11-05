from django.conf.urls import url

from cart.views import checkout, remove, remove_all, add, buy


urlpatterns = [
    url(r'^$', checkout, name="checkout"), #Він викликає відображення checkout, яке відображає сторінку оформлення замовлення кошика.
    url(r'^remove$', remove, name="remove"), #Він викликає відображення remove, яке обробляє видалення одного елемента з кошика
    url(r'^remove_all$', remove_all, name="remove_all"), #Він викликає відображення remove_all, яке обробляє видалення всіх елементів з кошика.
    url(r'^add$', add, name="add"), #Він викликає відображення add, яке обробляє додавання товару до кошика.
    url(r'^buy$', buy, name="buy"), # Він викликає відображення buy, яке, обробляє процес покупки товарів у кошику.
]
