from django.conf.urls import url

from main.views import MainPageView

urlpatterns = [
    url(r'^$', MainPageView.as_view(), name="main"),
]
# Викликається клас-вид MainPageView.as_view(), який відповідає за відображення головної сторінки за допомогою класів.
# Визначено ім'я main для цього URL-шляху, яке можна використовувати для створення посилань 