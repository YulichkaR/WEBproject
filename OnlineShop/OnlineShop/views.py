from django.http import JsonResponse #використовується для повернення відповідей у форматі JSON.
from .tasks import process_image

def process_image_view(request):#Оголошення функції process_image_view, яка обробляє HTTP-запити.
    if request.method == 'POST': #Перевірка, чи метод HTTP-запиту є POST. Якщо так, виконується наступне:
        image_path = request.POST.get('image_path')
        #Отримання значення параметра image_path з POST-запиту. Це передбачає, що в POST-запиті міститься параметр image_path, який визначає шлях до зображення.
        process_image.delay(image_path)#Виклик асинхронної задачі Celery process_image для обробки зображення з вказаним шляхом. Використовується метод .delay(), щоб запустити задачу асинхронно.
        return JsonResponse({'status': 'Image processing started.'})#Повернення відповіді у форматі JSON зі статусом "Image processing started."

    else:#Якщо метод HTTP-запиту не є POST, виконується наступне:
        return JsonResponse({'status': 'Invalid request method.'})#овернення відповіді у форматі JSON зі статусом "Invalid request method." для непідтриманого методу HTTP (в даному випадку, якщо не POST).
