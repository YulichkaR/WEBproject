from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.shortcuts import render, redirect

from categories.models import Category
from goods.models import Good
from profiles.forms import SignUpForm, LoginForm


def signup(request):
    if request.method == 'POST': #Цей перегляд відповідає за сторінку реєстрації нового користувача
        form = SignUpForm(request.POST) #Якщо запит типу POST, перегляд спробує створити нового користувача на основі даних, введених у форму SignUpForm.
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()#Після створення користувача, дані оновлюються для збігу з інформацією, введеною користувачем.
            user.username = form.cleaned_data.get('email').split('@')[0]
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            user.profile.subscribe = form.cleaned_data.get('subscribe')
            user.save()#Після створення користувача та автентифікації, користувач автоматично увійде в систему і буде перенаправлений на головну сторінку.
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            auth_login(request, user)
            return redirect('/')
    else: #Якщо запит типу GET, створюється порожній екземпляр форми SignUpForm і відображається сторінка реєстрації.
        form = SignUpForm()
    goods = Good.objects.filter(featured=True)[:3]
    categories = Category.objects.all()[::1]
    return render(request, 'signup.html', {'form': form, 'goods': goods, 'categories': categories})


def login(request): #Цей перегляд відповідає за сторінку входу користувача.
    if request.method == 'POST': #Перевіряє тип запиту (GET або POST).
        form = LoginForm(request.POST)#Якщо запит типу POST, перегляд спробує автентифікувати користувача на основі даних, введених у форму LoginForm
        if form.is_valid(): #Якщо користувач успішно автентифікується, він увійде в систему та буде перенаправлений на головну сторінку.
            username = form.cleaned_data.get('email').split('@')[0]
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                auth_login(request, user)
                return redirect('/')
    else: #Якщо запит типу GET, створюється порожній екземпляр форми LoginForm і відображається сторінка входу.
        form = LoginForm()
    goods = Good.objects.filter(featured=True)[:3]
    categories = Category.objects.all()[::1]
    return render(request, 'login.html', {'form': form, 'goods': goods, 'categories': categories})


def logout(request):#Цей перегляд відповідає за вихід користувача з системи
    auth_logout(request)
    return redirect('/profile/login') #При виклику цього перегляду, користувач виходить з системи і перенаправляється на сторінку входу.
