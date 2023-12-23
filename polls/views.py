from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate

def index_page(request):
    context = {}
    context['authors'] = 'Anton and Stanislav'
    context['pages'] = 2
    return render(request, 'index.html', context)


@login_required
def SeaBattle_page(request):
    context = {}
    return render(request, 'SeaBattle.html', context)

@login_required
def mygift_page(request):
    context = {}
    'aaaaa'
    return render(request, 'MyGifts.html', context)


def registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # получаем имя пользователя и пароль из формы
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            # выполняем аутентификацию
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def fields(request):
    context = {}
    return render(request, 'fields.html', context)

def users_page(request):
    context = {}
    return render(request, 'users.html', context)

def edit_fields(request):
    context = {}
    return render(request, 'edit_fields.html', context)

def settings_gift(request):
    context = {}
    return render(request, 'settings_gift.html', context)