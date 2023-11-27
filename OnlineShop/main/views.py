from django.views.generic.base import TemplateView
from categories.models import Category
from goods.models import Good

class MainPageView(TemplateView):
    template_name = "mainpage.html"#визначає ім'я шаблону, який буде використовуватися для відображення головної сторінки. У цьому випадку шаблон називається "mainpage.html"
    categories = Category.objects.all() # це два атрибути класу, які містять категорії та товари, які будуть відображені на головній сторінці. Вони ініціалізуються при створенні класу.
    goods = Good.objects.filter(featured=True)[:3]
    

    def get_context_data(self, **kwargs):#визначає контекст для передачі у шаблон. В даному випадку в контекст додаються дані про категорії та рекомендовані товари. Контекст є словником, який містить дані для відображення в шаблоні.
        context = super(MainPageView, self).get_context_data(**kwargs)
        context["categories"] = self.categories
        context["goods"] = self.goods
        return context
