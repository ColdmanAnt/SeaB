from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from polls.models import Gifts, Gift1_History, Board
from polls.forms import GiftForm, BoardForm, EditForm
from django.contrib.auth.models import User


def index_page(request):
    context = {}
    context['authors'] = 'Anton and Stanislav'
    context['pages'] = 2
    return render(request, 'index.html', context)


@login_required
def SeaBattle_page(request):
    context = {}
    boards = Board.objects.all()
    game_boards = []
    for board in boards:
        if request.user.id in board.users_id:
            game_boards.append(board)
    context['boards'] = game_boards
    return render(request, 'user/SeaBattle.html', context)


@login_required
def mygift_page(request):
    context = {}
    'aaaaa'
    return render(request, 'user/MyGifts.html', context)


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


def check_admin(request):
    return request.user.is_superuser


@staff_member_required
def fields(request):
    context = {}
    context['boards'] = Board.objects.all()
    return render(request, 'admin/fields.html', context)

@staff_member_required
def create_board(request):
    context = {}
    all_users = User.objects.values()
    context['users'] = all_users
    description = '''
                web-игра морской бой. За каждую
                покупку на определенную сумму, будут начисляться бонусные
                выстрелы. Эти выстрелы можно тратить на поле морского боя и,
                если вы попадете в корабль, то получаете какой-либо гарантированный приз.
                '''
    context['description'] = description
    if request.method == "POST":
        form = BoardForm(request.POST)
        if form.is_valid():
            users_id = []
            user = form.cleaned_data['user']
            users_id.append(user)
            name = form.cleaned_data['name']
            size = form.cleaned_data['size']
            record = Board(name=name, size=size, users_id=users_id)
            record.save()
    return render(request, 'admin/create_board.html', context)

@staff_member_required
def users_page(request):
    context = {}
    all_users = User.objects.values()
    context['users'] = all_users
    return render(request, 'admin/users.html', context)

@staff_member_required
def edit_fields(request, board_id):
    context = {}
    all_users = User.objects.all()
    context['users'] = all_users
    description = '''
                    web-игра морской бой. За каждую
                    покупку на определенную сумму, будут начисляться бонусные
                    выстрелы. Эти выстрелы можно тратить на поле морского боя и,
                    если вы попадете в корабль, то получаете какой-либо гарантированный приз.
                    '''
    context['description'] = description
    board = Board.objects.get(id=board_id)
    context['board'] = board
    array_users = []
    for user in all_users:
        if user.id in board.users_id:
            array_users.append(user)
    context['array_users'] = array_users

    if request.method == "POST":
        form = BoardForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            board.users_id.append(user)
            board.name = form.cleaned_data['name']
            board.size = form.cleaned_data['size']
            board.save()
    return render(request, 'admin/edit_fields.html', context)

@staff_member_required
def settings_gift(request):
    context = {}
    context['history'] = Gifts.objects.all()
    return render(request, 'admin/settings_gift.html', context)

@staff_member_required
def create_gift(request):
    context = {}

    if request.method == "POST":
        form = GiftForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            record = Gifts(name=name, description=description)
            record.save()

    return render(request, 'admin/Creategift.html', context)

def battle_page(request):
    context = {}
    return render(request, 'user/battle.html', context)