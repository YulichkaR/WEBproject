from django.conf.urls import url

from contact.views import email_view, success_view

urlpatterns = [
    url(r'^$', email_view, name="email"), # Він викликає функцію відображення email_view, яка відповідає за відображення форми для відправлення повідомлення через форму зворотного зв'язку.
    url(r'^success$', success_view, name="success"), #Цей URL викликає функцію відображення success_view, яка відповідає за відображення сторінки успішного відправлення повідомлення або підтвердження
]
