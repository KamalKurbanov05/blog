from django import forms

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# class CustomAuthenticationForm(AuthenticationForm):
#     class Meta:
#         form = AuthenticationForm
#         fields = "__all__"
#         labels = {
#             "username": "foo",
#             "password": "bar"
#         }


class RegistrationsForm(UserCreationForm):
    name = forms.CharField(max_length=20, required=True, label='Имя', help_text='имя', )
    about_me = forms.CharField(widget=forms.TextInput(), label='Расскажите о себе',
                               required=False, )
    avatar = forms.ImageField(label='Аватар профиля', required=False, )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'name', 'about_me', 'avatar',)


class BlogForm(forms.Form):
    # for csv
    image = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
    )
    csv_file = forms.FileField(required=False, label='для csv файла', )
