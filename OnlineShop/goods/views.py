from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from cart.models import Cart, CartItem
from categories.models import Category
from comments.models import Comment
from goods.models import Good
from profiles.models import Profile


def good_detail_view(request, **kwargs): #Ця функція відображає сторінку деталей конкретного товару
    context = dict()
    try:
        good = Good.objects.get(id=kwargs['pk'])#Використовує ідентифікатор товару kwargs['pk'] для отримання відповідного товару.
        #Збирає інформацію про товар, коментарі до нього, рекомендовані товари, категорії та перевіряє, чи товар є в кошику користувача.
        context["good"] = good
        context["comments"] = Comment.objects.filter(good=good)[::1]
        context["goods"] = Good.objects.filter(featured=True)[:3]
        context["categories"] = Category.objects.all()[::1]
        profile = Profile.objects.filter(user=request.user)[0]
        carts = list(filter(lambda x: not x.is_active, Cart.objects.filter(profile=profile)))
        ids = set()
        for cart in carts:
            for item in CartItem.objects.filter(cart=cart)[::1]:
                ids.add(item.good.id)
        context["is_bought"] = good.id in ids
    except Good.DoesNotExist:
        raise Http404("Good does not exist")

    return render(request, 'good_detail.html', context)#Використовує шаблон good_detail.html для відображення інформації про товар та коментарів.


def catalog(request):#Ця функція відображає сторінку каталогу товарів
    context = dict()
    goods = Good.objects.all()[::1]

    category = request.GET.get('category')
    if category is not None:
        goods = list(filter(lambda g: g.category.name == category, goods))#Здійснює фільтрацію товарів залежно від різних параметрів, таких як категорія, ціна, рекомендації та інше.

    price = request.GET.get('price')
    if price is not None:
        if price == 'lower':
            goods.sort(key=lambda g: g.price)
        else:
            goods.sort(key=lambda g: g.price, reverse=True)

    recommend = request.GET.get('recommend')
    if recommend is not None:
        if recommend == 'true':
            goods = list(filter(lambda g: g.featured, goods))

    in_stock = request.GET.get('in_stock')
    if in_stock is not None:
        if in_stock == 'true':
            goods = list(filter(lambda g: g.in_stock, goods))

    name = request.GET.get('search')
    if name is not None:
        goods = list(filter(lambda g: g.name.lower().startswith(name.lower()), goods))

    categories = Category.objects.all()
    paginator = Paginator(goods, 6) #Використовує пагінацію для відображення обмеженої кількості товарів на сторінці.
    page = request.GET.get('page')
    good_list = paginator.get_page(page)
#Збирає інформацію про товари, категорії та інші параметри для відображення на сторінці каталогу.
    context['goods'] = goods[:3]
    context['good_list'] = good_list
    context['categories'] = categories
    context['page_range'] = list(paginator.page_range)

    return render(request, 'catalog.html', context)


def add_comment(request):#Ця функція додає коментар до конкретного товару.
    if request.method == "POST" and request.user.is_authenticated:#Перевіряє, чи користувач аутентифікований і чи є текст коментаря в POST-запиті.
        text = request.POST.get('comment_text') #Додає новий коментар до товару, до якого відноситься URL, з якого було викликано цей метод.
        if text is not None:
            comment = Comment()
            comment.user = request.user
            comment.text = text
            comment.good = Good.objects.get(id=request.META.get('HTTP_REFERER').split('/')[-1])
            comment.save()
        return redirect(request.META.get('HTTP_REFERER'))#Після додавання коментаря перенаправляє користувача на сторінку, з якої було викликано цей метод.
    else:
        return Http404()
