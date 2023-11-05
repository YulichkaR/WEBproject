from django.core.mail import send_mail
from django.http import HttpResponse, BadHeaderError
from django.shortcuts import render, redirect

from categories.models import Category
from contact.forms import ContactForm
from goods.models import Good


def email_view(request):#ця функція відповідає за відображення сторінки для відправлення повідомлення через форму зворотного зв'язку.
    if request.method == 'GET':#Перевіряється, чи HTTP-метод запиту - GET. Якщо так, то форма створюється для відображення користувачу.
        form = ContactForm()
    else:
        form = ContactForm(request.POST) #Якщо HTTP-метод запиту - POST (користувач надіслав дані форми), то дані з форми перевіряються на валідність. Якщо форма є валідною, то виконується наступне:
        if form.is_valid():
            name = form.cleaned_data['name'] #Отримується ім'я користувача, тема повідомлення, адреса електронної пошти користувача та текст повідомлення з валідних даних форми.
            subject = "{0}: {1}".format(name, form.cleaned_data['subject'])#Створюється тема повідомлення, яка містить ім'я користувача та тему повідомлення.
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['yulichka2551@gmail.com'])
            except BadHeaderError: #Якщо заголовок повідомлення некоректний (BadHeaderError), повертається відповідь з повідомленням про помилку "Invalid header found."
                return HttpResponse('Invalid header found.')
            return redirect('success')#Якщо повідомлення вдало відправлено, користувач перенаправляється на сторінку успішного відправлення (функція success_view).
    goods = Good.objects.filter(featured=True)[:3]
    categories = Category.objects.all()[::1]
    return render(request, "contact.html", {'form': form, 'goods': goods, 'categories': categories})
#Після всіх перевірок, витягуються товари та категорії для відображення на сторінці.

def success_view(request):# Ця функція відповідає за відображення сторінки успішного відправлення повідомлення. Ось деталі кожного кроку цього методу:
    goods = Good.objects.filter(featured=True)[:3]#Витягуються товари та категорії для відображення на сторінці успішного відправлення.
    categories = Category.objects.all()[::1]
    return render(request, "success.html", {'goods': goods, 'categories': categories})#Повертається відповідь, яка відображає сторінку success.html та передає дані про товари та категорії.
