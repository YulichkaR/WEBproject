from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(required=True)# Це поле для введення імені користувача. forms.CharField визначає текстове поле, в якому користувач може ввести своє ім'я. 
    from_email = forms.EmailField(required=True)#Це поле для введення електронної пошти користувача. forms.EmailField визначає текстове поле для введення адреси електронної пошти, і також вимагає, щоб введена адреса була дійсною електронною поштою
    subject = forms.CharField(required=True)#Це поле для введення теми повідомлення. Користувач може ввести тему свого повідомлення.
    message = forms.CharField(widget=forms.Textarea, required=True)#Це поле для введення тексту повідомлення. forms.CharField визначає текстове поле, яке може бути введено користувачем. widget=forms.Textarea вказує на використання багаторядкового текстового поля для введення повідомлення.