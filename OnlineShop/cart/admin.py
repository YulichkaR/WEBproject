from django.contrib import admin
from goods.models import Good, GoodImage

admin.site.register(Good) #цей рядок реєструє модель Good в адміністративній панелі, щоб адміністратор міг керувати товарами через неї.
admin.site.register(GoodImage) #цей рядок реєструє модель GoodImage в адміністративній панелі, щоб адміністратор міг керувати зображеннями товарів.
