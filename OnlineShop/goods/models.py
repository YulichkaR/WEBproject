from django.db import models
from categories.models import Category
from django.urls import reverse


class Good(models.Model): #Ця модель представляє товари у вашому магазині.
    name = models.CharField(max_length=50, unique=True, db_index=True, verbose_name="Name")
    category = models.ForeignKey(Category, verbose_name="Category", on_delete=models.CASCADE)
    description = models.TextField(verbose_name="Short description")
    content = models.TextField(verbose_name="Additional information")
    price = models.FloatField(db_index=True, verbose_name="Price")
    price_acc = models.FloatField(null=True, blank=True, verbose_name="Price with discount")
    in_stock = models.BooleanField(default=True, db_index=True, verbose_name="In stock")
    comments = models.BooleanField(default=True, verbose_name="Comments status")
    featured = models.BooleanField(default=False, db_index=True, verbose_name="Recommended")
    image = models.ImageField(upload_to="goods/list", verbose_name="Main image")

    def __str__(self):
        return "{0}: {1}".format(self.category, self.name)

    def save(self, *args, **kwargs): #використовуються для очищення зображень при зміні або видаленні запису.
        try:
            this_record = Good.objects.get(pk=self.pk)
            if this_record.image != self.image:
                this_record.image.delete(save=False)
        except:
            pass
        super(Good, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.image.delete(save=False)
        super(Good, self).delete(*args, **kwargs)

    def get_absolute_url(self): #визначає URL для деталей товару, використовується для генерації посилань на сторінку товару.
        return reverse("goods_detail", kwargs={"pk": self.pk})

    class Meta: #визначає деякі метадані моделі, такі як назви та імена для адміністративного інтерфейсу.
        verbose_name = "Good"
        verbose_name_plural = "Goods"


class GoodImage(models.Model):#Ця модель представляє додаткові зображення для товарів. Кожний товар може мати багато додаткових зображень.
    good = models.ForeignKey(Good, verbose_name="Good", on_delete=models.CASCADE)#: Посилання на товар, до якого відноситься зображення (зв'язок з моделлю Good).
    image = models.ImageField(upload_to="goods/detail", verbose_name="Additional image")#Зображення товару, яке завантажується у папку "goods/detail".

    def save(self, *args, **kwargs):#використовуються для очищення зображень при зміні або видаленні запису.
        try:
            this_record = GoodImage.objects.get(pk=self.pk)
            if this_record.image != self.image:
                this_record.image.delete(save=False)
        except:
            pass
        super(GoodImage, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.image.delete(save=False)
        super(GoodImage, self).delete(*args, **kwargs)

    class Meta: #визначає деякі метадані моделі, такі як назви та імена для адміністративного інтерфейсу.
        verbose_name = "Good image"
        verbose_name_plural = "Good images"
