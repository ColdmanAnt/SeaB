from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from polls.models import Gifts, Board, Ship, BoardAccess
from polls.forms import GiftForm, BoardForm, ShipForm, ShotForm
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
def delete_field(request, board_id):
    context = {}
    board = Board.objects.get(id=board_id)
    board.delete()
    return render(request, 'admin/fields.html', context)


@staff_member_required
def delete_user_and_shots(request, access_id):
    context = {}
    access = BoardAccess.objects.all()
    for acc in access:
        if acc.id == access_id:
            acc.delete()
    return render(request, 'admin/addshot.html', context)


@staff_member_required
def delete_gift(request, gift_id):
    context = {}
    gift = Gifts.objects.get(id=gift_id)
    ships = Ship.objects.all()
    for ship in ships:
        if ship.gift_id == gift_id:
            ship.delete()
    gift.delete()
    return render(request, 'admin/settings_gift.html', context)

@staff_member_required
def delete_ship(request, ship_id):
    context = {}
    ship = Ship.objects.get(id=ship_id)
    ship.delete()
    return render(request, 'admin/AddShip.html', context)


@staff_member_required
def fields(request):
    context = {}
    context['boards'] = Board.objects.all()
    return render(request, 'admin/fields.html', context)


def add_ship(request, board_id):
    context = {}
    gifts = Gifts.objects.all()
    context['gifts'] = gifts
    ships = Ship.objects.filter(board_id=board_id)
    context['ships'] = ships
    board = Board.objects.get(id=board_id)
    context['board'] = board
    print(board.size)
    if request.method == "POST":
        form = ShipForm(request.POST)
        if form.is_valid():
            x = form.cleaned_data['x']
            y = form.cleaned_data['y']
            gift_id = form.cleaned_data['gift_id']
            record = Ship(x=x, y=y, board_id=board_id, gift_id=gift_id)
            record.save()
        else:
            print('aaaaa')
    return render(request, 'admin/AddShip.html', context)


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
            name = form.cleaned_data['name']
            size = form.cleaned_data['size']
            record = Board(name=name, size=size, users_id=[])
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


def battle_page(request, board_id):
    context = {}
    description = '''
                web-игра морской бой. За каждую\n
                покупку на определенную сумму, будут начисляться бонусные\n
                выстрелы. Эти выстрелы можно тратить на поле морского боя и,\n
                если вы попадете в корабль, то получаете какой-либо гарантированный приз.
                Совершайте выстрелы и выигрывайте призы, только учтите, что выстрелы ограничены
                '''
    context['description'] = description
    board = Board.objects.get(id=board_id)
    ships = Ship.objects.filter(board_id=board_id)
    field = [''] * board.size * board.size
    context['field'] = field
    context['board'] = board
    return render(request, 'user/battle.html', context)


@staff_member_required
def shots(request, board_id):
    context = {}
    board = Board.objects.get(id=board_id)
    users = User.objects.all()
    access = BoardAccess.objects.all()
    acc = []
    for b in access:
        if b.board_id == board_id:
            acc.append(b)
    context['access'] = acc
    array_users = []
    for user in users:
        if user.id in board.users_id:
            array_users.append(user)
    context['array_users'] = array_users
    context['users'] = users
    context['board'] = board
    if request.method == "POST":
        form = ShotForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            board.users_id.append(user)
            shot_count = form.cleaned_data['shots']
            record = BoardAccess(shots=shot_count, board_id=board_id, us=user)
            record.save()
            board.save()
        else:
            print('nooo')

            board.save()

    return render(request, 'admin/addshot.html', context)
