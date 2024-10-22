from django.shortcuts import render
from .models import *
from .forms import UserRegister


def platform(request):
    return render(request, 'platform.html')


def catalog(request):
    title = 'Игры'
    games = Game.objects.all()
    context = {
        'title': title,
        'games': games

    }
    return render(request, 'catalog.html', context)


def cart(request):
    return render(request, 'cart.html')


def sign_up_by_djando(request):
    users = Buyer.objects.all()
    info = {}
    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            age = form.cleaned_data['age']

            if password != repeat_password:
                info['error'] = 'Пароли не совпадают'
            elif int(age) < 18:
                info['error'] = 'Вы должны быть старше 18'
            elif username in username_list(users):
                info['error'] = 'Пользователь уже существует'
            else:
                info['message'] = f'Приветствуем, {username}!'
                Buyer.objects.create(name=username,
                                     password=password,
                                     age=age)
        else:
            info['error'] = 'Данные не корректны'

    else:
        form = UserRegister()
    info['form'] = form
    return render(request, 'registration_page.html', info)


def username_list(users: list[Buyer]):
    list_username = []
    for user in users:
        list_username.append(str(user.name))
    return list_username
