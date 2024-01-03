from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from polls.models import Gifts, Gift1_History, Board
from polls.forms import GiftForm, BoardForm
from django.contrib.auth.models import User


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
    context['boards'] = Board.objects.all()
    return render(request, 'fields.html', context)

def create_board(request):
    context = {}
    all_users = User.objects.values()
    context['users'] = all_users
    if request.method == "POST":
        form = GiftForm(request.POST)
        if form.is_valid():
            users_id = form.cleaned_data['users_id']
            name = form.cleaned_data['name']
            description = '''
            web-игра морской бой. За каждую
            покупку на определенную сумму, будут начисляться бонусные
            выстрелы. Эти выстрелы можно тратить на поле морского боя и,
            если вы попадете в корабль, то получаете какой-либо гарантированный приз.
            '''
            size = form.cleaned_data['size']
            record = Board(name=name, size=size, users_id=users_id)
            record.save()
    return render(request, 'create_board.html', context)
def users_page(request):
    context = {}
    all_users = User.objects.values()
    context['users'] = all_users
    return render(request, 'users.html', context)


def edit_fields(request):
    context = {}
    return render(request, 'edit_fields.html', context)


def settings_gift(request):
    context = {}
    context['history'] = Gifts.objects.all()
    return render(request, 'settings_gift.html', context)


def create_gift(request):
    context = {}

    if request.method == "POST":
        form = GiftForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            record = Gifts(name=name, description=description)
            record.save()

    return render(request, 'Creategift.html', context)
