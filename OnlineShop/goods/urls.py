from django.conf.urls import url

from goods.views import good_detail_view, catalog, add_comment

urlpatterns = [
    url(r'^(?P<pk>\d+)$', good_detail_view, name="good"),
    #Цей URL-шлях відповідає за відображення сторінки деталей товару. Використовується регулярний вираз для визначення pk як числового ідентифікатора товару.
    # Призначений для виклику функції відображення good_detail_view.
    # Визначено ім'я good для цього URL-шляху
    url(r'^catalog$', catalog, name="catalog"),
     #Цей URL-шлях відповідає за відображення сторінки каталогу товарів.
     # Призначений для виклику функції відображення catalog.
     # Визначено ім'я catalog для цього URL-шляху
    url(r'^comment$', add_comment, name="add_comment"),
     # Цей URL-шлях відповідає за додавання коментарів до товарів.
     # Призначений для виклику функції відображення add_comment.
     # Визначено ім'я add_comment для цього URL-шляху.
]
