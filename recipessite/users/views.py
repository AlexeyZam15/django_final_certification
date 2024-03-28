from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import RegisterUserForm, LoginUserForm
from django.contrib import messages


def login_user(request):
    form = LoginUserForm(request.POST or None)
    if request.method == 'POST':
        form = LoginUserForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user and user.is_active:
                login(request, user=user)
                messages.success(request, 'Вы успешно вошли в систему')
                return redirect('index')
    context = {'form': form,
               'title': 'Авторизация',
               'url': 'login'}
    return render(request, 'users/login.html', context)


def logout_user(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Вы не авторизованы')
        return redirect('login')
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы')
    return redirect('login')


def register(request):
    form = RegisterUserForm()
    context = {'form': form,
               'title': 'Регистрация',
               'url': 'register',
               }
    return render(request, 'users/register.html', context)
