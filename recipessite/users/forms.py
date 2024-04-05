from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(
        label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(
        label="Логин", widget=forms.TextInput(attrs={'class': 'form-group'}))
    password1 = forms.CharField(
        label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-group'}))
    password2 = forms.CharField(
        label="Повторите пароль", widget=forms.PasswordInput(attrs={'class': 'form-group'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2', 'email', 'first_name', 'last_name']
        labels = {
            'email': 'Email',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }
        
    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Такой email уже зарегистрирован')
        return email
