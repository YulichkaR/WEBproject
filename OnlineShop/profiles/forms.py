from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm): #Використовується для реєстрації нових користувачів
    first_name = forms.CharField()
    last_name = forms.CharField()
    subscribe = forms.BooleanField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try: #Перевіряє, чи введена електронна адреса (поле email) не використовується іншим користувачем. Якщо така адреса вже існує, видається відповідна помилка.
            match = User.objects.get(email=email)
        except User.DoesNotExist:
            return email

        raise forms.ValidationError('This email address is already in use.')

    class Meta: #Визначено клас Meta, де вказано модель User і поля, які включаються у форму.
        model = User
        fields = ('email', 'first_name', 'last_name', 'subscribe', 'password1', 'password2',)


class LoginForm(forms.Form): #Використовується для входу зареєстрованих користувачів в систему.
    email = forms.EmailField() #Містить поля для введення електронної адреси (email) і пароля (password).
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):#Під час автентифікації, перевіряє, чи існує користувач із введеною електронною адресою та правильним паролем. Якщо немає відповідного користувача, видається помилка "Wrong email or password".
        email = self.cleaned_data['email']
        username = email.split('@')[0]
        password = self.cleaned_data['password']
        if not authenticate(username=username, password=password):
            raise forms.ValidationError("Wrong email or password")
#Не має класу Meta, так як вона не пов'язана з конкретною моделлю користувача.