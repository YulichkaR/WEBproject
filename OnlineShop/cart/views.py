from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect

from cart.models import Cart, CartItem
from categories.models import Category
from goods.models import Good
from profiles.models import Profile


def checkout(request):#Цей метод відповідає за обробку GET-запитів на сторінку оформлення замовлення (checkout).
    if request.method == 'GET': #Перевіряється, чи HTTP-метод запиту - GET, тобто чи це запит на відображення сторінки.
        _cart = dict()#Створюється словник _cart для зберігання даних про кошик.
        profile = Profile.objects.filter(user=request.user)[0]#Отримується профіль користувача, який робить запит. Профіль пов'язаний з користувачем.   
        cart = list(filter(lambda x: x.is_active, Cart.objects.filter(profile=profile)))#Фільтруються кошики, які належать даному користувачеві та є активними (існують кошики, які можуть бути неактивними).
        if len(cart) > 0:#Якщо існують активні кошики, отримуються всі товари з цього кошика, і обчислюється загальна вартість замовлення та знижка.
            cart_items = CartItem.objects.filter(cart=cart[0])[::1]#В результаті, формується словник _cart, який містить дані про кошик, загальну суму та знижку.
            total = sum([cart_item.quantity * cart_item.good.price for cart_item in cart_items])
            discount = total - cart[0].total
            cart_total = cart[0].total + 50
            _cart['total'] = total
            _cart['discount'] = discount
            _cart['cart_total'] = cart_total
        else:
            cart_items = []
    else:
        cart_items = []
    goods = Good.objects.filter(featured=True)[:3]#Витягується список товарів, які рекомендовані (featured), і категорії товарів для відображення на сторінці оформлення замовлення.
    categories = Category.objects.all()[::1]
    return render(request, 'checkout.html', {'cart_items': cart_items, 'goods': goods, 'categories': categories, 'cart': _cart}) #Повертається відповідь, яка відображає сторінку checkout.html та передає дані про кошик, рекомендовані товари та категорії.


@csrf_protect
def remove(request):#Цей метод відповідає на POST-запити для видалення товару з кошика.
    if request.method == "POST" and request.user.is_authenticated:#Перевіряється, чи HTTP-метод запиту - POST, тобто це запит на видалення товару.
        profile = Profile.objects.filter(user=request.user)[0] #Отримується профіль користувача, який робить запит, та фільтруються активні кошики, належать користувачеві.
        cart = list(filter(lambda x: x.is_active, Cart.objects.filter(profile=profile)))
        if len(cart) > 0:
            item = CartItem.objects.get(id=request.POST.get('id'))#Отримується ідентифікатор товару, який користувач хоче видалити з кошика, Знаходиться відповідний товар із кошика та відбувається видалення цього товару з кошика.
            item.cart.total -= item.quantity * item.good.price #Оновлюється загальна сума кошика.
            item.cart.save()
            if item is not None:
                item.delete()
        return HttpResponse() #Повертається відповідь з порожнім вмістом (HTTP відповідь без тіла).
    else:
        return HttpResponseBadRequest()


@csrf_protect
def remove_all(request): #Цей метод відповідає на GET-запити для видалення всіх товарів з кошика.
    if request.method == "GET" and request.user.is_authenticated: #Перевіряється, чи HTTP-метод запиту - GET, тобто це запит на видалення всіх товарів з кошика.
        profile = Profile.objects.filter(user=request.user)[0]#Отримується профіль користувача, який робить запит, та фільтруються активні кошики, які належать користувачеві.
        cart = list(filter(lambda x: x.is_active, Cart.objects.filter(profile=profile))) #Для кожного товару в кошику, здійснюється його видалення з кошика.
        if len(cart) > 0:
            for item in CartItem.objects.filter(cart=cart[0]):
                item.delete()
            cart[0].total = 0 #Оновлюється загальна сума кошика.
            cart.save() #Після видалення всіх товарів з кошика, загальна сума кошика скидається до нуля.
        return redirect(request.META.get('HTTP_REFERER'))#Повертається перенаправлення на попередню сторінку (зворотній реферер).
    else:
        return HttpResponseBadRequest()


def add(request):#Цей метод відповідає на POST-запити для додавання товару до кошика. 
    if request.method == "POST" and request.user.is_authenticated: #Перевіряється, чи HTTP-метод запиту - POST, тобто це запит на додавання товару до кошика.
        profile = Profile.objects.filter(user=request.user)[0]#Отримується профіль користувача, який робить запит, та фільтруються активні кошики, які належать користувачеві.
        cart = list(filter(lambda x: x.is_active, Cart.objects.filter(profile=profile)))#Створюється новий товар у кошику або оновлюється існуючий, враховуючи кількість, матеріал та інші деталі.
        cartItem = CartItem()
        if len(cart) > 0:
            cartItem.cart = cart[0]
        else:
            cart = Cart()
            cart.profile = profile
            cart.total = 0.0
            cart.save()
            cartItem.cart = cart
        cartItem.quantity = int(request.POST.get('id_quantity'))
        cartItem.material = request.POST.get('id_material')
        cartItem.good = Good.objects.get(id=request.POST.get('id_good_id'))
        cartItem.save()
        return redirect('/good/{0}'.format(request.POST.get('id_good_id'))) #Після успішного додавання товару, користувач перенаправляється на сторінку товару, яку він додав до кошика.
    else:
        return HttpResponseBadRequest()


def buy(request):#Цей метод відповідає на POST-запити для підтвердження покупки. Ось деталі кожного кроку цього методу:
    if request.method == "POST" and request.user.is_authenticated:#Перевіряється, чи HTTP-метод запиту - POST, тобто це запит на підтвердження покупки.
        profile = Profile.objects.filter(user=request.user)[0]#Отримується профіль користувача, який робить запит, та фільтруються активні кошики, які належать користувачеві.
        cart = list(filter(lambda x: x.is_active, Cart.objects.filter(profile=profile)))[0]
        cart.is_active = False #Помічається, що кошик більше не активний, тобто покупка завершилася.
        cart.save()
        return redirect(request.META.get('HTTP_REFERER'))#Після підтвердження покупки, користувач перенаправляється на попередню сторінку (зворотній реферер).
    else:
        return HttpResponseBadRequest()
