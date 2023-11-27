from django.db import models
from categories.models import Category
from django.urls import reverse
import enum
from django.dispatch import receiver
from django.db.models.signals import post_save
from OnlineShop.tasks import process_image, get_free_server_port

@enum.unique
class ImageStatus(str, enum.Enum):
    PENDING = "PENDING"
    COMPRESSING = "COMPRESSING"
    COMPRESSED = "COMPRESSED"

    @classmethod
    def choices(cls):
        return [(item.value, item.name) for item in cls]

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
    status = models.CharField(max_length=10, choices=ImageStatus.choices(), default=ImageStatus.PENDING)

    def __str__(self):
        return "{0}: {1}".format(self.category, self.name)

    # def save(self, *args, **kwargs): #використовуються для очищення зображень при зміні або видаленні запису.
    #     try:
    #         this_record = Good.objects.get(pk=self.pk)
    #         if this_record.image != self.image:
    #             this_record.image.delete(save=False)
    #     except:
    #         pass
    #     super(Good, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.image.delete(save=False)
        super(Good, self).delete(*args, **kwargs)

    def get_absolute_url(self): #визначає URL для деталей товару, використовується для генерації посилань на сторінку товару.
        return reverse("goods_detail", kwargs={"pk": self.pk})

    class Meta: #визначає деякі метадані моделі, такі як назви та імена для адміністративного інтерфейсу.
        verbose_name = "Good"
        verbose_name_plural = "Goods"

#Ця функція викликається при збереженні об'єкта моделі Good. Вона викликає асинхронну задачу за допомогою process_image.delay('test').
    def process_image_on_save(self):
        server_port = get_free_server_port()
        process_image.delay(self.image.name)

    def save(self, *args, **kwargs):
        # Викликати метод обробки зображення при збереженні моделі
        self.process_image_on_save()
        
        # У цьому рядку виконується спроба отримати запис про товар з бази даних за допомогою Good.objects.get(pk=self.pk). Це робиться для порівняння зображень: якщо нове зображення не таке, як попереднє (яке вже існує у базі даних), тоді попереднє зображення видаляється.
        try:
            this_record = Good.objects.get(pk=self.pk)
            if this_record.image != self.image:
                this_record.image.delete(save=False)
        except:
            pass
        super(Good, self).save(*args, **kwargs)
        #Цей рядок важливий, оскільки він відповідає за збереження змін в базу даних. 

class GoodImage(models.Model):#Ця модель представляє додаткові зображення для товарів. Кожний товар може мати багато додаткових зображень.
    good = models.ForeignKey(Good, verbose_name="Good", on_delete=models.CASCADE)#: Посилання на товар, до якого відноситься зображення (зв'язок з моделлю Good).
    image = models.ImageField(upload_to="goods/detail", verbose_name="Additional image")#Зображення товару, яке завантажується у папку "goods/detail".
    status = models.CharField(max_length=10, choices=ImageStatus.choices(), default=ImageStatus.PENDING)
    
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

# @receiver(post_save, sender=Good)
# def process_image_on_save(sender, instance, **kwargs):
#     if request.method == 'POST':
#         image_path = request.POST.get('image_path')

#         try:
#             server_port = get_free_server_port()

#             if not is_server_busy(server_port):
#                 process_image.delay(image_path, server_port)
#                 return JsonResponse({'status': 'Image processing started.'})
#             else:
#                 return JsonResponse({'status': f'Server {server_port} is busy. Try again later.'})
#         except Exception as e:
#             return JsonResponse({'status': str(e)})
#     else:
#         return JsonResponse({'status': 'Invalid request method.'})